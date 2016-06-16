import profile
from time import time  # medir tiempos

import numpy as np

import algoritmos.búsqueda_espacio_estados as búsqee
import estructuraProblema.problema_planificacion_efectos_postivos_negativos as probpl

# Clases de símbolos de objetos
from algoritmos.graphplan import Graphplan

Localizaciones = ['L1', 'L2']
Robots = ['R1']
Gruas = ['G1', 'G2']
Contenedores = ['C1']
Pilas = ['P1', 'P2']
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

localizacion_pila = {'L1': ['P1'], 'L2': ['P2']}
localizaciones_con_pilas = probpl.RelaciónRígida(lambda pila, localizacion:
                                                 pila in localizacion_pila[localizacion])

# Operadores

desplazar_robot = probpl.Operador(
    nombre='desplazar_robot({l1},{l2},{r})',
    precondiciones=[localizacion_robot({'{r}': '{l1}'}),
                    localizacion_ocupada({'{l2}': 'no'}),
                    localizacion_ocupada({'{l1}': 'si'})],
    efectosp=[localizacion_robot({'{r}': '{l2}'}),
              localizacion_ocupada({'{l1}': 'no'}),
              localizacion_ocupada({'{l2}': 'si'})],
    efectosn=[localizacion_robot({'{r}': '{l1}'}),
              localizacion_ocupada({'{l2}': 'no'}),
              localizacion_ocupada({'{l1}': 'si'})],
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
    efectosp=[grua_contenedor_cogido({'{g}': 'ninguno'}),
              robot_cargado_contenedor({'{r}': '{c}'})],
    efectosn=[grua_contenedor_cogido({'{g}': '{c}'}),
              robot_cargado_contenedor({'{r}': 'ninguno'})],
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
    efectosp=[grua_contenedor_cogido({'{g}': '{c}'}),
              robot_cargado_contenedor({'{r}': 'ninguno'})],
    efectosn=[grua_contenedor_cogido({'{g}': 'ninguno'}),
              robot_cargado_contenedor({'{r}': '{c}'})],
    relaciones_rígidas=radio_accion('{g}', '{l}'),
    l=Localizaciones,
    g=Gruas,
    r=Robots,
    c=Contenedores
)

poner_contenedor_en_pila = probpl.Operador(
    nombre='poner_contenedor_en_pila({l},{g},{c1},{c2},{p})',
    precondiciones=[grua_contenedor_cogido({'{g}': '{c1}'}),
                    contenedor_encima_pila({'{p}': '{c2}'}),
                    contenedor_sobre({'{c2}': 'ninguno'}),
                    contenedor_en_pila({'{c1}': 'ninguno'})],
    efectosp=[grua_contenedor_cogido({'{g}': 'ninguno'}),
              contenedor_en_pila({'{c1}': '{p}'}),
              contenedor_encima_pila({'{p}': '{c1}'}),
              contenedor_sobre({'{c2}': '{c1}'})],
    efectosn=[grua_contenedor_cogido({'{g}': '{c1}'}),
              contenedor_encima_pila({'{p}': '{c2}'}),
              contenedor_sobre({'{c2}': 'ninguno'}),
              contenedor_en_pila({'{c1}': 'ninguno'})],
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
                    contenedor_sobre({'{c2}': '{c1}'}),
                    contenedor_en_pila({'{c1}': '{p}'})],
    efectosp=[grua_contenedor_cogido({'{g}': '{c1}'}),
              contenedor_en_pila({'{c1}': 'ninguno'}),
              contenedor_encima_pila({'{p}': '{c2}'}),
              contenedor_sobre({'{c2}': 'ninguno'})],
    efectosn=[grua_contenedor_cogido({'{g}': 'ninguno'}),
              contenedor_encima_pila({'{p}': '{c1}'}),
              contenedor_sobre({'{c2}': '{c1}'}),
              contenedor_en_pila({'{c1}': '{p}'})],
    relaciones_rígidas=[radio_accion('{g}', '{l}'),
                        localizaciones_con_pilas('{p}', '{l}')],
    l=Localizaciones,
    g=Gruas,
    r=Robots,
    c1=Contenedores,
    c2=ContenedoresYPallet,
    p=Pilas
)

contenedor_encima_pila_persistencia = probpl.Operador(
    nombre='contenedor_encima_pila_persistencia({p},{c})',
    precondiciones=[contenedor_encima_pila({'{p}': '{c}'})],
    efectosp=[contenedor_encima_pila({'{p}': '{c}'})],
    efectosn=[],
    c=ContenedoresYPallet,
    p=Pilas
)

contenedor_sobre_persistencia = probpl.Operador(
    nombre='contenedor_sobre_persistencia({cp},{c})',
    precondiciones=[contenedor_sobre({'{cp}': '{c}'})],
    efectosp=[contenedor_sobre({'{cp}': '{c}'})],
    efectosn=[],
    cp=ContenedoresYPallet,
    c=Contenedores
)


contenedor_en_pila_persistencia = probpl.Operador(
    nombre='contenedor_en_pila_persistencia({c},{p})',
    precondiciones=[contenedor_en_pila({'{c}': '{p}'})],
    efectosp=[contenedor_en_pila({'{c}': '{p}'})],
    efectosn=[],
    c=Contenedores,
    p=Pilas
)

localizacion_ocupada_persistencia = probpl.Operador(
    nombre='localizacion_ocupada_persistencia({l},{sn})',
    precondiciones=[localizacion_ocupada({'{l}': '{sn}'})],
    efectosp=[localizacion_ocupada({'{l}': '{sn}'})],
    efectosn=[],
    l=Localizaciones,
    sn={'si', 'no'}
)

localizacion_robot_persistencia = probpl.Operador(
    nombre='localizacion_robot_persistencia({r},{l})',
    precondiciones=[localizacion_robot({'{r}': '{l}'})],
    efectosp=[localizacion_robot({'{r}': '{l}'})],
    efectosn=[],
    r=Robots,
    l=Localizaciones
)

robot_cargado_contenedor_persistencia = probpl.Operador(
    nombre='robot_cargado_contenedor_persistencia({r},{c})',
    precondiciones=[robot_cargado_contenedor({'{r}': '{c}'})],
    efectosp=[robot_cargado_contenedor({'{r}': '{c}'})],
    efectosn=[],
    r=Robots,
    c=Contenedores,
)

grua_contenedor_cogido_persistencia = probpl.Operador(
    nombre='grua_contenedor_cogido_persistencia({g},{c})',
    precondiciones=[grua_contenedor_cogido({'{g}': '{c}'})],
    efectosp=[grua_contenedor_cogido({'{g}': '{c}'})],
    efectosn=[],
    g=Gruas,
    c=Contenedores+['ninguno'],
)

problema_estibadores = probpl.ProblemaPlanificación(
    operadores=[desplazar_robot,
                grua_carga_robot,
                grua_descarga_robot,
                poner_contenedor_en_pila,
                coger_contenedor_pila,
                contenedor_encima_pila_persistencia,
                contenedor_sobre_persistencia,
                contenedor_en_pila_persistencia,
                localizacion_ocupada_persistencia,
                localizacion_robot_persistencia,
                robot_cargado_contenedor_persistencia,
                grua_contenedor_cogido_persistencia],
    estado_inicial=probpl.Estado(localizacion_ocupada({'L1': 'si', 'L2': 'no'}),
                                 localizacion_robot({'R1': 'L1'}),
                                 robot_cargado_contenedor({'R1': 'ninguno'}),
                                 grua_contenedor_cogido({'G1': 'ninguno', 'G2': 'ninguno'}),
                                 contenedor_en_pila({'C1': 'P1'}),
                                 contenedor_sobre({'C1': 'ninguno', 'pallet': 'C1'}),
                                 contenedor_encima_pila({'P1': 'C1', 'P2': 'pallet'})),
    objetivos=contenedor_en_pila({'C1': 'P2'})
)

graphplan = Graphplan(problema_estibadores);
graphplan.graphPlan();
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

profile.run('print(búsqueda_profundidad.buscar(problema_estibadores)); print')
profile.run('print(busqueda_anchura.buscar(problema_estibadores)); print')
profile.run('print(busqueda_optima.buscar(problema_estibadores)); print')

