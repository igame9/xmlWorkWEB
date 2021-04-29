from django.urls import path
from . import views  # view из корня

app_name = 'xmlWEBApp'


urlpatterns = [
    path("", views.index, name="_indexPage_"),
    path('<str:any>.xml/', views.xml, name="_xmlWork_"),
    path('saveChange/', views.saveChange, name="_saveXml_"),
    path('deleteFile/', views.deleteFile, name="_deleteXML_"),
    path('newXML/', views.newXML, name="_newXML_"),
]
