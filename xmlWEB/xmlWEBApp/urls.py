from django.urls import path
from . import views  # view из корня
from . import viewsLearn

app_name = 'xmlWEBApp'

urlpatterns = [
    path("", views.index, name="_indexPage_"),
    path('<str:any>/', views.xml, name="_xmlWork_"),  # '<str:any>.xml/'
    path('saveChange/save', views.saveChange, name="_saveXml_"),
    path('deleteFile/delete', views.deleteFile, name="_deleteXML_"),
    path('newXML/create', views.newXML, name="_newXML_"),
    path('findXML/find', views.findXML, name="_findXML_"),
    path('findXML/<str:any>/', views.xml, name="_findXML_"),
    path('learn/nlp', viewsLearn.nlp, name="_nlp_"),
    path('learn/learnModel', viewsLearn.learnModel, name="_learn_"),
    path('learn/test', viewsLearn.testLearn, name="_test_"),
    path('learn/accuracy', viewsLearn.accuracyClassif, name="_accuracy_"),
    path('getPredict/predict', views.getPredict, name="_getPredict_"),
    path('newXML/autofill', views.autoFillArticle, name="_autoFillArticle_"),

]
