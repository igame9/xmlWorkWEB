from django.urls import path
from . import views  # view из корня

urlpatterns = [
    path("", views.index, name="_indexPage_"),
    path('<str:any>.xml/', views.xml, name="_xmlWork_"),
]
