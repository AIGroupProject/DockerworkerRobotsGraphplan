class Accion(object):
    def __init__(self, nombre, precondiciones, efectosN, efectosP):
        self.nombre = nombre
        self.precondiciones = precondiciones
        self.efectosN = efectosN
        self.efectosP = efectosP


    def getNombre(self):
        return self.nombre

    def getPrecondiciones(self):
        return self.precondiciones

    def getEfectosN(self):
        return self.efectosN

    def getEfectosP(self):
        return self.efectosP

    def siEsPrecondicion(self, atomo):
        return atomo in self.precondiciones

    def siEsEfectoN(self, atomo):
        return atomo in self.efectosN

    def siEsEfectoP(self, atomo):
        return atomo in self.efectosP

    def siPrecondEnLista(self,lista):
        for pred in self.precondiciones:
            if pred not in lista:
                return False
        return True
