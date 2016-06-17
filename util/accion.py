class Accion(object):
    def __init__(self, nombre, precondiciones, efectosp, efectosn):
        self.nombre = nombre
        self.precondiciones = precondiciones
        self.efectosp = efectosp
        self.efectosn = efectosn


    def get_nombre(self):
        return self.nombre

    def get_precondiciones(self):
        return self.precondiciones

    def get_efectosp(self):
        return self.efectosp

    def get_efectosn(self):
        return self.efectosn

