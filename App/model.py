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
from DISClib.Algorithms.Sorting import mergesort as ms
import datetime

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
        start_station_name = lt.getElement(station_search, 1)["Start Station Name"]
        end_station_name = lt.getElement(station_search, 1)["End Station Name"]
        start_station_id = lt.getElement(station_search, 1)["Start Station Id"]
        end_station_id = lt.getElement(station_search, 1)["End Station Id"]
        if not gr.containsVertex(analyzer["connections"],str(int(start_station_id))+ "-" + start_station_name):
            gr.insertVertex(analyzer["connections"], str(int(start_station_id))+ "-" + start_station_name)
            lt.addLast(vertices, str(int(start_station_id))+ "-" + start_station_name)
        if not gr.containsVertex(analyzer["connections"], str(int(end_station_id))+"-"+end_station_name):
            gr.insertVertex(analyzer["connections"], str(int(end_station_id))+"-"+end_station_name)
            lt.addLast(vertices, str(int(end_station_id))+"-"+end_station_name)
        for station in lt.iterator(station_search):
            suma += int(float(station["Trip  Duration"]))
            A, B = str(int(start_station_id))+ "-" + start_station_name, str(int(end_station_id))+"-"+end_station_name
        promedio = suma/lt.size(station_search)
        gr.addEdge(analyzer["connections"], A, B, promedio)
    return vertices


# Funciones para agregar informacion al catalogo

def addTrips(catalog, trip, station):
    """Esta función adiciona un """
    table = catalog['trip_table']
    existstation = mp.contains(table, station)
    if existstation:
        entry = mp.get(table, station)
        station_search = me.getValue(entry)
    else:
        station_search = lt.newList(datastructure = "ARRAY_LIST")
        mp.put(table, station, station_search)
    lt.addLast(station_search, trip)


def addStations(catalog, station_id, station_name, time, usertype, startStation): 
    """Esta función adiciona una estación a la tabla de hash de estaciones """
    table = catalog['stations_table']
    existstation = mp.contains(table, str(int(station_id)) + "-" + station_name)

    if not existstation:
        info ={"station_id": station_id, "station_name": station_name,"datetime_start": {}, 
        "datetime_end": {}, "nAnnual": 0, "nCasual": 0, "nTripsEnd":0, "nTripsStart": 0}
    else:
        info = me.getValue(mp.get(table, str(int(station_id)) + "-" + station_name))

    if startStation:
        if usertype == "Casual Member":
            info["nCasual"] += 1
        elif usertype == "Annual Member":
            info["nAnnual"] += 1
        info["datetime_start"][time] = info["datetime_start"].get(time, 0) + 1
        info["nTripsStart"] += 1
       
    else:
        info["datetime_end"][time] = info["datetime_end"].get(time, 0) + 1
        info["nTripsEnd"] += 1
        
    mp.put(table, str(int(station_id)) + "-" + station_name, info)


# Funciones para creacion de datos

# Funciones de consulta

def totalStops(analyzer):
    """Retorna el total de estaciones (vertices) del grafo """
    return gr.numVertices(analyzer['connections'])

def totalConnections(analyzer):
    """Retorna el total arcos del grafo"""
    return gr.numEdges(analyzer['connections'])

def indegree(analyzer, vertex):
    return gr.indegree(analyzer["connections"], vertex)

def outdegree(analyzer, vertex):
    return gr.outdegree(analyzer["connections"], vertex)

def more_trips_datetime(dict):
    """Esta función retorna la fecha_hora con mayor frecuencia de viajes"""
    max = 0
    max_datetime = ""
    for DATETIME in dict:
        if dict[DATETIME] > max:
            max_datetime = DATETIME
            max = dict[DATETIME]
    return max_datetime

# Requerimiento 1
def Top5estaciones_mas_viajes(analyzer):
    lista_estaciones = lt.newList(datastructure = "ARRAY_LIST")
    lista_vertices = gr.vertices(analyzer["connections"])
    for station_name in lt.iterator(lista_vertices):
        
        existstation = mp.contains(analyzer['stations_table'], station_name)
        if existstation:
            info = me.getValue(mp.get(analyzer['stations_table'], station_name))

        info["station_name"] = station_name
        info["outdegree"] = outdegree(analyzer, station_name)
        info["more_trips_datetime"] = more_trips_datetime(info["datetime_start"])
        lt.addLast(lista_estaciones, info)

    sorted_list = ms.sort(lista_estaciones, cmpOutDegree)
    Top5Estaciones = lt.subList(sorted_list, 1, 5)
    return Top5Estaciones


def cmpOutDegree(estacion1, estacion2):
    """Devuelve verdadero (True) si el outdegree de estacion1 es mayor que el de estacion2"""
    return estacion1["outdegree"] > estacion2["outdegree"]


# Requerimiento 2
def possibleRoutes(analyzer, vertex, time, minstations, maxroutes):
    minCost = djk.Dijkstra(analyzer["connections"], vertex)
    vertices = gr.vertices(analyzer["connections"])
    recorridos = lt.newList("ARRAY_LIST")
    nRoutes = 1
    for vertex in lt.iterator(vertices):
        pila = djk.pathTo(minCost, vertex)
        if pila != None:
            totaltime = 0
            size = lt.size(pila)
            for dic in lt.iterator(pila):
                totaltime += dic["weight"]
            if time >= totaltime*2 and minstations <= size and nRoutes <= maxroutes:
                lt.addLast(recorridos, pila)
                nRoutes += 1
    return recorridos 
            


# Requerimiento 3 
def kosarajuTable(analyzer, componentes):
    estaciones = mp.keySet(componentes["idscc"])
    analyzer['kosaraju_table'] = mp.newMap(562000, maptype='PROBING', loadfactor=0.5)
    for estacion in lt.iterator(estaciones):
        entry = mp.get(componentes["idscc"], estacion)
        component = me.getValue(entry)
        existcomponent = mp.contains(analyzer['kosaraju_table'], component)
        if existcomponent:
            entry2 = mp.get(analyzer['kosaraju_table'], component)
            component_search = me.getValue(entry2)
        else:
            component_search = lt.newList(datastructure = "ARRAY_LIST")
            mp.put(analyzer['kosaraju_table'], component, component_search)
        lt.addLast(component_search, estacion)

def connectedComponents(analyzer):
    componentes = scc.KosarajuSCC(analyzer["connections"])
    kosarajuTable(analyzer, componentes)
    table = analyzer["kosaraju_table"]
    nComponentes = scc.KosarajuSCC(analyzer["connections"])["components"]
    tableStations = analyzer["stations_table"]
    lista = lt.newList("ARRAY_LIST")

    for i in range (1, nComponentes+1):
        maxStart = 0
        maxEnd = 0
        entry = mp.get(table, i)
        stationList = me.getValue(entry)
        for station in lt.iterator(stationList):
            entry2 = mp.get(tableStations, station)
            stat = me.getValue(entry2)
            if  stat["nTripsStart"] >= maxStart:
                maxStart = stat["nTripsStart"]
                maxStartStation = station
            if  stat["nTripsEnd"] >= maxEnd:
                maxEnd = stat["nTripsEnd"]
                maxEndStation = station
        dic = {"component": i, "maxStart": maxStartStation, "maxEnd": maxEndStation, "size": lt.size(stationList)}
        lt.addLast(lista, dic)
    sorted_list = ms.sort(lista, compareSCCsize)
    return nComponentes, sorted_list

# Requerimiento 4
def minTime(analyzer, startStation, endStation):
    minCost = djk.Dijkstra(analyzer["connections"], startStation)
    pila = djk.pathTo(minCost, endStation)
    tiempoTotal = 0
    for dic in lt.iterator(pila):
        tiempoTotal+= dic["weight"]
    nStops = lt.size(pila) + 1
    nRoutes = lt.size(pila) 
    return tiempoTotal, nStops, nRoutes, pila 


# Funciones utilizadas para comparar elementos dentro de una lista

def compareSCCsize(comp1, comp2):
    return comp1["size"] > comp2["size"]

        