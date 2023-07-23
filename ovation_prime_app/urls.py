from django.urls import path

from . import views

urlpatterns = [
    path('conductance_interpolated/', views.get_ovation_prime_conductance_interpolated),
    path('conductance/', views.get_ovation_prime_conductance),
    path('weighted_flux/', views.get_weighted_flux),
    path('weighted_flux_interpolated/', views.get_weighted_flux_interpolated),
    path('seasonal_flux/', views.get_seasonal_flux),
]
