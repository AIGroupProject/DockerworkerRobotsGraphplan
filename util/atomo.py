class Atomo(object):
    def __init__(self,nombre):
        self.nombre = nombre
        self.generadoras = [] #listas de acciones que generan este atomo

    def getName(self):
        return self.name

    def getGeneradoras(self):
        return self.generadoras

    def addGeneradora(self,accion):
        self.generadoras.append(accion)


