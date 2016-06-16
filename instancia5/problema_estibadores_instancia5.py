from time import time  # medir tiempos

import numpy as np

import algoritmos.búsqueda_espacio_estados as búsqee
import estructuraProblema.problema_planificación as probpl
import util.imprimir_algoritmos as imp

# Clases de símbolos de objetos
Localizaciones = ['L1', 'L2', 'L3', 'L4']
Robots = ['R1', 'R2']
Gruas = ['G1', 'G2']
Contenedores = ['C1', 'C2', 'C3', 'C4']
Pilas = ['P1', 'P2', 'P3', 'P4']
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
traceabilityMatrix[0][2] = True
traceabilityMatrix[1][3] = True

matrizTrazSimet = (traceabilityMatrix + traceabilityMatrix.T)

# Relaciones rígidas
adyacente = probpl.RelaciónRígida(lambda x, y:
                                  matrizTrazSimet[
                                      Localizaciones.index(x),
                                      Localizaciones.index(y)])
radio = {'G1': ['L1','L3'], 'G2': ['L2','L4']}
radio_accion = probpl.RelaciónRígida(lambda grua, localizacion:
                                     localizacion in radio[grua])

contenedor_encima_si_mismo = probpl.RelaciónRígida(lambda c1, c2:
                                                   c1 != c2)

localizacion_pila = {'L1': ['P1', 'P2'], 'L2': ['P3'], 'L3': ['P4'], 'L4': []}
localizaciones_con_pilas = probpl.RelaciónRígida(lambda pila, localizacion:
                                                 pila in localizacion_pila[localizacion])


# HEURISTICAS
def heu1_problema_estibadores_ampliado(nodo):
    heu = nodo.estado.variables_estados['contenedor_en_pila({c})']
    penalizacion = 0

    # penalizamos las variables de estado que no cumplen con el objetivo
    if heu['C1'] != 'P2':
        penalizacion +=1
    if heu['C2'] != 'P2':
        penalizacion += 1
    return penalizacion



# def heu2_problema_estibadores_ampliado(nodo):
#     heu = nodo.estado.variables_estados['contenedor_en_pila({c})']
#     penalizacion = 0
#
#     # penalizamos las variables de estado que no cumplen con el objetivo
#     if heu['C1'] != 'P2':
#         penalizacion += 1
#     if heu['C2'] != 'P2':
#         penalizacion += 1
#     return penalizacion

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
    estado_inicial=probpl.Estado(localizacion_ocupada({'L1': 'si', 'L2': 'si', 'L3': 'no', 'L4': 'no'}),
                                 localizacion_robot({'R1': 'L1', 'R2': 'L2'}),
                                 robot_cargado_contenedor({'R1': 'ninguno', 'R2': 'ninguno'}),
                                 grua_contenedor_cogido({'G1': 'ninguno', 'G2': 'ninguno'}),
                                 contenedor_en_pila({'C1': 'P1', 'C2': 'P1', 'C3': 'P1', 'C4':'P1'}),
                                 contenedor_sobre({'pallet': 'C1', 'C1': 'C2', 'C2': 'C3', 'C3': 'C4','C4':'ninguno'}),
                                 contenedor_encima_pila({'P1': 'C4', 'P2': 'pallet', 'P3': 'pallet', 'P4': 'pallet'})),
    objetivos=contenedor_en_pila({'C1': 'P2', 'C2': 'P2', 'C3': 'P3', 'C4': 'P1'})
)

busqueda_profundidad = búsqee.BúsquedaEnProfundidad()
busqueda_anchura = búsqee.BúsquedaEnAnchura()
busqueda_optima = búsqee.BúsquedaÓptima()
busqueda_primero_el_mejor = búsqee.BúsquedaPrimeroElMejor(heu1_problema_estibadores_ampliado)

#Calcula tiempos, nodos analizados e imprime solucion
imp.imprimir(problema_estibadores, busqueda_profundidad, busqueda_primero_el_mejor)
