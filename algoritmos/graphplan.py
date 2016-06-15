class Graphplan(object):
    def __init__(self, problema_planificacion):
        self.estado_inicial = problema_planificacion.estado_inicial
        self.acciones = problema_planificacion.acciones
        self.objetivos = problema_planificacion.objetivos
        self.accion_persistencia = [x for x in self.acciones if 'persistencia' in x.nombre]

    def graphPlan(self):
        niveles = []
        nivel = GraphplanNivel(capa_acciones=None, capa_atomos=self.estado_inicial)

        i = 0
        while True:
            if self.objetivos in P:
                print("Objetivos iguales a las precondiciones")
            else:
                i = i + 1
                # for ()


class GraphplanNivel(object):
    def __init__(self, capa_acciones=None, capa_atomos=None):
        if capa_acciones is None:
            capa_acciones = []
        if capa_atomos is None:
            capa_atomos = []
        self.capa_acciones = capa_acciones
        self.capa_atomos = capa_atomos


class CapaAtomos(object):
    def __init__(self):
        self.capaAtomosSinMutex = []
        self.capaAtomosMutex = []


class CapaAcciones(object):
    def __init__(self):
        self.capaAcciones = []
