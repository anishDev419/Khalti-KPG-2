
from django.contrib import admin
from django.urls import path
from . import views
from . import webhooks

urlpatterns = [
    path('', views.Index.as_view(), name="khalti"),
    path('submit/', views.Submit.as_view(), name="submit-khalti"),
    path('success-form-khalti/', views.SuccessForm.as_view(), name="success-form-khalti"),
    # path('return-khalti/', views.ReturnURL, name="return-khalti"),
    # path('return-khalti/', webhooks.Return_URL, name="return-khalti"),
]
