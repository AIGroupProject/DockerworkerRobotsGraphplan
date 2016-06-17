from util.mutex import Mutex
from util.util import extraer_estado_inicial
from util.util import extraer_acciones
from util.util import extraer_objetivo
from util.accion import Accion

class Graphplan(object):
    def __init__(self, problema_planificacion):
        self.estado_inicial = extraer_estado_inicial(problema_planificacion)
        self.acciones = extraer_acciones(problema_planificacion)
        self.objetivos = extraer_objetivo(problema_planificacion)
        self.accion_persistencia = [x for x in problema_planificacion.acciones if 'persistencia' in x.nombre]
        self.niveles = []

    def graphPlan(self):
        self.niveles = []
        #Creamos un nivel que contendrá acciones y atomos
        capa_atomosa = CapaAtomos()
        capa_atomosa.setAtomos(self.estado_inicial)
        nivel = GraphplanNivel(capa_acciones=None, capa_atomos=capa_atomosa)
        i = 0
        #añadimos el nivel a niveles
        self.niveles.append(nivel)
        while True:
            if self.objetivos in self.niveles[i].capa_atomos.atomos: #sin mutex entre ellos
                print("Objetivos iguales a las precondiciones")
            else:
                i = i + 1
                #Creamos la capa de acciones
                # que tienen que cumplir las precondiciones de Pi-1
                capa_acciones = CapaAcciones()
                capa_atomos = CapaAtomos()
                capa_acciones.setAcciones(self.accionesAplicables(self.niveles[i-1]))
                capa_atomos.setAtomos(self.efectosAcciones(capa_acciones.acciones))

                #Calculamos mutex sobre la capa de acciones Ai
                capa_acciones.setAccionesMutex(self.accionesMutex(capa_acciones.acciones,self.niveles[i-1].capa_atomos))

                #Creamos la capa de atomos(efectos de aplicar acciones)
                proximoNivel = GraphplanNivel(capa_acciones,capa_atomos)
                #Calculamos mutex sobre la capa de atomos
                capa_atomos.setAtomosMutex(self.esAtomosMutex(proximoNivel))

                self.niveles.append(proximoNivel)

            # if la capa de atomos son las mismas en Pi-1 y Pi

            if all(atomo in self.niveles[i].capa_atomos.atomos for atomo in self.objetivos):
                return i

            # y además tienen los mismos mutex se termina el while mediante break
        #devolver fallo porq no se ha podido encontrar una solucion



    #metodo que dado un nivel devuelve la lista de acciones aplicables a ese nivel
    def accionesAplicables(self, nivelanterior):
        list = []
        for a in self.acciones:
            if a.es_aplicable(nivelanterior.capa_atomos.atomos):
                list.append(a)
        return list

    def efectosAcciones(self, acciones):
        efectos =[]
        for a in acciones:
            for efec in a.efectosp:
                if efec not in efectos:
                    efectos.append(efec)
        return efectos

    def accionesMutex(self, lista_acciones, capa_atomos):
        lista_acciones_mutex = []
        for acc1 in lista_acciones:
            for acc2 in lista_acciones:
                if(acc1 != acc2) and self.esAccionMutex(acc1, acc2):
                    lista_acciones_mutex.append(Mutex(acc1,acc2))
                else:
                    for atomo1 in capa_atomos.atomos:
                        for atomo2 in capa_atomos.atomos:
                            if Mutex(atomo1, atomo2) in capa_atomos.atomosMutex:
                                lista_acciones_mutex.append(Mutex(acc1, acc2))
        return lista_acciones_mutex

    def esAtomosMutex(self,nivel):
        lista_atomos_mutex = []
        for atomo1 in nivel.capa_atomos.atomos:
            for atomo2 in nivel.capa_atomos.atomos:
                if (atomo1!=atomo2) and self.esAtomoMutex(atomo1,atomo2,nivel.capa_acciones):
                    lista_atomos_mutex.append(Mutex(atomo1,atomo2))
        return lista_atomos_mutex




    def esAccionMutex(self,acc1,acc2):
        for efectn in acc1.efectosn:
            if efectn in acc2.precondiciones or efectn in acc2.efectosp:
                return True
        for efectn in acc2.efectosn:
            if efectn in acc1.precondiciones or efectn in acc1.efectosp:
                return True
        return False

    def esAtomoMutex(self,atomo1,atomo2,capa_acciones):
        for acc1 in capa_acciones.acciones:
            if atomo1 in acc1.efectosp and atomo2 in acc1.efectosp:
                return False
            for acc2 in capa_acciones.acciones:
                if (acc1!=acc2) and Mutex(acc1,acc2) in capa_acciones.accionesMutex:
                    True
        return False




class GraphplanNivel(object):
    def __init__(self, capa_acciones=None, capa_atomos=None):
        if capa_acciones is None:
            capa_acciones = CapaAcciones()
        if capa_atomos is None:
            capa_atomos = CapaAtomos()
        self.capa_acciones = capa_acciones
        self.capa_atomos = capa_atomos


class CapaAtomos(object):
    def __init__(self):
        self.atomos = []
        self.atomosMutex = []

    def setAtomos(self, lista_atomos):
        self.atomos=lista_atomos;

    def setAtomosMutex(self, lista_atomos_mutex):
        self.atomosMutex=lista_atomos_mutex

    def añadirAtomo(self,atomo):
        self.atomos.append(atomo)

    def añadirAtomosMutex(self,atomo1, atomo2):
        self.atomosMutex.append(Mutex(atomo1,atomo2))

class CapaAcciones(object):
    def __init__(self,):
        self.acciones = []
        self.accionesMutex = []

    def setAcciones(self, acciones):
        self.acciones = acciones

    def setAccionesMutex(self,acciones_mutex):
        self.accionesMutex = acciones_mutex

    def añadirAccion(self, accion):
        self.acciones.append(accion)

    def añadirAccionesMutex(self,accion1, accion2):
        self.accionesMutex.append(Mutex(accion1,accion2))
