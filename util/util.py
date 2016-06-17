from util.accion import Accion

def extraer_acciones(problema_estibadores):
    lista_acciones = []
    ## SACA DE TODAS LAS ACCIONES LAS PRECONDICIONES QUE DESPUES SERAN ATOMOS, EFECTOSP Y EFECTOSN
    for accion in problema_estibadores.acciones:

        lista_pre = []
        lista_pre_modificada = []
        lista_pre_final = []
        lista_efectos_pos = []
        lista_efectos_pos_modificada = []
        lista_efectos_pos_final = []
        lista_efectos_neg = []
        lista_efectos_neg_modificada = []
        lista_efectos_neg_final = []

        for precond in accion.precondiciones:
            lista_pre.append(str(precond))
        for efecp in accion.efectosp:
            lista_efectos_pos.append(str(efecp))
        for efecn in accion.efectosn:
            lista_efectos_neg.append(str(efecn))

        for precondicion in lista_pre:
            lista_pre_modificada += precondicion.split("\n")
        for efecp in lista_efectos_pos:
            lista_efectos_pos_modificada += efecp.split("\n")
        for efecn in lista_efectos_neg:
            lista_efectos_neg_modificada += efecn.split("\n")

        for x in lista_pre_modificada:
            if "No definido" not in x:
                lista_pre_final.append(x)

        for x in lista_efectos_pos_modificada:
            if "No definido" not in x:
                lista_efectos_pos_final.append(x)

        for x in lista_efectos_neg_modificada:
            if "No definido" not in x:
                lista_efectos_neg_final.append(x)

        lista_acciones.append(Accion(accion.nombre,lista_pre_final, lista_efectos_pos_final, lista_efectos_neg_final))


    # print(lista_acciones)

    return lista_acciones





def extraer_estado_inicial (problema_estibadores):
    ###SACA DEL ESTADO INICIAL LOS ATOMOS
    lista_inicial = []
    lista_estado_inicial = []
    lista_final = []
    for x in problema_estibadores.estado_inicial.variables_estados:
        lista_inicial.append(str(problema_estibadores.estado_inicial.variables_estados[x]))

    for x in lista_inicial:
        lista_estado_inicial += x.split("\n")


    return lista_estado_inicial


def extraer_objetivo(problema_estibadores):
    lista_obj = []
    lista_obj_modificada = []
    lista_obj_final = []

    for objetivo in problema_estibadores.objetivos:
        lista_obj.append(str(objetivo))
    for obj in lista_obj:
        lista_obj_modificada += obj.split("\n")
    for x in lista_obj_modificada:
        if "No definido" not in x:
            lista_obj_final.append(x)

    return lista_obj_final

