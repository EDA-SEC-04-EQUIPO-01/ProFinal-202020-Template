"""
 * Copyright 2020, Departamento de sistemas y Computación
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
def init():
    analyzer = model.newAnalyzer()
    return analyzer
# ___________________________________________________


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos

def loadFile(analyzer, file):
    file = cf.data_dir + file
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.adddate(analyzer, trip)
        model.addAreasTime(analyzer,trip)
    return analyzer
def mayBeInt(pNumber):
    try:
        int(pNumber)
        return True
    except:
        return None

def verifyTime(time):
    if len(time)==5:
        if mayBeInt(time[0]) and mayBeInt(time[1]) and time[2] == ":" and mayBeInt(time[3]) and mayBeInt(time[4]):
            return True
    return False
# ___________________________________________________

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def getBestScheduleOnRange(analyzer,originArea,endArea,initialRange,finalRange):
    if verifyTime(initialRange) and verifyTime(finalRange):
        return model.getBestScheduleOnRange(analyzer,originArea,endArea,initialRange,finalRange)
    return False