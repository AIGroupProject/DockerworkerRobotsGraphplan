import algoritmos.búsqueda_espacio_estados as búsqee

from time import time  # medir tiempos


def imprimir(problema_estibadores, busqueda_profundidad, busqueda_primero_el_mejor=None):

    if busqueda_profundidad is not None:
        print("\n")
        tiempo_inicial = time()
        b_prof = busqueda_profundidad.buscar(problema_estibadores)
        tiempo_final = time()
        print("Longitud de la solución: ", len(b_prof))
        print('Tiempo del algoritmo profundidad', tiempo_final - tiempo_inicial)
        print(b_prof)

    # if busqueda_anchura is not None:
    #     print("\n")
    #     tiempo_inicial = time()
    #     b_anch = busqueda_anchura.buscar(problema_estibadores)
    #     tiempo_final = time()
    #     print("Longitud de la solución: ", len(b_prof))
    #     print(b_anch)
    #     print('Tiempo del algoritmo anchura', tiempo_final - tiempo_inicial)
    #
    # if busqueda_optima is not None:
    #     print("\n")
    #     tiempo_inicial = time()
    #     b_opt = busqueda_optima.buscar(problema_estibadores)
    #     tiempo_final = time()
    #     print("Longitud de la solución: ", len(b_opt))
    #     print(b_opt)
    #     print('Tiempo del algoritmo busqueda optima', tiempo_final - tiempo_inicial)

    if busqueda_primero_el_mejor is not None:
        print("\n")
        tiempo_inicial = time()
        b_prim = busqueda_primero_el_mejor.buscar(problema_estibadores)
        tiempo_final = time()
        print("Longitud de la solución: ", len(b_prim))
        print(b_prim)
        print('Tiempo del algoritmo primer el mejor ', tiempo_final - tiempo_inicial)
        print("\n")
