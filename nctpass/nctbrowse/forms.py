from django import forms
from django.forms import ModelChoiceField
from .models import Vehicle

class ModelModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title()

class VehicleForm(forms.Form):
    make = ModelModelChoiceField(
        queryset=Vehicle.objects.values_list('make', flat=True).distinct().order_by('make'),
        #queryset=Vehicle.objects.all().distinct('make'),
        label='',
        widget=forms.Select(attrs={"onChange":'this.form.submit()'}),
        empty_label="Select Make:",
    )

class VehicleModelForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.make = kwargs.pop('make')
        super(VehicleModelForm, self).__init__(*args, **kwargs)

        self.fields['model'] = ModelChoiceField(
            label='',
            queryset=Vehicle.objects.filter(make=self.make) \
                                    .values_list('model', flat=True) \
                                    .distinct().order_by('model'),
            widget=forms.Select(attrs={"onChange":'this.form.submit()'}),
            empty_label="Select Model:",
        )

class VehicleYearForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.make = kwargs.pop('make')
        self.model = kwargs.pop('model')
        super(VehicleYearForm, self).__init__(*args, **kwargs)

        self.fields['year'] = ModelChoiceField(
            label='',
            queryset=Vehicle.objects.filter(make=self.make, model=self.model) \
                            .values_list('year', flat=True).distinct() \
                            .order_by('year'),
            widget=forms.Select(attrs={"onChange":'this.form.submit()'}),
            empty_label="Select Year:",
        )
