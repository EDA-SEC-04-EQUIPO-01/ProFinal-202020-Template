'''
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
 '''
import config
from DISClib.ADT import stack as st
from DISClib.ADT.graph import gr
from DISClib.DataStructures import edge as ed
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import minpq as mq
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me 
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.Algorithms.Sorting import selectionsort as st
import datetime

assert config

'''
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
'''

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo
def newAnalyzer():
    try:
        analyzer = {
                    'taxis': None,
                    'dates':None,
                    'companies': None,
                    'areas': None,
                    'IDS': None,
                    'startTime': None,
                    'startAreas':None,
                    'endAreas': None,
                    'trips': None
                    }
        analyzer['endAreas'] = m.newMap(numelements=47,
                                        maptype = 'PROBING',
                                        loadfactor=0.4893617021276596,
                                        comparefunction=comparetaxi)
        analyzer['startAreas'] = m.newMap(numelements=47,
                                        maptype = 'PROBING',
                                        loadfactor=0.4893617021276596,
                                        comparefunction=comparetaxi)
        analyzer['trips'] = m.newMap(numelements=1000,
                                        maptype = 'PROBING',
                                        loadfactor=0.5,
                                        comparefunction=comparetaxi)
        analyzer['taxis'] = m.newMap(numelements=1000,
                                      maptype = 'PROBING',
                                      loadfactor=0.5,
                                      comparefunction=comparetaxi)
        analyzer['dates'] = om.newMap(comparefunction=compare)
        analyzer['areas'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=768,
                                              comparefunction=comparetaxi)
        analyzer['IDS']=m.newMap(numelements=300,
                                      maptype = "PROBING",
                                      loadfactor= 0.5,
                                      comparefunction= compareIds)

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

def crearHashInfo(analyzer,trip):
    empresa=trip['company']
    if m.get(analyzer['IDS'],"totalServicios") is None:
        m.put(analyzer['IDS'], "totalServicios", 1)
    else:
        totalParcial = me.getValue(m.get(analyzer['IDS'],"totalServicios"))
        m.put(analyzer['IDS'],'totalServicios',1+totalParcial)
    if m.get(analyzer["IDS"], empresa) is None:

        a = m.newMap(numelements=4,
                    maptype = "PROBING",
                    loadfactor= 0.5,
                    comparefunction= compareIds)  

        lista=lt.newList(datastructure='ARRAY_LIST',
                         cmpfunction = compare)   

        lt.addLast(lista,trip["taxi_id"])  
        m.put(a,"nombreTaxis",lista)
        m.put(a,"servicios",1)
        
    else:
        a = getValue(analyzer['IDS'],empresa)
        parejaServicios=m.get(a,"servicios")
        num= me.getValue(parejaServicios) +1
        m.put(a,"servicios",num)


        parejaTaxis = m.get(a,"nombreTaxis")
        lista= me.getValue(parejaTaxis) 
        if lt.isPresent(lista,trip["taxi_id"]) == 0:
            lt.addLast(lista,trip["taxi_id"])
            m.put(a,"nombreTaxis",lista)
    m.put(analyzer['IDS'],empresa, a)


def addTables(map, key, value):
    isThereArea = m.get(map, float(key))
    if isThereArea is None:
        areaMaped = lt.newList(datastructure='ARRAY_LIST',
                                cmpfunction = compare)
        m.put(map,float(key),areaMaped)
        isThereArea = m.get(map, float(key))
    datesList = me.getValue(isThereArea)
    isThereDate = lt.isPresent(datesList, value[11:16])
    if isThereDate == 0:
        lt.addLast(datesList, value[11:16])

def addAreasTable(analyzer, vertex, area, isInitial, date):
    if gr.containsVertex(analyzer['areas'], vertex) is False:
            gr.insertVertex(analyzer['areas'],vertex)
    if isInitial:
        addTables(analyzer['startAreas'],area, date)
        
    else:
        addTables(analyzer['endAreas'], area, date)

        
def calculateEdge(analyzer,vertexA,vertexB,tripDuration):
    isThereTripBefore = m.get(analyzer, vertexA+"-"+vertexB)
    if isThereTripBefore is None:
        time = [0,0]
        m.put(analyzer, vertexA+"-"+vertexB,time)
        isThereTripBefore = m.get(analyzer, vertexA+"-"+vertexB)
    tripTime = me.getValue(isThereTripBefore)
    tripTime[0]+=1
    tripTime[1]+=float(tripDuration)
    return tripTime[1]/tripTime[0]

def addAreasTime(analyzer,trip):
    initialDate = trip['trip_start_timestamp']
    endDate = trip['trip_end_timestamp']
    initialArea = trip['pickup_community_area']
    finalArea = trip['dropoff_community_area']
    tripDuration = trip['trip_seconds']
    if initialArea!=finalArea and tripDuration != 0 and tripDuration != "" and initialArea != "" and finalArea !="" and endDate != None and initialDate != None:
        vertexA = initialArea+" "+initialDate[11:16]
        vertexB = finalArea+" "+endDate[11:16]
        addAreasTable(analyzer,vertexA, initialArea, True, initialDate)
        addAreasTable(analyzer,vertexB, finalArea, False, endDate)
        edge = calculateEdge(analyzer['trips'],vertexA,vertexB,tripDuration)
        existEdge = gr.getEdge(analyzer['areas'], vertexA,vertexB)
        if existEdge is None:
            gr.addEdge(analyzer['areas'], vertexA,vertexB,edge)
        else:
            ed.setWeight(existEdge,edge)

def adddate(analyzer, trip):
    datebr = trip['trip_start_timestamp']
    datepr = ""
    for a in range(0,10):
        datepr+= datebr[a]
    date = datetime.datetime.strptime(datepr, '%Y-%m-%d')
    if om.get(analyzer['dates'],date)==None:
        taxis = m.newMap(numelements=1000,maptype='PROBING',comparefunction=comparetaxi)
        om.put(analyzer['dates'],date,addtaxis(taxis,trip))
    else:
        taxix = om.get(analyzer['dates'],date)
        taxis = me.getValue(taxix)
        om.put(analyzer['dates'],date,addtaxis(taxis,trip))
    return analyzer
    
def addtaxis(taxis, trip):
    try:
        istaxi = m.get(taxis,trip['taxi_id'])
        if istaxi == None and float(trip['trip_miles']) > 0 and float(trip['trip_total']) > 0:
            taxi = {}
            taxi['miles'] = float(trip['trip_miles'])
            taxi['money'] = float(trip['trip_total'])
            taxi['services'] = 1
            m.put(taxis, trip['taxi_id'], taxi)
        elif istaxi != None and float(trip['trip_miles']) > 0 and float(trip['trip_total']) > 0:
            taxi = me.getValue(istaxi)
            taxi['miles'] += float(trip['trip_miles'])
            taxi['money'] += float(trip['trip_total'])
            taxi['services'] += 1
            m.put(taxis, trip['taxi_id'], taxi)  
    except:
        pass
    return taxis


# ==============================
# Funciones de consulta

def getValue(map,key):
    return me.getValue(m.get(map,key))

    
def extraerInfo(analayzer, topServicios, topTaxis): #N
    totalcompanies = lt.size(m.keySet(analayzer['IDS']))-1
    totaltaxis = 0
    tser = mq.newMinPQ(compareinverted)
    ttax = mq.newMinPQ(compareinverted)
    res1 = lt.newList()
    res2 = lt.newList()
    listcompanies = m.keySet(analayzer['IDS'])
    iterator = it.newIterator(listcompanies)
    while it.hasNext(iterator):
        element = it.next(iterator)
        if element != 'totalServicios':
            elementpr = getValue(analayzer['IDS'],element)
            services = getValue(elementpr,'servicios')
            taxis = getValue(elementpr,'nombreTaxis')
            numtaxis = lt.size(taxis)
            totaltaxis += numtaxis
            mq.insert(tser,(element,services))
            mq.insert(ttax,(element,numtaxis))
    
    for a in range(0,topServicios):
        lt.addLast(res1,mq.delMin(tser))
    
    for a in range(0,topTaxis):
        lt.addLast(res2,mq.delMin(ttax))

    return (totalcompanies,totaltaxis,res2,res1)


def getMostPointsinDate(analayzer,date,top):
    try:
        info = om.get(analayzer['dates'],date)
        taxismap = me.getValue(info)
        taxislist = m.keySet(taxismap)
        taxispoints = mq.newMinPQ(compareinverted)
        iterator = it.newIterator(taxislist)
        res = lt.newList()
        while it.hasNext(iterator):
            element = it.next(iterator)
            taxix = m.get(taxismap,element)
            taxi = me.getValue(taxix)
            points = (taxi['miles']/taxi['money'])*taxi['services']
            mq.insert(taxispoints,(element,points))
        for a in range(0,top):
            lt.addLast(res,mq.delMin(taxispoints))
    except:
        res = None
    return res
    


def getBestScheduleOnRange(analyzer,originArea,endArea,initialRange,finalRange):
    posiblesVertices = m.get(analyzer['startAreas'],originArea)
    posiblesSalidas = m.get(analyzer['endAreas'], endArea)
    menor = None
    horarioBueno = None
    if posiblesVertices != None and posiblesSalidas != None:
        vertices = me.getValue(posiblesVertices)
        salidas = me.getValue(posiblesSalidas)
        iterator = it.newIterator(vertices)
        menor = 10000000000000000000000
        path = None
        while it.hasNext(iterator):
            vertice = it.next(iterator)
            salidasIterator = it.newIterator(salidas)
            vertices = str(originArea) + " " + vertice
            if isInRange(vertice, initialRange,finalRange):
                dijsktra = djk.Dijkstra(analyzer['areas'],vertices)
                while it.hasNext(salidasIterator):
                    salida = it.next(salidasIterator)
                    if djk.hasPathTo(dijsktra, str(endArea)+" "+salida):
                        camino = djk.distTo(dijsktra, str(endArea)+" "+salida)
                        if camino < menor:
                            menor = camino
                            path = djk.pathTo(dijsktra, str(endArea)+" "+salida)
        horario = st.pop(path)
        horarioBueno = horario['vertexA'][len(horario['vertexA'])-5:]
    return (menor, horarioBueno)
                    
            
            

def getMostPointsinDateRange(analyzer,date1,date2,top):
    try:
        info = om.values(analyzer['dates'],date1,date2)
        iterator1 = it.newIterator(info)
        taxis = m.newMap(numelements=1000, maptype = 'PROBING', loadfactor=0.5, comparefunction=comparetaxi)
        taxispoints = mq.newMinPQ(compareinverted)
        res = lt.newList()
        while it.hasNext(iterator1):
            element1 = it.next(iterator1)
            taxislist = m.keySet(element1)
            iterator2 = it.newIterator(taxislist)
            while it.hasNext(iterator2):
                element2 = it.next(iterator2)
                taxix = m.get(element1,element2)
                taxi = me.getValue(taxix)
                points = (taxi['miles']/taxi['money'])*taxi['services']
                istaxi = m.get(taxis,element2)
                if istaxi == None:
                    m.put(taxis,element2,points)
                else:
                    value = me.getValue(istaxi)
                    value += points
                    m.put(taxis,element2,value)
        taxislist = m.keySet(taxis)
        iterator = it.newIterator(taxislist)
        while it.hasNext(iterator):
            element = it.next(iterator)
            taxix = m.get(taxis,element)
            taxid = me.getKey(taxix)
            taxipo = me.getValue(taxix)
            mq.insert(taxispoints,(taxid,taxipo))

        for a in range(0,top):
            lt.addLast(res,mq.delMin(taxispoints))
    except:
        res = None
    return res 
  

# ==============================

# ==============================
# Funciones Helper
# ==============================
def convertirTiempo(tiempo):
    if tiempo[0] == "0":
        time = int(tiempo[1])
    else:
        time = int(tiempo)
    return time

def isInRange(hora, rango1, rango2):
    horaRangoInicial = convertirTiempo(rango1[:2])
    minutosRangoInicial = convertirTiempo(rango1[3:])
    horaRangoFinal =  convertirTiempo(rango2[:2])
    minutosRangoFinal = convertirTiempo(rango2[3:])
    horaComparada = convertirTiempo(hora[:2])
    minutosComparada = convertirTiempo(hora[3:])
    if (horaComparada > horaRangoInicial):
        if horaComparada < horaRangoFinal:
            return True
        elif horaComparada == horaRangoFinal and minutosRangoFinal >= minutosComparada:
            return True
    elif horaComparada == horaRangoInicial and minutosComparada<=minutosRangoInicial:
        if horaComparada < horaRangoFinal:
            return True
        elif horaComparada == horaRangoFinal and minutosRangoFinal >= minutosComparada:
            return True
    return False
        

# ==============================
# Funciones de Comparacion
def compare(element1, element2):

    if (element1 == element2):
        return 0
    elif (element1 > element2):
        return 1
    else:
        return -1

def comparetaxi(element1, element2):

    if (element1 == element2['key']):
        return 0
    elif (element1 > element2['key']):
        return 1
    else:
        return -1

def compareinverted(tup1, tup2):
    num1 = tup1[1]
    num2 = tup2[1]
    if (num1 == num2):
        return 0
    elif (num1 > num2):
        return -1
    else:
        return 1
        
def compareIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


# ==============================