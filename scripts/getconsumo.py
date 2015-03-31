#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent
import time
import urllib
import json
import httplib
import os
import time
import types

API_CLIMA = "http://api.openweathermap.org/data/2.5/weather?id=3435910"
API_LESS = "http://52.10.233.24/v1/circuits/{0}/latest"

cielo = {
    800: "Soleado",
    801: "Parcialmente soleado",
    802: "Parcialmente nublado",
    803: "Mayormente nublado",
    804: "Nublado",
    711: "Neblina"
}

httplib.HTTPConnection.debuglevel = 0


def GET(url):

    # hace peticion a api en amazon, y api clima
    result = []
    try:
        response = urllib.urlopen(url)
    except:
        print "failed host {0}".format(url)
        return 0
    else:
        if response.code == 200:
            result = dict(json.load(response))
            # print result
            if result.has_key('data'):
                return result['data'][0]['proc']["power"]
            elif result.has_key('weather') and result.has_key('main'):
                return result
            else:
                return 0
        elif response.code == 500:
            return 0
        else:
            return 0


def GET_CLIMA():

    result = GET(API_CLIMA)
    clima = {}
    if result == 0:
        result = "null"
        return result
    elif result['main'].has_key('temp'):
        clima = result['main']
        if result['weather'][0]['id'] in cielo.keys():
            clima.update({"cielo": cielo[result['weather'][0]['id']]})
        else:
            clima.update({"cielo": result['weather'][0]['description']})
        clima.update({"temp": clima["temp"] - 273})
        clima.update({"temp_max": clima["temp_max"] - 273})
        clima.update({"temp_min": clima["temp_min"] - 273})
        return clima


def transform(array):
    dic = {}
    for key in range(len(array)):
        dic.update({array[key]: 0})
    return dic

def consumototal(self, **args):

    borneras_aire = transform(args.get('aire'))
    borneras_luz = transform(args.get('luz'))
    borneras_tomas = transform(args.get('corrientes'))
    
    r_luz, r_aire, r_tomas = [], [], []
    suma_aire, suma_luz, suma_tomas, suma_total = 0, 0, 0, 0

    clima = GET_CLIMA()
    if clima != "null":
        timewait = 300
    else:
        timewait = 5

    count = 0

    while True:

        count += 1
        # despues de una hora, actualizar el clima
        if count == timewait:
            clima = GET_CLIMA()
            if clima == "null":
                timewait = 5
                count = 0
            else:
                timewait = 300
                count = 0

        # loopear por borneras de aire
        for _id in borneras_aire.keys():
            power = GET(API_LESS.format(_id))
            if type(power) != types.NoneType:
                borneras_aire[_id] = power
                r_aire.append(power)
            else:
                r_aire.append(borneras_aire[_id])

        # loopear por borneras de luz
        for _id in borneras_luz.keys():
            power = GET(API_LESS.format(_id))
            if type(power) != types.NoneType:
                borneras_luz[_id] = power
                r_luz.append(power)
            else:
                r_luz.append(borneras_luz[_id])

        # loopear por borneras de tomas
        for _id in borneras_tomas.keys():
            power = GET(API_LESS.format(_id))
            if type(power) != types.NoneType:
                borneras_tomas[_id] = power
                r_tomas.append(power)
            else:
                r_tomas.append(borneras_tomas[_id])

        suma_aire = sum(r_aire)
        suma_luz = sum(r_luz)
        suma_tomas = sum(r_tomas)
        suma_total = suma_aire + suma_luz + suma_tomas

        # reset
        r_aire = []
        r_luz = []
        r_tomas = []

        self.emit('consumo_total', {'power_total': suma_total, 'power_aire': suma_aire,
                                    'power_luz': suma_luz, 'power_tomas': suma_tomas, 'clima': clima})

        # time.sleep(1)
    gevent.sleep(0.1)
