import pandas as pd
import sys
import argparse
from datetime import date
import csv
from datetime import datetime
from math  import radians
import math
import cmath
from cmath import sqrt
import os

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'latlong',
        type=str,
        default='0'
    )
    parser.add_argument(
       '--output',
       type=str,
       default=('csv')
    )
    args = parser.parse_args()

    lat_long = args.latlong
    lat_long = lat_long.replace("'", "")
    nome = args.output
    lat1 = lat_long.split(",")[0]
    lng1 = lat_long.split(",")[1]

    now = str(datetime.now())
    now = now.split(".")[0]
    now = now.replace(" ", "_")
    now = now.replace(":", "-")
    pesquisa = pd.read_csv('data/eventlog.csv')

    distancia = []
    existe = False

    latitude_tabela = []
    longitude_tabela = []
    for k in range(len(pesquisa.payload)):
        s = str(pesquisa.payload[k])
        latitude_tabela.append(s.split(",")[2])

        aux = s.split(",")[3]
        longitude_tabela.append(aux.split("<")[0])

    def haversine_meters(lat1, lng1, lat2, lng2):
        """haversine_meters calculates the distance in meters between two coordinates"""

        rlat1 = math.radians(lat1)
        rlng1 = math.radians(lng1)
        rlat2 = math.radians(lat2)
        rlng2 = math.radians(lng2)

        dlat = rlat2 - rlat1
        dlng = rlng2 - rlng1
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
            math.radians(lat2)) * math.sin(dlng / 2) * math.sin(dlng / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        total = (6371 * c) * 1000
        return total



    if nome == 'json':
        output_arq = open(now + "." + nome, 'w')
    elif nome == 'csv':
        output_arq = open(now + "." + nome, 'w')
        output_arq.writelines("device,prefix,instant,payload,company\n")


    for i in range(len(pesquisa.payload)):
        lat2 = float(latitude_tabela[i])
        lng2 = float(longitude_tabela[i])
        distancia.append(haversine_meters(float(lat1), float(lng1), float(lat2), float(lng2)))
        if (distancia[i] <= 50):
            existe = True
            if nome == 'json':
                output_arq.writelines("{\n \"device\": \"" + str(pesquisa.device[i]) + '\",\n \"prefix\": \"' + str(
                    pesquisa.prefix[i]) + '\",\n \"instant\": \"' + str(
                    pesquisa.instant[i]) + '\",\n \"payload\": \"' + str(
                    pesquisa.payload[i]) + '\",\n \"company\": \"' + str(pesquisa.company[i]) + "\"\n}\n")

            elif nome == 'csv':
                output_arq.writelines(str(pesquisa.device[i]) + ',' + str(pesquisa.prefix[i]) + ',' + str(
                    pesquisa.instant[i]) + ',\"' + str(pesquisa.payload[i]) + '\",' + str(pesquisa.company[i]) + "\n")


    if (existe):
        name = now + "." + nome
        print ("Pesquisa concluída: Arquivo {} gerado".format(name))
        output_arq.close()
    else:
        name = now + "." + nome
        output_arq.close()
        local = os.path.dirname(os.path.realpath(__file__))
        print ("Pesquisa concluída: Valores não encontrados")
        os.remove(os.path.join(local, name))


if __name__ == '__main__':
    main()


