
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: principal.py - secuencia principal de codigo para el proyecto                -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

from datos import df_usdmxn, df_ce
import funciones as fn
import time
import numpy as np
import mass_ts as mass

# -- ----------------------------------------------------------------------- FUNCTION : 1 -- #
# -- Calcular escenarios para indicadores
s_f1 = time.time()
df_ce = fn.f_escenario(p0_datos=df_ce)
e_f1 = time.time()
time_f1 = round(e_f1 - s_f1, 4)
print('f_escenario se tardo: ' + str(time_f1))

# -- ----------------------------------------------------------------------- FUNCTION : 2 -- #
# -- Calcular las metricas para reacciones del precio
s_f2 = time.time()
df_ce = fn.f_metricas(param_ce=df_ce, param_ph=df_usdmxn)
e_f2 = time.time()
time_f2 = round(e_f2 - s_f2, 4)
print('f_metricas se tardo: ' + str(time_f2))

# -- ---------------------------------------------------------- Data exploratory analysis -- #

# -- Statistics of scenario ocurrence

# -- Scenario statistics visualizations

# -- Boxplot for each indicator_scenario metrics values, for all the 4 metrics

# -- ----------------------------------------------------------------------- FUNCTION : 3 -- #
# -- Tabla de ocurrencias de escenario para cada indicador
s_f3 = time.time()
df_ind_1 = fn.f_tabla_ind(param_ce=df_ce)
e_f3 = time.time()
time_f3 = round(e_f3 - s_f3, 2)
print('f_tabla_ind se tardo: ' + str(time_f3))

# -- ----------------------------------------------------------------------- FUNCTION : 4 -- #
# -- Seleccionar indicadores y escenarios con observaciones suficientes
s_f4 = time.time()
df_ind_2 = fn.f_seleccion_ind(param_ce=df_ind_1, param_c1=60, param_c2=25)
e_f4 = time.time()
time_f4 = round(e_f4 - s_f4, 2)
print('f_seleccion_ind se tardo: ' + str(time_f4))

# -- ----------------------------------------------------------------------- FUNCTION : 5 -- #
# -- Construir tabla de anova para seleccionar escenarios candidatos
s_f5 = time.time()
df_ind_3 = fn.f_anova(param_data1=df_ind_2, param_data2=df_ce)
e_f5 = time.time()
time_f5 = round(e_f5 - s_f5, 2)
print('f_anova se tardo: ' + str(time_f3))

# -- ----------------------------------------------------------------------- FUNCTION : 6 -- #
# -- Busqueda hacia adelante de patrones

# Para cada indicador, para cada escenario, empezar desde la 1era ocurrencia y buscar
# hacia adelante:
# -- En los mismos indicadores y mismos escenarios
# -- En los mismos indicadores en diferentes escenarios
# -- En otros indicadores
# -- En todas las demas ventanas de precios

procesos = len(df_ind_3.iloc[:, 1])


def f_busqueda_adelante(param_row, param_ca_data=df_ind_3, param_ce_data=df_ce):
    """
    Parameters
    ----------
    param_row :
    param_ce_data
    param_ca_data :

    Returns
    -------

    Debugging
    ---------
    param_row = 0
    param_ca_data = df_ind_3
    param_ce_data = df_ce
    param_p_ventana = 30

    """

    # renglon con informacion de escenario candidato
    candidate_data = param_ca_data.iloc[param_row, :]

    # primera ocurrencia de escenario candidato
    ancla = param_ce_data[(param_ce_data['esc'] == candidate_data['esc']) &
                          (param_ce_data['name'] == candidate_data['name'])].iloc[param_row, :]

    # fecha de ancla
    fecha_ini = ancla['timestamp']

    # se toma el timestamp de precios igual a timestamp del primer escenario del indicador
    ind_ini = df_usdmxn[df_usdmxn['timestamp'] == fecha_ini].index
    # fecha final es la fecha inicial mas un tamaño de ventana arbitrario
    ind_fin = ind_ini + param_p_ventana
    # se construye la serie query
    serie_q = df_usdmxn.iloc[ind_ini[0]:ind_fin[0], :]
    # se toma el close
    serie_q = np.array(serie_q['close'])
    # se normaliza para tener todos entre 0 y 1
    serie_q = serie_q / max(serie_q)

    # se construye la serie completa para busqueda (un array de numpy de 1 dimension)
    serie = np.array(df_usdmxn['close'])[7:]
    serie = serie / max(serie)

    # -- parametros del algoritmo -- #
    # tamaño de ventana para iterar la busqueda = tamaño de query
    batch_size = param_p_ventana * 1
    # regresar los Top X casos que "mas parecidos" = Cantidad total de ocurrencias de indicador
    top_matches = 5
    # regresar los indices y las distancias
    mass_indices, mass_dists = mass.mass2_batch(serie, serie_q, batch_size=batch_size,
                                                top_matches=top_matches, n_jobs=4)

    return 1
