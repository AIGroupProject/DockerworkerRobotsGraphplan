import itertools
import copy
import problema_planificación as probpl


class InstanciaMétodo:
    def __init__(self, nombre, tarea, subtareas, precondiciones):
        self.nombre = nombre
        self.tarea = tarea
        self.subtareas = subtareas
        self.precondiciones = precondiciones

    def es_aplicable(self, estado):
        return all(estado.satisface(precondición)
                   for precondición in self.precondiciones)


class Método:
    def __init__(self, nombre, tarea, subtareas,
                 precondiciones=None, relaciones_rígidas=None,
                 **variables):
        self.nombre = nombre
        self.tarea = tarea
        if not isinstance(subtareas, list):
            subtareas = [subtareas]
        self.subtareas = subtareas
        if precondiciones is None:
            precondiciones = []
        if not isinstance(precondiciones, list):
            precondiciones = [precondiciones]
        self.precondiciones = precondiciones
        if relaciones_rígidas is None:
            relaciones_rígidas = []
        if not isinstance(relaciones_rígidas, list):
            relaciones_rígidas = [relaciones_rígidas]
        self.relaciones_rígidas = relaciones_rígidas
        self.variables = variables

    def _procesar(self, componente, asignación):
        nueva_componente = copy.deepcopy(componente)
        for valores_dominios, valor_variable in nueva_componente.items():
            del nueva_componente[valores_dominios]
            nuevos_valores = tuple(valor.format(**asignación) for valor in valores_dominios)
            nuevo_valor = valor_variable.format(**asignación)
            nueva_componente[nuevos_valores] = nuevo_valor
        return nueva_componente

    def obtener_instancia(self, asignación):
        nombre = self.nombre.format(**asignación)
        tarea = self.tarea.format(**asignación)
        precondiciones = [self._procesar(precondición, asignación)
                          for precondición in self.precondiciones]
        subtareas = [subtarea.format(**asignación)
                     for subtarea in self.subtareas]
        return InstanciaMétodo(nombre, tarea, subtareas, precondiciones)

    def verifica_relaciones_rígidas(self, asignación):
        return all(relación_rígida.verifica(asignación)
                   for relación_rígida in self.relaciones_rígidas)

    def obtener_instancias(self):
        nombres_variables = self.variables.keys()
        valores_variables = self.variables.values()
        producto_valores = itertools.product(*valores_variables)
        asignaciones = (dict(zip(nombres_variables, valores)) for valores in producto_valores)
        return [self.obtener_instancia(asignación) for asignación in asignaciones
                if self.verifica_relaciones_rígidas(asignación)]


class ProblemaPlanificaciónHTN(probpl.ProblemaPlanificación):
    def __init__(self, operadores, métodos, estado_inicial=None, tareas=None):
        super().__init__(operadores, estado_inicial)
        if tareas is None:
            tareas = []
        if not isinstance(tareas, list):
            tareas = [tareas]
        self.tareas = tareas
        if métodos is None:
            métodos = []
        if not isinstance(métodos, list):
            métodos = [métodos]
        instancias_métodos = sum((método.obtener_instancias() for método in métodos), [])
        self.métodos_relevantes = {}
        for instancia_método in instancias_métodos:
            tarea = instancia_método.tarea
            self.métodos_relevantes.setdefault(tarea, []).append(instancia_método)
        for acción in self.acciones:
            self.métodos_relevantes[acción.nombre] = acción

    def es_primitiva(self, tarea):
        return isinstance(self.métodos_relevantes.get(tarea, None), probpl.AcciónPlanificación)


class DescomposiciónHaciaAdelante:
    def __init__(self, detallado=False):
        self.detallado = detallado

    def buscar(self, problema):
        self.problema = problema
        return self._buscar(problema.estado_inicial, problema.tareas, [])

    def _buscar(self, estado, tareas, plan):
        if self.detallado:
            print('Estado:', estado)
            print('Tareas a realizar:', tareas)
        if not tareas:
            return plan
        tarea = tareas[0]
        # if self.detallado:
        #     print('Realizando la tarea {}...'.format(tarea))
        if self.problema.es_primitiva(tarea):
            if self.detallado:
                print('La tarea {} es primitiva'.format(tarea))
            acción_relevante = self.problema.métodos_relevantes[tarea]
            if acción_relevante.es_aplicable(estado):
                if self.detallado:
                    print('La tarea {} es aplicable'.format(tarea))
                nuevo_estado = acción_relevante.aplicar(estado)
                return self._buscar(nuevo_estado, tareas[1:], plan + [tarea])
            else:
                if self.detallado:
                    print('La tarea {} no es aplicable'.format(tarea))
                return None
        else:
            if self.detallado:
                print('La tarea {} es no primitiva'.format(tarea))
            métodos = self.problema.métodos_relevantes.get(tarea, [])
            # print('Métodos relevantes para la tarea {}: {}'.format(
            #     tarea, [método.nombre for método in métodos]))
            if not métodos:
                print('No hay métodos para descomponer la tarea {}'.format(tarea))
            for método in métodos:
                if self.detallado:
                    print('Descomponiendo la tarea {} con el método {}...'.format(
                        tarea, método.nombre))
                if método.es_aplicable(estado):
                    if self.detallado:
                        print('El método {} es aplicable'.format(método.nombre))
                    nuevas_tareas = método.subtareas
                    solución = self._buscar(estado, nuevas_tareas + tareas[1:], plan)
                    if solución is not None:
                        return solución
                else:
                    if self.detallado:
                        print('El método {} no es aplicable'.format(método.nombre))
            return None
