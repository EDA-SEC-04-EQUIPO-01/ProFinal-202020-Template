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


import sys
import config
from App import controller
from DISClib.ADT import stack
from DISClib.DataStructures import listiterator as it
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
small = "taxi-trips-wrvz-psew-subset-small.csv"
medium = "taxi-trips-wrvz-psew-subset-medium.csv"
large = "taxi-trips-wrvz-psew-subset-large.csv"
# ___________________________________________________


# ___________________________________________________
#  Menu principal
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de taxis en Chicago: ")
    print("3- Reporte de información de compañías y taxis: ")
    print("4- Conocer taxis con más puntos: ")
    print("5- Conocer el mejor horario entre dos 'Community Areas': ")
    print("*******************************************")
# ___________________________________________________


def optionTwo():
    file = input("¿Que archivo desea cargar?\nEscriba 1 para el pequeño.\nEscriba 2 para el mediano.\nEscriba 3 para el grande.\n")
    print("\nCargando información de taxis en Chicago")
    if file[0] == "1":
        controller.loadFile(cont,small)
        print("Archivo pequeño cargado exitosamente")
    elif file[0] == "2":
        controller.loadFile(cont,medium)
        print("Archivo mediano cargado exitosamente")
    elif file[0] == "3":
        controller.loadFile(cont,large)
        print("Archivo grande cargado exitosamente")
    else:
        print("Ingrese un valor válido")


def optionThree(): #N
    try:
        topTaxis=int(input("Ingresa cuantas empresas quieres ver segun la cantidad de taxis que poseen: "))
        topServicios=int(input("Ingresa cuantas empresas quieres ver segun la cantidad de trayectos recorridos: "))
        respuesta= controller.extraerInfo(cont,topServicios, topTaxis)
        print("\nEl numero total de taxis es de: ",respuesta[1],"\nEl total de compañias con almenos un vehiculo registrado es de: ",respuesta[0],"\n\nLas compañias con más taxis afiliados son: ")
        iterator = it.newIterator(respuesta[2])
        while it.hasNext(iterator):
            element = it.next(iterator)
            print(element)
        print("\n\nLas compañias que mas servicios prestaron son:")
        iterator = it.newIterator(respuesta[3])
        while it.hasNext(iterator):
            element = it.next(iterator)
            print(element)
    except:
        print("Ingrese un número válido")
    


def optionFour(): 
    try:
        des = int(input('¿Desea conocer una fecha (1) o un rango de fechas (2)? '))
        if des == 1:
            date = input('Ingrese la fecha que desea conocer (AAAA-MM-DD): ')
            top = int(input('Ingrese el número de elementos que quiere en el top: '))
            res = controller.getMostPointsinDate(cont,date,top)
            if res != None:
                iterator = it.newIterator(res)
                i = 1
                print('\nLos',top,'taxis con mas puntos en la fecha',date,'son:\n')
                while it.hasNext(iterator):
                    element = it.next(iterator)
                    pr = "{0}. El taxi {1} con {2} puntos.\n".format(i,element[0],element[1])
                    print(pr)
                    i+=1
            else:
                print("\nLa fecha ingresada no tiene taxis.")
        elif des == 2: 
            date1 = input('Ingrese la fecha inicial del rango que desea conocer (AAAA-MM-DD): ')
            date2 = input('Ingrese la fecha final del rango que desea conocer (AAAA-MM-DD): ')
            top = int(input('Ingrese el número de elementos que quiere en el top: '))
            res = controller.getMostPointsinDateRange(cont,date1,date2,top)
            if res != None:
                iterator = it.newIterator(res)
                i = 1
                print('\nLos',top,'taxis con mas puntos entre la fecha',date1,'y la fecha',date2,'son:\n')
                while it.hasNext(iterator):
                    element = it.next(iterator)
                    pr = "{0}. El taxi {1} con {2} puntos.\n".format(i,element[0],element[1])
                    print(pr)
                    i+=1
            else:
                print("\nEl rango ingresado no tiene taxis")
        else:
            print('Ingrese una opción válida')
    except:
        print('Ingrese una fecha válida.')


def optionFive():
    horarioBueno = controller.getBestScheduleOnRange(cont,originArea,endArea,initialRange,finalRange)
    if horarioBueno == False:
        print("Los rangos de fecha que introdujiste no están en los formatos correctos")
    elif horarioBueno[0] == None:
        print("Las areas que introdujiste no existen")
    else:
        print("El mejor horario para ir desde la estación",int(originArea),"hasta la estación",int(endArea),"en el rango de tiempo",initialRange,"-",finalRange,"es",horarioBueno[1],"y te demoras",horarioBueno[0],"segundos")



"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs) == 1:
        print("\nInicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:      
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        originArea = float(input("Introduzca el area de donde quiere viajar: "))
        endArea = float(input("Introduzca el area a donde quiere ir: "))
        initialRange = input("Introduzca la hora inicial que quiere consultar en formato HH:MM: ")
        finalRange = input("Introduzca la hora final que quiere consultar en formato HH:MM: ")
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    else:
        sys.exit(0)
sys.exit(0)