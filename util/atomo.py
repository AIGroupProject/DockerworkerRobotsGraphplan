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

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)