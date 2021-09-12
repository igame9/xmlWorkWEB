from django.urls import path
from . import views  # view из корня

app_name = 'xmlWEBApp'

urlpatterns = [
    path("", views.index, name="_indexPage_"),
    path('<str:any>/', views.xml, name="_xmlWork_"),  # '<str:any>.xml/'
    path('saveChange/save', views.saveChange, name="_saveXml_"),
    path('deleteFile/delete', views.deleteFile, name="_deleteXML_"),
    path('newXML/create', views.newXML, name="_newXML_"),
    path('findXML/find', views.findXML, name="_findXML_"),
    path('findXML/<str:any>.xml/', views.xml, name="_findXML_"),
]
