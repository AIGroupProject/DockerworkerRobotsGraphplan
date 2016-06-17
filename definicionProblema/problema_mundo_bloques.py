import random

import estructuraProblema.problema_planificación as probpl

import estructuraProblema.problema_planificación_HTN as probhtn

# Clases de símbolos de objetos
Bloques = ['A', 'B', 'C']


# Variables de estados
posición = probpl.VariableDeEstados(nombre='posición({b},{bmb})',
                                    b=Bloques,bmb=Bloques+['mesa','brazo'])
bloque_encima = probpl.VariableDeEstados(nombre='bloque_encima({b},{bn})',
                                         b=Bloques,bn=Bloques+['ninguno'])
bloque_cogido = probpl.VariableDeEstados(nombre='bloque_cogido({bn})',
                                         bn=Bloques+['ninguno'])


# Relaciones rígidas
bloques_distintos = probpl.RelaciónRígida(lambda b1, b2: b1 != b2)


# Operadores
coger_bloque_mesa = probpl.Operador(
    nombre='coger_bloque_mesa({b},{bmb})',
    precondiciones=[bloque_cogido({'ninguno': 'si'}),
                    posición({'{b},{bmb}': 'si'}),
                    bloque_encima({'{b},ninguno': 'si'})],
    efectos=[bloque_cogido({'{b}': 'si'}),
             posición({'{b},brazo': 'si'})],
    b=Bloques,
    bmb=Bloques+['mesa','brazo']
)
poner_bloque_mesa = probpl.Operador(
    nombre='poner_bloque_mesa({b})',
    precondiciones=bloque_cogido('{b}'),
    efectos=[bloque_cogido('ninguno'),
             posición({'{b}': 'mesa'})],
    b=Bloques
)
coger_bloque_pila = probpl.Operador(
    nombre='coger_bloque_pila({b1}, {b2})',
    precondiciones=[bloque_cogido('ninguno'),
                    posición({'{b1}': '{b2}'}),
                    bloque_encima({'{b1}': 'ninguno'})],
    efectos=[bloque_cogido('{b1}'),
             bloque_encima({'{b2}': 'ninguno'}),
             posición({'{b1}': 'brazo'})],
    relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
    b1=Bloques,
    b2=Bloques
)
poner_bloque_pila = probpl.Operador(
    nombre='poner_bloque_pila({b1}, {b2})',
    precondiciones=[bloque_cogido('{b1}'),
                    bloque_encima({'{b2}': 'ninguno'})],
    efectos=[bloque_cogido('ninguno'),
             bloque_encima({'{b2}': '{b1}'}),
             posición({'{b1}': '{b2}'})],
    relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
    b1=Bloques,
    b2=Bloques
)


# Instancia del problema
problema_mundo_bloques = probpl.ProblemaPlanificación(
    operadores=[coger_bloque_mesa,
                poner_bloque_mesa,
                coger_bloque_pila,
                poner_bloque_pila],
    estado_inicial=probpl.Estado(posición({'A': 'mesa',
                                           'B': 'mesa',
                                           'C': 'B'}),
                                 bloque_encima({'A': 'ninguno',
                                                'B': 'C',
                                                'C': 'ninguno'}),
                                 bloque_cogido('ninguno')),
    objetivos=posición({'A': 'B',
                        'B': 'C',
                        'C': 'mesa'})
)


# Métodos
colocar_bloque_en_mesa = probhtn.Método(
    nombre='colocar_bloque_en_mesa({b1}, {b2})',
    tarea='colocar({b1}, mesa)',
    subtareas=['despejar({b1})', 'mover({b1}, mesa)'],
    precondiciones=posición({'{b1}': '{b2}'}),
    relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
    b1=Bloques,
    b2=Bloques
)
colocar_bloque_en_bloque = probhtn.Método(
    nombre='colocar_bloque_en_bloque({b1}, {b2}, {b3})',
    tarea='colocar({b1}, {b2})',
    subtareas=['despejar({b1})', 'despejar({b2})', 'mover({b1}, {b2})'],
    precondiciones=posición({'{b1}': '{b3}'}),
    relaciones_rígidas=[bloques_distintos('{b1}', '{b2}'),
                        bloques_distintos('{b1}', '{b3}'),
                        bloques_distintos('{b2}', '{b3}')],
    b1=Bloques,
    b2=Bloques,
    b3=Bloques + ['mesa']
)
no_colocar_bloque = probhtn.Método(
    nombre='no_colocar_bloque({b1}, {b2})',
    tarea='colocar({b1}, {b2})',
    subtareas=[],
    precondiciones=posición({'{b1}': '{b2}'}),
    relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
    b1=Bloques,
    b2=Bloques + ['mesa']
)
despejar_bloque = probhtn.Método(
    nombre='despejar_bloque({b1}, {b2})',
    tarea='despejar({b1})',
    subtareas=['despejar({b2})', 'mover({b2}, mesa)'],
    precondiciones=bloque_encima({'{b1}': '{b2}'}),
    relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
    b1=Bloques,
    b2=Bloques
)
no_despejar_bloque = probhtn.Método(
    nombre='no_despejar_bloque({b})',
    tarea='despejar({b})',
    subtareas=[],
    precondiciones=bloque_encima({'{b}': 'ninguno'}),
    b=Bloques
)
mover_bloque = probhtn.Método(
    nombre='mover_bloque({b1}, {b2})',
    tarea='mover({b1}, {b2})',
    subtareas=['coger({b1})', 'poner({b1}, {b2})'],
    relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
    b1=Bloques,
    b2=Bloques + ['mesa']
)
coger_bloque_de_mesa = probhtn.Método(
    nombre='coger_bloque_de_mesa({b})',
    tarea='coger({b})',
    subtareas='coger_bloque_mesa({b})',
    precondiciones=posición({'{b}': 'mesa'}),
    b=Bloques
)
coger_bloque_de_bloque = probhtn.Método(
    nombre='coger_bloque_de_bloque({b1}, {b2})',
    tarea='coger({b1})',
    subtareas='coger_bloque_pila({b1}, {b2})',
    precondiciones=posición({'{b1}': '{b2}'}),
    relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
    b1=Bloques,
    b2=Bloques
)
poner_bloque_en_mesa = probhtn.Método(
    nombre='poner_bloque_en_mesa({b})',
    tarea='poner({b}, mesa)',
    subtareas='poner_bloque_mesa({b})',
    precondiciones=bloque_cogido('{b}'),
    b=Bloques
)
poner_bloque_en_bloque = probhtn.Método(
    nombre='poner_bloque_en_bloque({b1}, {b2})',
    tarea='poner({b1}, {b2})',
    subtareas='poner_bloque_pila({b1}, {b2})',
    precondiciones=bloque_cogido('{b1}'),
    relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
    b1=Bloques,
    b2=Bloques
)


problema_mundo_bloques_HTN = probhtn.ProblemaPlanificaciónHTN(
    operadores=[coger_bloque_mesa,
                poner_bloque_mesa,
                coger_bloque_pila,
                poner_bloque_pila],
    métodos=[colocar_bloque_en_mesa,
             colocar_bloque_en_bloque,
             no_colocar_bloque,
             despejar_bloque,
             no_despejar_bloque,
             mover_bloque,
             coger_bloque_de_mesa,
             coger_bloque_de_bloque,
             poner_bloque_en_mesa,
             poner_bloque_en_bloque],
    estado_inicial=probpl.Estado(posición({'A': 'mesa',
                                           'B': 'mesa',
                                           'C': 'B'}),
                                 bloque_encima({'A': 'ninguno',
                                                'B': 'C',
                                                'C': 'ninguno'}),
                                 bloque_cogido('ninguno')),
    tareas=['colocar(C, mesa)', 'colocar(B, C)', 'colocar(A, B)']
)

busqueda = probhtn.DescomposiciónHaciaAdelante();

print(busqueda.buscar(problema_mundo_bloques_HTN))


# Generador aleatorio de instancias del problema
class ProblemaMundoBloques(probhtn.ProblemaPlanificaciónHTN):
    def __init__(self, estado_inicial=None, nbloques=None, descripción=False):
        if estado_inicial is not None:
            nbloques = len(estado_inicial.posición)
        self.bloques = ['B{}'.format(b) for b in range(nbloques)]
        if descripción:
            print('Bloques:', self.bloques)
        self.posición = probpl.VariableDeEstados(nombre='posición({b})',
                                                 b=self.bloques)
        self.bloque_encima = probpl.VariableDeEstados(nombre='bloque_encima({b})',
                                                      b=self.bloques)
        self.bloque_cogido = probpl.VariableDeEstados(nombre='bloque_cogido')
        if estado_inicial is None:
            estado_inicial = self._generar_estado_inicial()
        if descripción:
            print('Estado inicial:', estado_inicial)
        operadores = self._generar_operadores()
        métodos = self._generar_métodos()
        tareas = self._generar_tareas()
        super().__init__(operadores, métodos, estado_inicial, tareas)
        self.objetivos = self._generar_objetivos()

    def _generar_estado_inicial(self):
        posición = {}
        bloque_encima = {b: 'ninguno' for b in self.bloques}
        bloques_libres = []
        bloques = self.bloques[:]
        random.shuffle(bloques)
        for b in bloques:
            posición_bloque = random.choice(bloques_libres + ['mesa'])
            posición[b] = posición_bloque
            if posición_bloque != 'mesa':
                bloque_encima[posición_bloque] = b
                bloques_libres.remove(posición_bloque)
            bloques_libres.append(b)
        return probpl.Estado(self.posición(posición),
                             self.bloque_encima(bloque_encima),
                             self.bloque_cogido('ninguno'))

    def _generar_operadores(self):
        bloques_distintos = probpl.RelaciónRígida(lambda b1, b2: b1 != b2)
        coger_bloque_mesa = probpl.Operador(
            nombre='coger_bloque_mesa({b})',
            precondiciones=[self.bloque_cogido('ninguno'),
                            self.posición({'{b}': 'mesa'}),
                            self.bloque_encima({'{b}': 'ninguno'})],
            efectos=[self.bloque_cogido('{b}'),
                     self.posición({'{b}': 'brazo'})],
            b=self.bloques
        )
        poner_bloque_mesa = probpl.Operador(
            nombre='poner_bloque_mesa({b})',
            precondiciones=self.bloque_cogido('{b}'),
            efectos=[self.bloque_cogido('ninguno'),
                     self.posición({'{b}': 'mesa'})],
            b=self.bloques
        )
        coger_bloque_pila = probpl.Operador(
            nombre='coger_bloque_pila({b1}, {b2})',
            precondiciones=[self.bloque_cogido('ninguno'),
                            self.posición({'{b1}': '{b2}'}),
                            self.bloque_encima({'{b1}': 'ninguno'})],
            efectos=[self.bloque_cogido('{b1}'),
                     self.bloque_encima({'{b2}': 'ninguno'}),
                     self.posición({'{b1}': 'brazo'})],
            relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
            b1=self.bloques,
            b2=self.bloques
        )
        poner_bloque_pila = probpl.Operador(
            nombre='poner_bloque_pila({b1}, {b2})',
            precondiciones=[self.bloque_cogido('{b1}'),
                            self.bloque_encima({'{b2}': 'ninguno'})],
            efectos=[self.bloque_cogido('ninguno'),
                     self.bloque_encima({'{b2}': '{b1}'}),
                     self.posición({'{b1}': '{b2}'})],
            relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
            b1=self.bloques,
            b2=self.bloques
        )
        return [coger_bloque_mesa,
                poner_bloque_mesa,
                coger_bloque_pila,
                poner_bloque_pila]

    def _generar_métodos(self):
        bloques_distintos = probpl.RelaciónRígida(lambda b1, b2: b1 != b2)
        colocar_bloque_en_mesa = probhtn.Método(
            nombre='colocar_bloque_en_mesa({b1}, {b2})',
            tarea='colocar({b1}, mesa)',
            precondiciones=self.posición({'{b1}': '{b2}'}),
            relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
            subtareas=['despejar({b1})', 'mover({b1}, mesa)'],
            b1=self.bloques,
            b2=self.bloques
        )
        colocar_bloque_en_bloque = probhtn.Método(
            nombre='colocar_bloque_en_bloque({b1}, {b2}, {b3})',
            tarea='colocar({b1}, {b2})',
            precondiciones=self.posición({'{b1}': '{b3}'}),
            relaciones_rígidas=[bloques_distintos('{b1}', '{b2}'),
                                bloques_distintos('{b1}', '{b3}'),
                                bloques_distintos('{b2}', '{b3}')],
            subtareas=['despejar({b1})', 'despejar({b2})', 'mover({b1}, {b2})'],
            b1=self.bloques,
            b2=self.bloques,
            b3=self.bloques + ['mesa']
        )
        no_colocar_bloque = probhtn.Método(
            nombre='no_colocar_bloque({b1}, {b2})',
            tarea='colocar({b1}, {b2})',
            precondiciones=self.posición({'{b1}': '{b2}'}),
            relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
            subtareas=[],
            b1=self.bloques,
            b2=self.bloques + ['mesa']
        )
        despejar_bloque = probhtn.Método(
            nombre='despejar_bloque({b1}, {b2})',
            tarea='despejar({b1})',
            precondiciones=self.bloque_encima({'{b1}': '{b2}'}),
            relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
            subtareas=['despejar({b2})', 'mover({b2}, mesa)'],
            b1=self.bloques,
            b2=self.bloques
        )
        no_despejar_bloque = probhtn.Método(
            nombre='no_despejar_bloque({b})',
            tarea='despejar({b})',
            precondiciones=self.bloque_encima({'{b}': 'ninguno'}),
            subtareas=[],
            b=self.bloques
        )
        mover_bloque = probhtn.Método(
            nombre='mover_bloque({b1}, {b2})',
            tarea='mover({b1}, {b2})',
            relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
            subtareas=['coger({b1})', 'poner({b1}, {b2})'],
            b1=self.bloques,
            b2=self.bloques + ['mesa']
        )
        coger_bloque_de_mesa = probhtn.Método(
            nombre='coger_bloque_de_mesa({b})',
            tarea='coger({b})',
            precondiciones=self.posición({'{b}': 'mesa'}),
            subtareas='coger_bloque_mesa({b})',
            b=self.bloques
        )
        coger_bloque_de_bloque = probhtn.Método(
            nombre='coger_bloque_de_bloque({b1}, {b2})',
            tarea='coger({b1})',
            precondiciones=self.posición({'{b1}': '{b2}'}),
            relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
            subtareas='coger_bloque_pila({b1}, {b2})',
            b1=self.bloques,
            b2=self.bloques
        )
        poner_bloque_en_mesa = probhtn.Método(
            nombre='poner_bloque_en_mesa({b})',
            tarea='poner({b}, mesa)',
            precondiciones=self.bloque_cogido('{b}'),
            subtareas='poner_bloque_mesa({b})',
            b=self.bloques
        )
        poner_bloque_en_bloque = probhtn.Método(
            nombre='poner_bloque_en_bloque({b1}, {b2})',
            tarea='poner({b1}, {b2})',
            precondiciones=self.bloque_cogido('{b1}'),
            relaciones_rígidas=bloques_distintos('{b1}', '{b2}'),
            subtareas='poner_bloque_pila({b1}, {b2})',
            b1=self.bloques,
            b2=self.bloques
        )
        return [colocar_bloque_en_mesa,
                colocar_bloque_en_bloque,
                no_colocar_bloque,
                despejar_bloque,
                no_despejar_bloque,
                mover_bloque,
                coger_bloque_de_mesa,
                coger_bloque_de_bloque,
                poner_bloque_en_mesa,
                poner_bloque_en_bloque]

    def _generar_tareas(self):
        pila = ['mesa'] + self.bloques
        return ['colocar({}, {})'.format(pila[i], pila[i - 1])
                for i in range(1, len(pila))]

    def _generar_objetivos(self):
        pila = ['mesa'] + self.bloques
        posición = {pila[i]: pila[i - 1] for i in range(1, len(pila))}
        return [self.posición(posición)]
