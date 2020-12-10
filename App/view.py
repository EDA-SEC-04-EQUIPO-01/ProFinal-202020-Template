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
    print("2- Cargar información de taxis en Chicago")
    print("3- Calcular la cantidad de clusters de viajes")
    print("4- Ruta turistica circular")
    print("5- Conocer estaciones más concurridas y la menos concurridas: ")

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


def optionThree():
    pass 


def optionFour():  #N
    pass


def optionFive():
    pass

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
        print(cont['dates'])
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:      
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    else:
        sys.exit(0)
sys.exit(0)