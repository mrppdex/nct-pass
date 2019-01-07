from collections import OrderedDict, defaultdict
from io import BytesIO
import base64
import matplotlib.pyplot as plt

from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg, Sum

# Create your views here.
from .models import Vehicle
from .forms import VehicleForm, VehicleModelForm, VehicleYearForm


def update_context_with_graphics(context):
    failures_bar_dict = context['failures']
    bars_number_list = list(range(len(failures_bar_dict)))

    fig = plt.figure(figsize=(8, 3))
    ax = fig.add_subplot(111)
    ax.barh(bars_number_list, list(failures_bar_dict.values()))
    ax.set_yticks(bars_number_list)
    ax.set_yticklabels(list(failures_bar_dict.keys()), fontsize=15)
    ax.set_xticks([])
    ax.invert_yaxis()

    for i, (k, v) in enumerate(failures_bar_dict.items()):
        plt.text(v, i, str(v),
                 horizontalalignment='right',
                 verticalalignment='center',
                 fontsize=20, color='white')



    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()

    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = figfile.getvalue()
    figfile.close()

    graphic = base64.b64encode(figdata_png)

    context['graphic'] = graphic.decode('utf-8')
    return context

def make_context_dict(**kwargs):
    resp_query = Vehicle.objects.filter(**kwargs)
    resp = get_list_or_404(resp_query)
    resp = resp_query.aggregate(
                                Sum('passed'),
                                Sum('total'),
                                Sum('vehicle_and_safety_equipment'),
                                Sum('lighting_and_electrical'),
                                Sum('steering_and_suspension'),
                                Sum('braking_equipment'),
                                Sum('wheels_and_tyres'),
                                Sum('engine_noise_and_exhaust'),
                                Sum('chassis_and_body'),
                                Sum('side_slip_test'),
                                Sum('suspension_test'),
                                Sum('light_test'),
                                Sum('brake_test'),
                                Sum('emmissions'),
                                Sum('other'),
                                Sum('incompletable'),
                            )

    new_dict = {}
    for key, value in resp.items():
        new_dict[key.split("__")[0].replace("_"," ").title()] = value
    new_dict.pop('Passed')
    new_dict.pop('Total')
    new_dict = OrderedDict(sorted(new_dict.items(), key=lambda t: -t[1] if t[1] else 0))

    top_5 = {}
    for i, (k, v) in enumerate(new_dict.items()):
        if i>= 5 or not v:
            break
        top_5[k] = v

    if len(top_5)>0:
        top_max = sorted(top_5.items(), key=lambda x: -x[1])[0][1]

    top_ = {}
    for k, v in top_5.items():
        if v >= 0.4*top_max:
            top_[k] = v


    context = {**kwargs, 'failures': {**top_}}

    if resp['passed__sum']:
        context['passed'] = "{:.2f}".format(100.*resp['passed__sum']/resp['total__sum'])
    else:
        context['passed'] = "0"

    context['count'] = str(resp['total__sum'])

    return context

def index(request):
    if request.method == 'POST':
        #form = VehicleForm(request.POST)
        make_id = request.POST.get('make')
        #print("FORM IS_VALID: ", form.is_valid())
        #if form.is_valid():
        return HttpResponseRedirect(reverse('make_results', args=[make_id]))
    else:
        form = VehicleForm()

    return render(request, 'nctbrowse/index.html', {'form': form})

def vehicle_make_results(request, make_id):

    context = make_context_dict(make=make_id)
    #context = update_context_with_graphics(context)

    if request.method == 'POST':
        make_id = request.POST.get('make')
        model_id = request.POST.get('model')
        return HttpResponseRedirect(reverse('model_results', args=[make_id, model_id]))
    else:
        form = VehicleModelForm(make=make_id)
        context['form'] = form

    return render(request, 'nctbrowse/make_result.html', context)
    #return HttpResponse(f"{make_id} pass rate is: {resp}")

def vehicle_model_results(request, make_id, model_id):

    context = make_context_dict(make=make_id, model=model_id)
    #context = update_context_with_graphics(context)

    if request.method == 'POST':
        make_id = request.POST.get('make')
        model_id = request.POST.get('model')
        year_id= request.POST.get('year')
        return HttpResponseRedirect(reverse('year_results', args=[str(make_id), str(model_id), year_id]))
    else:
        form = VehicleYearForm(make=make_id, model=model_id)
        context['form'] = form

    return render(request, 'nctbrowse/model_result.html', context)


def vehicle_year_results(request, make_id, model_id, year_id):

    context = make_context_dict(make=make_id, model=model_id, year=year_id)
    context = update_context_with_graphics(context)

    return render(request, 'nctbrowse/final_result.html', context)
