import random
import Algorithm.problema_planificación as probpl
import numpy as np

# Clases de símbolos de objetos
Localizaciones = ['l1', 'l2', 'l3']
Robots = ['r1', 'r2']
Gruas = ['g1', 'g2']
Contenedores = ['c1', 'c2', 'c3']

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
    b=Contenedores
)

localizacion_contenedor = probpl.VariableDeEstados(
    nombre='localizacion_contenedor({b})',
    b=Robots
)

## Esto se puede sacar a una clase que contruya una matriz
## tal como se hace aqui, con sus get y set
traceabilityMatrix = np.zeros((len(Localizaciones), len(Localizaciones)), dtype='bool')
#l1 adyacente l2
traceabilityMatrix[0][1] = True
#l2 adyacente l3
traceabilityMatrix[1][2] = True

matrizTrazSimet = (traceabilityMatrix+traceabilityMatrix.T)

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
print('¿Existe relacion de adyacencia?', adyacente_fun('l1','l3'))


radio = {'g1': ['l1','l2'],'g2':['l3']}

radio_accion = probpl.RelaciónRígida(lambda grua, localizacion:
                                     localizacion in radio[grua])

##Prueba de la función lambda
radio_fun = lambda grua, localizacion: localizacion in radio[grua]

print('¿Esta en el radio de accion?', radio_fun('g1','l3'))


# Operadores
