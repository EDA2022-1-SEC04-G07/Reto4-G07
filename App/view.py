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
    print("1- Cargar información en el catálogo")
    print("2- Comprar bicicletas para las estaciones con más viajes de origen")
    print("3- Planear paseos turísticos por la ciudad")
    print("4- Reconocer los componentes fuertemente conectados del sistema")
    print("5- Planear una ruta rápida para el usuario")
    print("6- Reportar rutas en un rango de fechas para los usuarios anuales")
    print("7- Planear el mantenimiento preventivo de bicicletas")
    print("8- La estación más frecuentada por los visitantes")

catalog = None

def optiontwo(analyzer, vertices):
    tabla = analyzer["stations_table"]
    lista = [["Station Name", "Station Id", "Indegree", "Outdegree"]]
    for index in range(1,6):
        vertex = lt.getElement(vertices, index)
        indegree = controller.indegree(analyzer, vertex)
        outdegree = controller.outdegree(analyzer, vertex)
        entry = mp.get(tabla, vertex)
        stationid = me.getValue(entry)
        lista2 = [vertex, str(stationid), str(indegree), str(outdegree)]        
        s = pd.Series(lista2).str.wrap(20)
        lista.append(s)

    for index in range(lt.size(vertices)-4, lt.size(vertices)+1):
        vertex = lt.getElement(vertices, index)
        indegree = controller.indegree(analyzer, vertex)
        outdegree = controller.outdegree(analyzer, vertex)
        entry = mp.get(tabla, vertex)
        stationid = me.getValue(entry)
        lista2 = [vertex, str(stationid), str(indegree), str(outdegree)]         
        s = pd.Series(lista2).str.wrap(20)
        lista.append(s)
    print("Los primeros y últimos 5 vértices registrados en el grafo son: ")
    print(tabulate.tabulate(lista,  tablefmt = "grid"))
        



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
        numedges = controller.totalConnections(cont)
        numvertex = controller.totalStops(cont)
        print("Total de viajes obtenidos: ", viajes)
        print('Numero de vertices: ' + str(numvertex))
        print('Numero de arcos: ' + str(numedges))
        optiontwo(cont, vertices)


    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass

    elif int(inputs[0]) == 7:
        pass

    elif int(inputs[0]) == 8:
        pass
    
    else:
        sys.exit(0)
sys.exit(0)
