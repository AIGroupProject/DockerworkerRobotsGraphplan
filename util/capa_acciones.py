class CapaAcciones(object):
    def __init__(self):
        self.acciones = []
        self.accionesMutex = []

    def getAcciones(self):
        return self.acciones

    def getAccionesMutex(self):
        return self.accionesMutex

