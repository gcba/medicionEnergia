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
            elif result.has_key('main') and result.has_key('weather'):
                clima = result['main']
                return clima
            else:
                return 0
        elif response.code == 500:
            return 0
        else:
            return 0


def GET_CLIMA():

    clima = GET(API_CLIMA)
    if clima == 0:
        clima = "null"
        return clima
    elif clima.has_key('temp'):
        if clima['weather'][0]['id'] in cielo.keys():
            clima.update({"cielo": cielo[clima['weather'][0]['id']]})
        else:
            clima.update({"cielo": clima['weather'][0]['description']})
        clima.update({"temp": clima["temp"] - 273})
        clima.update({"temp_max": clima["temp_max"] - 273})
        clima.update({"temp_min": clima["temp_min"] - 273})
        return clima


def consumototal(self, **args):

    borneras_aire = args.get('aire')
    borneras_luz = args.get('luz')
    borneras_tomas = args.get('corrientes')

    r_luz, r_aire, r_tomas = [], [], []
    suma_aire, suma_luz, suma_tomas, suma_total = 0, 0, 0, 0

    clima = GET_CLIMA()
    count = 0
    timewait = 360
    
    while True:

        count += 1
        # despues de una hora, actualizar el clima
        if count == timewait:
            clima = GET_CLIMA()
            if clima == "null":
                timewait = 20
            else:
                count = 0

        # loopear por borneras de aire
        for _id in borneras_aire:
            power = GET(API_LESS.format(_id))
            if type(power) != types.NoneType:
                r_aire.append(power)

        # loopear por borneras de luz
        for _id in borneras_luz:
            power = GET(API_LESS.format(_id))
            if type(power) != types.NoneType:
                r_luz.append(power)

        # loopear por borneras de tomas
        for _id in borneras_tomas:
            power = GET(API_LESS.format(_id))
            if type(power) != types.NoneType:
                r_tomas.append(power)

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