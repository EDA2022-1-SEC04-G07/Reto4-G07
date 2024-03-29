﻿"""
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
 """

import config as cf
import model
import csv
from DISClib.ADT import list as lt
import datetime

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadTrips(analyzer, tripsfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    tripsfile = cf.data_dir + tripsfile
    input_file = csv.DictReader(open(tripsfile, encoding="utf-8"), delimiter=",")
    viajes = 0
    for trip in input_file:
        stopid = trip['End Station Id'] != "" and trip["Start Station Id"] != ""
        bikeid = trip["Bike Id"] != ""
        tripduration = trip["Trip  Duration"] != ""
        if stopid and bikeid and tripduration:
            difcero = int(float(trip["Trip  Duration"])) > 0
            trip['End Station Id'] = str(int(float(trip['End Station Id'])))
            trip['Start Station Id'] = str(int(float(trip['Start Station Id'])))
            difstop = trip['Start Station Name'] != trip['End Station Name'] 
            #difstop = int(float(trip['Start Station Id'])) != int(float(trip['End Station Id'])) 
            if difstop and difcero:

                try:
                    trip["Start Time"] = datetime.datetime.strptime(trip["Start Time"], "%m/%d/%Y %H:%M")
                except Exception:
                    print(trip["Start Time"])
            
                try:
                    trip["End Time"] = datetime.datetime.strptime(trip["End Time"], "%m/%d/%Y %H:%M") 
                except Exception:
                    print(trip["End Time"])

                startStation_name_id = trip["Start Station Id"] + "-" + trip["Start Station Name"]
                endStation_name_id = trip["End Station Id"] + "-" + trip["End Station Name"]
                model.addTrips(analyzer['trip_table'], startStation_name_id + "--" + endStation_name_id, trip)
                model.addStations(analyzer['stations_table'], startStation_name_id, trip["Start Time"], trip["User Type"], True)
                model.addStations(analyzer['stations_table'], endStation_name_id, trip["End Time"], None, False)
                model.addBikeId(analyzer, trip, trip["Bike Id"])
                
                if trip["User Type"] == "Annual Member":
                    model.addDateTrips(analyzer, trip["Start Time"].date(), trip)
                viajes += 1
    
    vertices = model.addGraph(analyzer)
    return analyzer, viajes , vertices

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)

def indegree(analyzer, vertex):
    return model.indegree(analyzer, vertex)

def outdegree(analyzer, vertex):
    return model.outdegree(analyzer, vertex)

#Requerimiento 1
def Requerimiento1(analyzer):
    return model.Top5estaciones_mas_viajes(analyzer)

#Requerimiento 2
def Requerimiento2(analyzer, vertex, time, minstations, maxroutes):
    return model.possibleRoutes(analyzer, vertex, time, minstations, maxroutes)

#Requerimiento 3
def Requerimiento3(analyzer):
    return model.connectedComponents(analyzer)

#Requerimiento 4
def Requerimiento4(analyzer, startStation, endStation):
    return model.minTime(analyzer, startStation, endStation)

#Requerimiento 5
def Requerimiento5(analyzer, start_date, end_date):
    return model.suscriberTripsInDateRange(analyzer, start_date, end_date)

#Requerimiento 6
def Requerimiento6(analyzer, bike_id):
    return model.bikeId(analyzer, bike_id)