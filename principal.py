
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Temporal Patterns                                                          -- #
# -- Codigo: principal.py - secuencia principal de codigo para el proyecto                -- #
# -- Repositorio: https://github.com/IFFranciscoME/Temporal_Patterns                      -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

# Importar Precios historicos M1 del 2019
from datos import df_usdmxn, df_ce
import funciones as fn

# -- -------------------------------------------------------------------- Data generation -- #
# Importar Calendario Economico

# Calcular escenarios para indicadores
df_ce = fn.f_escenario(p0_datos=df_ce)

# -- ------------------------------------------------------ Indicator-Scenario Selection -- #

# -- Calcular las metricas para reacciones del precio, para medir el cambio en la varianza
df_ce = fn.f_metricas(param_ce=df_ce, param_ph=df_usdmxn)

# -- ---------------------------------------------------------- Data exploratory analysis -- #

# -- Statistics of scenario ocurrence

# -- Scenario statistics visualizations

# -- Boxplot for each indicator_scenario metrics values, for all the 4 metrics

# -- Tabla de ocurrencias de escenario para cada indicador
df_indes = fn.f_tabla_ind(param_ce=df_ce)

# -- Seleccionar indicadores y escenarios para pruebas ANOVA
# indicadores con mas de 40 observaciones.
indes_out_1 = df_indes[df_indes['T'] < 40].index
df_indes.drop(indes_out_1, inplace=True)
df_indes.reset_index(inplace=True, drop=True)

# escenarios de cada indicador con mas de 12 observaciones
indes_out_2 = df_indes[(df_indes['A'] < 12) & (df_indes['B'] < 12) &
                       (df_indes['C'] < 12) & (df_indes['D'] < 12)].index
df_indes.drop(indes_out_2, inplace=True)
df_indes.reset_index(inplace=True, drop=True)

# -- ------------------------------------------------------- FUNCION: Tabla Pruebas ANOVA -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- construir la tabla ANOVA

# -- construir tabla de indicador_escenario con los candidatos
param_tab = df_indes
ind = list(set(df_indes['indicador']))
esc = ['A', 'B', 'C', 'D']

# -- seleccionar indicador
df_indes[df_indes['indicador'] == ind[0]]
# -- -- encontrar el escenario donde hay mas de 30 observaciones

# -- eligir aleatoriamente la misma cantidad de observaciones para 3 grupos distintos
# -- Hacer prueba ANOVA a cada indicador_escenario con sus 3 grupos
