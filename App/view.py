"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
import pandas as pd
import tabulate

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información en el catálogo")
    print("3- Comprar bicicletas para las estaciones con más viajes de origen")
    print("4- Planear paseos turísticos por la ciudad")
    print("5- Reconocer los componentes fuertemente conectados del sistema")
    print("6- Planear una ruta rápida para el usuario")
    print("7- Reportar rutas en un rango de fechas para los usuarios anuales")
    print("8- Planear el mantenimiento preventivo de bicicletas")
    print("9- La estación más frecuentada por los visitantes")

catalog = None

def optiontwo(analyzer, vertices):
    tabla = analyzer["stations_table"]
    lista = [["Station Name", "Station Id", "Indegree", "Outdegree"]]

    for index in range(1,6):
        vertex = lt.getElement(vertices, index)
        indegree = controller.indegree(analyzer["connections"], vertex)
        outdegree = controller.outdegree(analyzer["connections"], vertex)
        entry = mp.get(tabla, vertex)
        stationid = me.getValue(entry)["station_id"]
        stationname = me.getValue(entry)["station_name"]
        if stationname == "":
            stationname = "Unknown"
        lista2 = [stationname, str(stationid), str(indegree), str(outdegree)]        
        s = pd.Series(lista2).str.wrap(20)
        lista.append(s)

    for index in range(lt.size(vertices)-4, lt.size(vertices)+1):
        vertex = lt.getElement(vertices, index)
        indegree = controller.indegree(analyzer["connections"], vertex)
        outdegree = controller.outdegree(analyzer["connections"], vertex)
        entry = mp.get(tabla, vertex)
        stationid = me.getValue(entry)["station_id"]
        stationname = me.getValue(entry)["station_name"]
        if stationname == "":
            stationname = "Unknown"
        lista2 = [stationname, str(stationid), str(indegree), str(outdegree)]         
        s = pd.Series(lista2).str.wrap(20)
        lista.append(s)
    print("Los primeros y últimos 5 vértices registrados en el grafo son: ")
    print(tabulate.tabulate(lista,  tablefmt = "grid"))

#Requerimiento 1       
def printTop5Estaciones_mas_viajes(Top5Estaciones):
    tabla = [["Station Id", "Station Name", "Out Trips", "Suscriber Out Trips", "Tourist Out Trips", "Out Degree(Routes)", "Rush hour", "Rush date"]]
    for index in range(1,6):
        info= lt.getElement(Top5Estaciones, index)
        linea = [info["station_id"], info["station_name"], str(info["nTripsStart"]),  str(info["nSuscriber"]), str(info["nTourist"]), str(info["outdegree"]), info["start_rush_hour"], info["start_rush_date"]]   
        s = pd.Series(linea).str.wrap(20)
        tabla.append(s)
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))

#Requerimiento 2
def printPossibleRoutes(recorridos):
    tabla = [["Stop stations", "Route time [s]", "Roundtrip time [s]", "Station IDs", "Station Names"]]
    
    for y in range(1, 4):
        route = lt.getElement(recorridos, y)
        total_time = 0
        size = lt.size(route)
        stationsname, stationsid = "", ""
        for x in range(lt.size(route), 0, -1):
            dic = lt.getElement(route, x)
            total_time += dic["weight"]
            name = dic["vertexA"][5:]
            if name == "":
                name = "Unknown"
            stationsname += name + " -> "
            stationsid += dic["vertexA"][:4] + " -> "
        linea = [str(size), str(total_time), str(total_time*2), stationsid[:-3], stationsname[:-3]]
        s = pd.Series(linea).str.wrap(20)
        tabla.append(s)
    
    for y in range(lt.size(recorridos)-2, lt.size(recorridos)+1):
        route = lt.getElement(recorridos, y)
        total_time = 0
        size = lt.size(route)
        stationsname, stationsid = "", ""
        for x in range(lt.size(route), 0, -1):
            dic = lt.getElement(route, x)
            total_time += dic["weight"]
            name = dic["vertexA"][5:]
            if name == "":
                name = "Unknown"
            stationsname += name + " -> "
            stationsid += dic["vertexA"][:4] + " -> "
        linea = [str(size), str(total_time), str(total_time*2), stationsid[:-3], stationsname[:-4]]
        s = pd.Series(linea).str.wrap(20)
        tabla.append(s)
    
    print("The first 3 and last 3 possible rputes are: ")
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))


#Requerimiento 3      
def printConnectedComponents(list):
    tabla = [["SSC size", "Max out station ID", "Max out station name", "Max in station ID", "Max in station name"]]
    for i in range(1,4):
        dic = lt.getElement(list, i)
        startName = dic["maxStart"][5:]
        endName = dic["maxEnd"][5:]
        if startName == "":
            startName = "Unknown"
        if endName == "":
            endName = "Unknown"
        linea = [str(dic["size"]), dic["maxStart"][:4], startName, dic["maxEnd"][:4], endName]   
        s = pd.Series(linea).str.wrap(20)
        tabla.append(s)
    for i in range(lt.size(list)-2,lt.size(list)+1):
        dic = lt.getElement(list, i)
        linea = [str(dic["size"]), dic["maxStart"][:4], startName, dic["maxEnd"][:4], endName]   
        s = pd.Series(linea).str.wrap(20)
        tabla.append(s)
    print("The first 3 and last 3 of the SCC are: ")
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))

#Requerimiento 4
def printMinTime(pila):
    tamano = lt.size(pila)
    tabla = [["Start Station Id", "Start Station Name", "End Station Id", "End Station Name", "Avg Route Duration"]]
    if tamano >= 12: 
        for i in range(tamano, tamano-3,-1):
            dic = lt.getElement(pila, i)
            startName = dic["vertexA"][5:]
            endName = dic["vertexB"][5:]
            if startName == "":
                startName = "Unknown"
            if endName == "":
                endName = "Unknown"
            linea = [dic["vertexA"][:4], startName, dic["vertexB"][:4], endName, str(dic["weight"])]
            s = pd.Series(linea).str.wrap(20)
            tabla.append(s)
        for i in range(3, 0,-1):
            dic = lt.getElement(pila, i)
            startName = dic["vertexA"][5:]
            endName = dic["vertexB"][5:]
            if startName == "":
                startName = "Unknown"
            if endName == "":
                endName = "Unknown"
            linea = [dic["vertexA"][:4], startName, dic["vertexB"][:4], endName, str(dic["weight"])]
            s = pd.Series(linea).str.wrap(20)
            tabla.append(s)
    else:
        for i in range(lt.size(pila), 0, -1):
            dic = lt.getElement(pila, i)
            startName = dic["vertexA"][5:]
            endName = dic["vertexB"][5:]
            if startName == "":
                startName = "Unknown"
            if endName == "":
                endName = "Unknown"
            linea = [dic["vertexA"][:4], startName, dic["vertexB"][:4], endName, str(dic["weight"])]
            s = pd.Series(linea).str.wrap(20)
            tabla.append(s)
    
    print("\n - Path details:")
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))


#Requerimiento 5
def printSuscriberTripsInDateRange(answer):
    print("\n+++ Top out station data: +++")
    tabla = [["Station Id", "Station Name", "Out Degree(Routes)", "Out Trips"], 
    [answer["topOutStation"][0][:4], answer["topOutStation"][0][5:], answer["topOutStation"][2], answer["topOutStation"][1]]]
    s = pd.Series(tabla).str.wrap(20)
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))

    print("\n+++ Top in station data: +++")
    tabla = [["Station Id", "Station Name", "In Degree(Routes)", "In Trips"], 
    [answer["topInStation"][0][:4], answer["topInStation"][0][5:], answer["topInStation"][2], answer["topInStation"][1]]]
    s = pd.Series(tabla).str.wrap(20)
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))

    print("\n+++ Top out trips rush hour station data: +++")
    tabla = [["Station Id", "Station Name", "Out rush hour", "Out rush hour count"], 
    [answer["topOutStation"][0][:4], answer["topOutStation"][0][5:], answer["start_rush_hour"][1], answer["start_rush_hour"][0]]]
    s = pd.Series(tabla).str.wrap(20)
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))

    print("\n+++ Top in trips rush hour station data: +++")
    tabla = [["Station Id", "Station Name", "In rush hour", "In rush hour count"], 
    [answer["topInStation"][0][:4], answer["topInStation"][0][5:], answer["end_rush_hour"][1], answer["end_rush_hour"][0]]]
    s = pd.Series(tabla).str.wrap(20)
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))
          

#Requerimiento 6
def printTopOutIn(dic):
    do = dic["Out"]
    tabla = [["Station ID", "Station Name", "Out Degree", "Out Trips"],
            [do["vertex"][:4], do["vertex"][5:], str(do["outdegree"]), str(do["mayor"])]]
    print("\n+++ Top out station data: +++")
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))

    di = dic["In"]
    tabla2 = [["Station ID", "Station Name", "In Degree", "In Trips"],
            [di["vertex"][:4], di["vertex"][5:], str(di["indegree"]), str(di["mayor"])]]
    print("\n+++ Top in station data: +++")
    print(tabulate.tabulate(tabla2,  tablefmt = "grid"))

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        load = controller.loadTrips(cont, "Bikeshare/Bikeshare-ridership-2021-utf8-small.csv")
        viajes = load[1]
        vertices = load[2]
        numedges = controller.totalConnections(cont["connections"])
        numvertex = controller.totalStops(cont["connections"])
        print("Total de viajes obtenidos: ", viajes)
        print('Numero de vertices: ' + str(numvertex))
        print('Numero de arcos: ' + str(numedges))
        optiontwo(cont, vertices)

    elif int(inputs[0]) == 3:
        print("=============== Req No. 1 Inputs ===============")
        print("Top 5 stations inside in the bikeshre Network")
        print('Number of stations in the network: ' + str(controller.totalStops(cont['connections'])))
        
        print("=============== Req No. 1 Answer ===============")
        print("Top 5 stations used as trip origins are: ")
        Top5Estaciones = controller.Requerimiento1(cont)
        printTop5Estaciones_mas_viajes(Top5Estaciones)


    elif int(inputs[0]) == 4:
        name = input("Ingrese el nombre de la estación de inicio o salida: ")
        id = input("Ingrese el ID de la estación de inicio o salida: ")
        time = float(input("Ingrese el tiempo máximo que puede tomar el viaje en mins: "))
        minstations = int(input("Ingrese el número minimo de estaciones de parada para la ruta: "))
        maxroutes = int(input("Ingrese el número máximo de rutas de respuesta: "))
        vertex = id+"-"+name

        print("\n=============== Req No. 2 Inputs ===============")
        print("Available time:", time, "[seg]")
        print("Minimum number of stations:", minstations)
        print("Maximum numer of routes:", maxroutes)
        print("Starting station: ", vertex)

        recorridos = controller.Requerimiento2(cont, vertex, time, minstations, maxroutes)
        
        print("\n=============== Req No. 2 Answer ===============")
        print("\n+++++ The TOP", maxroutes, "routes are: +++++")
        printPossibleRoutes(recorridos)

    elif int(inputs[0]) == 5:
        print("=============== Req No. 3 Inputs ===============")
        print("+++ calculating the strongly connected components +++")
        
        req = controller.Requerimiento3(cont)
        con = req[0]
        list = req[1]

        print("\n=============== Req No. 3 Answer ===============")
        print("There are", con, "Strongly Connected Components (SCC) in the graph")
        print("\n+++ The SCC details are: +++")
        printConnectedComponents(list)


    elif int(inputs[0]) == 6:
        startid = input("Ingrese el ID de la estación de inicio: ")
        startname = input("Ingrese el nombre de la estación de inicio: ")
        endid = input("Ingrese el ID de la estación de llegada: ")
        endname = input("Ingrese el nombre de la estación de llegada: ")
        
        print("\n=============== Req No. 4 Inputs ===============")
        print("Start station:", startname, "with ID:", startid)
        print("End station:", endname, "with ID:", endid)
        
        req = controller.Requerimiento4(cont, startid+"-"+startname, endid+"-"+endname)
        totalTime = req[0]
        nStops = req[1]
        nRoutes = req[2]
        pila = req[3]

        print("\n=============== Req No. 4 Answer ===============")
        print("+++ Dijkstra's Trip details +++")
        print(" - Number of stops:", nStops)
        print(" - Number of routes:", nRoutes)
        print(" - Total time [seg]:", totalTime)
        printMinTime(pila)
        
    elif int(inputs[0]) == 7:
        start_date = input("Ingrese la Fecha inicial de consulta (formato “%m/%d/%Y”): ") 
        end_date =  input("Ingrese la Fecha final de consulta (formato “%m/%d/%Y”): ") 
        print("=============== Req No. 5 Inputs ===============")
        print("Analyze trips between ", start_date, " and ", end_date)
        
        suscriberConnections, total_timeTrip, n_trips, answer = controller.Requerimiento5(cont, start_date, end_date)
        print("=============== Req No. 5 Answer ===============")
        print(n_trips, "trips between", start_date, " and ", end_date)
        vertices = controller.totalStops(suscriberConnections)
        arcos = controller.totalConnections(suscriberConnections)
        print("Vertices (estaciones): ", vertices, "& Edges (trips): ", arcos)
        printSuscriberTripsInDateRange(answer)

    elif int(inputs[0]) == 8:
        bike_id = int(input("Ingrese el ID de la bicicleta: "))
        print("\n=============== Req No. 6 Inputs ===============")
        print("Analyze trips with the bike ID", bike_id)
        req = controller.Requerimiento6(cont, bike_id)
        numedges = controller.totalConnections(cont["gBikeId"])
        numvertex = controller.totalStops(cont["gBikeId"])
        total_duration = req[0] 
        total_trips = req[1]
        dic = req[2]

        print("\n=============== Req No. 6 Answer ===============")
        print(total_trips, "trips with bike ID", bike_id, "\n")

        print(numvertex, "unique stations loaded...")
        print(numedges, "clean avg trips data loaded...")
        print("\n\n--- DiGraph specs ---")
        print("Nodes: ", numvertex, "& Edges:", numedges)
        print("Total trip time:", total_duration, "[sec].")
        print("Total trip time:", total_duration/60, "[h].")
        printTopOutIn(dic)
    
    else:
        sys.exit(0)
sys.exit(0)
