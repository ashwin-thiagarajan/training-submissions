from django.urls import path
from .views import ConvertCurrencyView

urlpatterns = [
    path('convert-currency/', ConvertCurrencyView.as_view(), name='convert-currency'),
]