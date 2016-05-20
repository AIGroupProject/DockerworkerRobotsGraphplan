import random
import Algorithm.problema_planificación as probpl
import numpy as np

# Clases de símbolos de objetos
Localizaciones = ['l1', 'l2', 'l3']
Robots = ['r1']
Gruas = ['g1', 'g2']
Contenedores = ['c1', 'c2', 'c3']
ContenedoresYSuelo = Contenedores + ['suelo']

# Variables de estados

contenedor_cogido = probpl.VariableDeEstados(
    nombre='contenedor_codigo({b})',
    b=(Localizaciones, Gruas))

posicion_contenedor = probpl.VariableDeEstados(
    nombre='posicion_contenedor({b})',
    b=Contenedores)

localizacion_contenedor = probpl.VariableDeEstados(
    nombre='localizacion_contenedor({b})',
    b=Contenedores
)

contenedor_encima = probpl.VariableDeEstados(
    nombre='contenedor_encima({b})',
    b=ContenedoresYSuelo
)

localizacion_robot = probpl.VariableDeEstados(
    nombre='localizacion_robot({b})',
    b=Robots
)

# Ejemplo impresion de Variable de Estado
print(contenedor_encima({'c1': 'Ninguno'}))

## Esto se puede sacar a una clase que contruya una matriz
## tal como se hace aqui, con sus get y set
traceabilityMatrix = np.zeros((len(Localizaciones), len(Localizaciones)), dtype='bool')
# l1 adyacente l2
traceabilityMatrix[0][1] = True
# l2 adyacente l3
traceabilityMatrix[1][2] = True

matrizTrazSimet = (traceabilityMatrix + traceabilityMatrix.T)

print(matrizTrazSimet)

# Relaciones rígidas
adyacente = probpl.RelaciónRígida(lambda x, y:
                                  matrizTrazSimet[
                                      Localizaciones.index(x),
                                      Localizaciones.index(y)])

##Prueba de la función lambda
adyacente_fun = lambda x, y: matrizTrazSimet[
    Localizaciones.index(x),
    Localizaciones.index(y)]
print('¿Existe relacion de adyacencia?', adyacente_fun('l1', 'l3'))

radio = {'g1': ['l1', 'l2'], 'g2': ['l3']}

radio_accion = probpl.RelaciónRígida(lambda grua, localizacion:
                                     localizacion in radio[grua])

##Prueba de la función lambda
radio_fun = lambda grua, localizacion: localizacion in radio[grua]

print('¿Esta en el radio de accion?', radio_fun('g1', 'l3'))




# Operadores

desplazar_robot_contenedor = probpl.Operador(
    nombre='desplazar_robot_contenedor({l1},{l2},{r},{c})',
    precondiciones=[localizacion_robot({'{r}': '{l1}'}),
                    localizacion_contenedor({'{c}': '{l1}'})],
    efectos=[localizacion_robot({'{r}': '{l2}'}),
             localizacion_contenedor({'{c}': '{l2}'})],
    relaciones_rígidas=adyacente('{l1}', '{l2}'),
    l1=Localizaciones,
    l2=Localizaciones,
    r=Robots,
    c=Contenedores
)

desplazar_robot = probpl.Operador(
    nombre='desplazar_robot({l1},{l2},{r})',
    precondiciones=[localizacion_robot({'{r}': '{l1}'})],
    efectos=[localizacion_robot({'{r}': '{l2}'})],
    relaciones_rígidas=adyacente('{l1}', '{l2}'),
    l1=Localizaciones,
    l2=Localizaciones,
    r=Robots
)

coger_contenedor_suelo = probpl.Operador(
    nombre='coger_contenedor_suelo({c},{l},{g})',
    precondiciones=[contenedor_cogido({'{g}': 'ninguno'}),
                    posicion_contenedor({'{c}': 'suelo'}),
                    localizacion_contenedor({'{c}': '{l}'})],
    efectos=[contenedor_cogido({'{g}': '{c}'}),
             posicion_contenedor({'{c}': '{g}'})],
    relaciones_rígidas=radio_accion('{g}', '{l}'),
    c=Contenedores,
    l=Localizaciones,
    g=Gruas
)

coger_contenedor_pila = probpl.Operador(
    nombre='coger_contenedor_pila',
    precondiciones=[contenedor_cogido({'{g}': 'ninguno'}),
                    posicion_contenedor({'{c1}': '{c2}'}),
                    contenedor_encima({'{c1}': 'ninguno'}),
                    localizacion_contenedor({'{c1}': '{l}'}),
                    localizacion_contenedor({'{c2}': '{l}'})],
    efectos=[contenedor_cogido({'{g}': '{c1}'}),
             posicion_contenedor({'{c1}': '{g}'}),
             contenedor_encima({'{c2}': 'ninguno'})],
    relaciones_rígidas=radio_accion('{g}', '{l}'),
    c1=Contenedores,
    c2=Contenedores,
    l=Localizaciones,
    g=Gruas
)

coger_contenedor_robot = probpl.Operador(
    nombre='coger_contenedor_robot',
    precondiciones=[localizacion_contenedor({'{c}': '{l}'}),
                    contenedor_cogido({'{g}': 'ninguno'}),
                    contenedor_cogido({'{r}': '{c}'}),
                    localizacion_robot({'{r}': '{l}'})],
    efectos=[contenedor_cogido({'{g}': '{c}'}),
             contenedor_cogido({'{r}': 'ninguno'})],
    relaciones_rígidas=radio_accion('{g}', '{l}'),
    c=Contenedores,
    g=Gruas,
    l=Localizaciones,
    r=Robots
)

poner_contenedor_suelo = probpl.Operador(
    nombre='poner_contenedor_suelo',
    precondiciones=[contenedor_cogido({'{g}': '{c}'}),
                    contenedor_encima({'suelo': 'ninguno'})],
    efectos=[contenedor_cogido({'{g}': 'ninguno'}),
             contenedor_encima({'suelo': '{c}'})],
    relaciones_rígidas=radio_accion('{g}', '{l}'),
    c=Contenedores,
    g=Gruas,
    l=Localizaciones
)

poner_contenedor_pila = probpl.Operador(
    nombre='poner_contenedor_pila',
    precondiciones=[contenedor_cogido({'{g}': '{c1}'}),
                    posicion_contenedor({'{c1}': '{g}'}),
                    localizacion_contenedor({'{c2}': '{l}'}),
                    contenedor_encima({'{c2}': 'ninguno'})],
    efectos=[contenedor_cogido({'{g}': 'ninguno'}),
             contenedor_encima({'{c2}': '{c1}'}),
             posicion_contenedor({'{c1}': '{c2}'}),
             contenedor_encima({'{c2}': 'ninguno'})
             ],
    relaciones_rígidas=radio_accion('{g}', '{l}'),
    c1=Contenedores,
    c2=Contenedores,
    g=Gruas,
    l=Localizaciones
)


poner_contenedor_robot = probpl.Operador(
    nombre='poner_contenedor_robot',
    precondiciones=[contenedor_cogido({'{g}': '{c}'}),
                    contenedor_cogido({'{r}': 'ninguno'}),
                    localizacion_robot({'{r}': '{l}'})],
    efectos=[contenedor_cogido({'{g}': 'ninguno'}),
             contenedor_cogido({'{r}': '{c}'}),
             localizacion_contenedor({'{c}': '{l}'})],
    relaciones_rígidas=radio_accion('{g}', '{l}'),
    c1=Contenedores,
    g=Gruas,
    l=Localizaciones,
    r=Robots
)


problema_estibadores = probpl.ProblemaPlanificación(
    operadores=[desplazar_robot_contenedor,
                desplazar_robot,
                coger_contenedor_suelo,
                coger_contenedor_pila,
                coger_contenedor_robot,
                poner_contenedor_suelo,
                poner_contenedor_pila,
                poner_contenedor_robot],
    estado_inicial=probpl.Estado(posicion_contenedor({'c1': 'l1',
                                                      'c2': 'c1',
                                                      'c3': 'l1'}),
                                 localizacion_contenedor({'c1': 'l1',
                                                          'c2': 'l1',
                                                          'c3': 'l1'}),
                                 contenedor_encima({'c1': 'c2',
                                                    'c2': 'c3',
                                                    'c3': 'ninguno'}),
                                 contenedor_cogido({'g1': 'ninguno',
                                                    'g2': 'ninguno'}),
                                 localizacion_robot({'l1': 'l3'})
                                 ),
    objetivos=posicion_contenedor({'c1': 'l3',
                                   'c2': 'c1',
                                   'c3': 'c2'})
)
