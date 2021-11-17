from django.apps import AppConfig
import pickle


def loadClassif():
    loaded = pickle.load(open("KNN.dat", 'rb'))
    print("Классификатор загружен")
    return loaded


loadedClassif = loadClassif()


class XmlwebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xmlWEBApp'
