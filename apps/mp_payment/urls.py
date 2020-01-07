from django.urls import path

from . import views

app_name = 'map_payment'

urlpatterns = [
    path(
        'token/capture/',
        views.CreditCardWebTokenCaptureView.as_view(),
        name='capture'
    ),
]
