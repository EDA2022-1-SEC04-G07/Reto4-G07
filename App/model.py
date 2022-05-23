"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dfo
from DISClib.Utils import error as error

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
            'connections': None,
            'trip_table': None,
            'stations_table': None
        }

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000)
        analyzer['trip_table'] = mp.newMap(562000,
                                   maptype='PROBING',
                                   loadfactor=0.5)
        analyzer['stations_table'] = mp.newMap(562000,
                                   maptype='PROBING',
                                   loadfactor=0.5)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafo

def addGraph(analyzer):
    llaves = mp.keySet(analyzer["trip_table"])
    vertices = lt.newList("SINGLE_LINKED")
    for key in lt.iterator(llaves):
        suma = 0
        entry = mp.get(analyzer["trip_table"], key)
        station_search = me.getValue(entry)
        if not (gr.containsVertex(analyzer["connections"], lt.getElement(station_search, 1)["Start Station Name"])):
            gr.insertVertex(analyzer["connections"], lt.getElement(station_search, 1)["Start Station Name"])
            lt.addLast(vertices, lt.getElement(station_search, 1)["Start Station Name"])
        if not (gr.containsVertex(analyzer["connections"], lt.getElement(station_search, 1)["End Station Name"])):
            gr.insertVertex(analyzer["connections"], lt.getElement(station_search, 1)["End Station Name"])
            lt.addLast(vertices, lt.getElement(station_search, 1)["End Station Name"])
        for station in lt.iterator(station_search):
            suma += int(float(station["Trip  Duration"]))
            A, B = station["Start Station Name"], station["End Station Name"]
        promedio = suma/lt.size(station_search)
        gr.addEdge(analyzer["connections"], A, B, promedio)
    return vertices


# Funciones para agregar informacion al catalogo

def addTrips(catalog, trip, station):
    """Esta función adiciona un track a la lista de tracks de un artista"""
    table = catalog['trip_table']
    existstation = mp.contains(table, station)
    if existstation:
        entry = mp.get(table, station)
        station_search = me.getValue(entry)
    else:
        station_search = lt.newList(datastructure = "ARRAY_LIST")
        mp.put(table, station, station_search)
    lt.addLast(station_search, trip)

def addStations(catalog, trip, station):
    """Esta función adiciona un track a la lista de tracks de un artista"""
    table = catalog['stations_table']
    existstation = mp.contains(table, station)
    if not existstation:
        mp.put(table, station, trip)
    

# Funciones para creacion de datos

# Funciones de consulta

def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])

def indegree(analyzer, vertex):
    return gr.indegree(analyzer["connections"], vertex)

def outdegree(analyzer, vertex):
    return gr.outdegree(analyzer["connections"], vertex)

# Requerimiento 2
def possibleRoutes(analyzer, vertex, time, minstations, maxroutes):
    recorridos = dfs.DepthFirstSearch(analyzer["connections"], vertex)
    lista = (mp.keySet(recorridos["visited"]))
    lista2 = (mp.valueSet(recorridos["visited"]))
    for i in range(1, lt.size(lista)+1):
        print(lt.getElement(lista, i))
        print(lt.getElement(lista2, i))


# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def mas_viajes_estaciones(analyzer):
    mayor = 0
    mayor_vertice = None
    lista_vertices = gr.vertices(analyzer["connections"])
    for vertex in lt.iterator(lista_vertices):
        degree = outdegree(analyzer, vertex) + indegree(analyzer, vertex)
        if mayor < degree:
            mayor = degree
            mayor_vertice = vertex

        