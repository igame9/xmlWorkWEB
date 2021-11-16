from django.apps import AppConfig


def loadClassif():
    import pickle
    loaded = pickle.load(open("KNN.dat", 'rb'))
    print("Классификатор загружен")
    return loaded


loadedClassif = loadClassif()


class XmlwebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xmlWEBApp'
