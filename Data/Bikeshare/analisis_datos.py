

def cargar_datos(ruta:str):
    archivo = open(ruta, "r", encoding = "utf8")
    titulos = archivo.readline()
    linea = archivo.readline()
    dic_estaciones_salida ={}
    dic_estaciones_llegada = {}
    while linea != "":
        datos = linea.replace("\"", "").strip().split(",")
        viaje = {"trip_id":datos[0],
                 "trip_duration": datos[1],
                 "start_time":datos[3],
                 "start_station_name":datos[4],
                 "end_estation_id":datos[5],
                 "end_time":datos[6],
                 "end_station_name": datos[7],
                 "bike_id":datos[8],
                 "user_type":datos[9]}
        if viaje["user_type"] == "Casual Member":
            id_estacion_salida = datos[2]
            if id_estacion_salida not in dic_estaciones_salida:
                dic_estaciones_salida[id_estacion_salida]=[viaje]
            else:
                dic_estaciones_salida[id_estacion_salida].append(viaje)
                
            id_estacion_llegada = datos[5]
            if id_estacion_llegada not in dic_estaciones_llegada:
                dic_estaciones_llegada[id_estacion_llegada]=[id_estacion_salida]
            else:
                if id_estacion_salida not in dic_estaciones_llegada[id_estacion_llegada]:
                    dic_estaciones_llegada[id_estacion_llegada].append(id_estacion_salida)
                
        linea = archivo.readline()
    archivo.close()
    return dic_estaciones_salida, dic_estaciones_llegada

print("termino")
tupla_dic= cargar_datos("Bikeshare-ridership-2021-utf8-small.csv")
dic_estaciones_llegada = tupla_dic[1]
dic_estaciones_salida = tupla_dic[0]

suma = 0
for id_estacion_llegada in  dic_estaciones_llegada:
    suma += len(dic_estaciones_llegada[id_estacion_llegada])
promedio = suma/len(dic_estaciones_llegada)
print(promedio)

