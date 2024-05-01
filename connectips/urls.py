
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="connectips"),
    path('submit/', views.Submit.as_view(), name="submit-connectips"),
    path('success-form-connectips/', views.Submit.as_view(), name="success-form-connectips"),
    path('form-redirect/', views.FormRedirect.as_view(), name="form-redirect"),
    # path('return-khalti/', webhooks.Return_URL, name="return-khalti"),
]
