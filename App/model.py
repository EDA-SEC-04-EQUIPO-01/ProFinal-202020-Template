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
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import minpq as mq
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me 
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
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
                    'areas': None
                    }


        analyzer['taxis'] = m.newMap(numelements=1000,
                                      maptype = 'PROBING',
                                      loadfactor=0.5,
                                      comparefunction=comparetaxi)
        analyzer['dates'] = om.newMap(comparefunction=compare)
        analyzer['companies']=m.newMap(numelements=1000,
                                      maptype = 'PROBING',
                                      loadfactor=0.5,
                                      comparefunction=compare)
        analyzer['areas'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=768,
                                              comparefunction=compare)


        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

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

def getMostPointsinDate(analayzer,date,top):
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
    return res

def getMostPointsinDateRange(analyzer,date1,date2,top):
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
    return res 
  

# ==============================

# ==============================
# Funciones Helper
# ==============================

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
        
# ==============================