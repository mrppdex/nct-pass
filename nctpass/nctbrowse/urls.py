from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<make_id>/', views.vehicle_make_results, name='make_results'),
    path('<make_id>/<model_id>/', views.vehicle_model_results, name='model_results'),
    path('<make_id>/<model_id>/<int:year_id>/', views.vehicle_year_results, name='year_results'),
]
