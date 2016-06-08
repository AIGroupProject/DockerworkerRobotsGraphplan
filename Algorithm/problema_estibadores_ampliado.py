import random
import Algorithm.problema_planificación as probpl
import Algorithm.búsqueda_espacio_estados as búsqee
import numpy as np
from time import time  # medir tiempos
import profile

# Clases de símbolos de objetos
Localizaciones = ['L1', 'L2']
Robots = ['R1']
Gruas = ['G1', 'G2']
Contenedores = ['C1','C2']
Pilas = ['P1', 'P2', 'P3']
ContenedoresYPallet = Contenedores + ['pallet']

# Variables de estado

localizacion_ocupada = probpl.VariableDeEstados(
    nombre='localizacion_ocupada({l})',
    l=Localizaciones
)

localizacion_robot = probpl.VariableDeEstados(
    nombre='localizacion_robot({r})',
    r=Robots
)

robot_cargado_contenedor = probpl.VariableDeEstados(
    nombre='robot_cargado_contenedor({r})',
    r=Robots
)

grua_contenedor_cogido = probpl.VariableDeEstados(
    nombre='grua_contenedor_cogido({g})',
    g=Gruas
)

contenedor_en_pila = probpl.VariableDeEstados(
    nombre='contenedor_en_pila({c})',
    c=Contenedores
)

contenedor_sobre = probpl.VariableDeEstados(
    nombre='contenedor_sobre({c})',
    c=ContenedoresYPallet
)

contenedor_encima_pila = probpl.VariableDeEstados(
    nombre='contenedor_encima_pila({p})',
    p=Pilas
)

# Ejemplo impresion de Variable de Estado
# print(contenedor_encima({'c1': 'ninguno'}))

## Esto se puede sacar a una clase que contruya una matriz
## tal como se hace aqui, con sus get y set
traceabilityMatrix = np.zeros((len(Localizaciones), len(Localizaciones)), dtype='bool')
# l1 adyacente l2
traceabilityMatrix[0][1] = True

matrizTrazSimet = (traceabilityMatrix + traceabilityMatrix.T)

# Relaciones rígidas
adyacente = probpl.RelaciónRígida(lambda x, y:
                                  matrizTrazSimet[
                                      Localizaciones.index(x),
                                      Localizaciones.index(y)])
radio = {'G1': ['L1'], 'G2': ['L2']}
radio_accion = probpl.RelaciónRígida(lambda grua, localizacion:
                                     localizacion in radio[grua])

contenedor_encima_si_mismo = probpl.RelaciónRígida(lambda c1, c2:
                                                   c1 != c2)

localizacion_pila = {'L1': ['P1','P3'], 'L2': ['P2']}
localizaciones_con_pilas = probpl.RelaciónRígida(lambda pila, localizacion:
                                                 pila in localizacion_pila[localizacion])

# Operadores

desplazar_robot = probpl.Operador(
    nombre='desplazar_robot({l1},{l2},{r})',
    precondiciones=[localizacion_robot({'{r}': '{l1}'}),
                    localizacion_ocupada({'{l2}': 'no'})],
    efectos=[localizacion_robot({'{r}': '{l2}'}),
             localizacion_ocupada({'{l1}': 'no'}),
             localizacion_ocupada({'{l2}': 'si'})],
    relaciones_rígidas=adyacente('{l1}', '{l2}'),
    l1=Localizaciones,
    l2=Localizaciones,
    r=Robots
)

grua_carga_robot = probpl.Operador(
    nombre='grua_carga_robot({l},{g},{r},{c})',
    precondiciones=[grua_contenedor_cogido({'{g}': '{c}'}),
                    localizacion_robot({'{r}': '{l}'}),
                    robot_cargado_contenedor({'{r}': 'ninguno'})],
    efectos=[grua_contenedor_cogido({'{g}': 'ninguno'}),
             robot_cargado_contenedor({'{r}': '{c}'})],
    relaciones_rígidas=radio_accion('{g}', '{l}'),
    l=Localizaciones,
    g=Gruas,
    r=Robots,
    c=Contenedores
)

grua_descarga_robot = probpl.Operador(
    nombre='grua_descarga_robot({l},{g},{r},{c})',
    precondiciones=[grua_contenedor_cogido({'{g}': 'ninguno'}),
                    localizacion_robot({'{r}': '{l}'}),
                    robot_cargado_contenedor({'{r}': '{c}'})],
    efectos=[grua_contenedor_cogido({'{g}': '{c}'}),
             robot_cargado_contenedor({'{r}': 'ninguno'})],
    relaciones_rígidas=radio_accion('{g}', '{l}'),
    l=Localizaciones,
    g=Gruas,
    r=Robots,
    c=Contenedores
)

poner_contenedor_en_pila = probpl.Operador(
    nombre='poner_contenedor_en_pila({l},{g},{c1},{c2},{p})',
    precondiciones=[grua_contenedor_cogido({'{g}': '{c1}'}),
                    contenedor_encima_pila({'{p}': '{c2}'})],
    efectos=[grua_contenedor_cogido({'{g}': 'ninguno'}),
             contenedor_en_pila({'{c1}': '{p}'}),
             contenedor_encima_pila({'{p}': '{c1}'}),
             contenedor_sobre({'{c2}': '{c1}'})],
    relaciones_rígidas=[radio_accion('{g}', '{l}'),
                        localizaciones_con_pilas('{p}', '{l}')],
    l=Localizaciones,
    g=Gruas,
    r=Robots,
    c1=Contenedores,
    c2=ContenedoresYPallet,
    p=Pilas
)

coger_contenedor_pila = probpl.Operador(
    nombre='coger_contenedor_pila({l},{g},{c1},{c2},{p})',
    precondiciones=[grua_contenedor_cogido({'{g}': 'ninguno'}),
                    contenedor_encima_pila({'{p}': '{c1}'}),
                    contenedor_sobre({'{c2}': '{c1}'})],
    efectos=[grua_contenedor_cogido({'{g}': '{c1}'}),
             contenedor_en_pila({'{c1}': 'ninguno'}),
             contenedor_encima_pila({'{p}': '{c2}'}),
             contenedor_sobre({'{c2}': 'ninguno'})],
    relaciones_rígidas=[radio_accion('{g}', '{l}'),
                        localizaciones_con_pilas('{p}', '{l}')],
    l=Localizaciones,
    g=Gruas,
    r=Robots,
    c1=Contenedores,
    c2=ContenedoresYPallet,
    p=Pilas
)

problema_estibadores = probpl.ProblemaPlanificación(
    operadores=[desplazar_robot,
                grua_carga_robot,
                grua_descarga_robot,
                poner_contenedor_en_pila,
                coger_contenedor_pila],
    estado_inicial=probpl.Estado(localizacion_ocupada({'L1': 'si', 'L2': 'no'}),
                                 localizacion_robot({'R1': 'L1'}),
                                 robot_cargado_contenedor({'R1': 'ninguno'}),
                                 grua_contenedor_cogido({'G1': 'ninguno', 'G2': 'ninguno'}),
                                 contenedor_en_pila({'C1': 'P1', 'C2': 'P1'}),
                                 contenedor_sobre({'C1': 'C2', 'pallet': 'C1', 'C2': 'ninguno'}),
                                 contenedor_encima_pila({'P1': 'C2', 'P2': 'pallet', 'P3': 'pallet'})),
    objetivos=contenedor_en_pila({'C1': 'P2','C2': 'P2'})
)

búsqueda_profundidad = búsqee.BúsquedaEnProfundidad()
busqueda_anchura = búsqee.BúsquedaEnAnchura()
busqueda_optima = búsqee.BúsquedaÓptima()
# busqueda_primero_el_mejor = búsqee.BúsquedaPrimeroElMejor()

tiempo_inicial = time()
búsqueda_profundidad.buscar(problema_estibadores)
tiempo_final = time()
print('Tiempo del algoritmo', tiempo_final-tiempo_inicial)

tiempo_inicial = time()
busqueda_anchura.buscar(problema_estibadores)
tiempo_final = time()
print('Tiempo del algoritmo', tiempo_final-tiempo_inicial)

tiempo_inicial = time()
busqueda_optima.buscar(problema_estibadores)
tiempo_final = time()
print('Tiempo del algoritmo', tiempo_final-tiempo_inicial)


# tiempo_inicial = time()
# busqueda_primero_el_mejor.buscar(problema_estibadores)
# tiempo_final = time()
# print('Tiempo del algoritmo', tiempo_final-tiempo_inicial)

print(búsqueda_profundidad.buscar(problema_estibadores))
print(busqueda_anchura.buscar(problema_estibadores))
print(busqueda_optima.buscar(problema_estibadores))

#profile.run('print(búsqueda_profundidad.buscar(problema_estibadores)); print')
#profile.run('print(busqueda_anchura.buscar(problema_estibadores)); print')
#profile.run('print(busqueda_optima.buscar(problema_estibadores)); print')

