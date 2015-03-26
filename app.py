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
import bottle

from socketio import socketio_manage
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace
from gevent import monkey

monkey.patch_all()
app = bottle.Bottle()

httplib.HTTPConnection.debuglevel = 0


try:
    zvirtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],
                            'virtenv', 'bin', 'activate_this.py')
    execfile(zvirtenv, dict(__file__=zvirtenv))
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
except:
    ip = "0.0.0.0"
    port = 8080


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
            elif result.has_key('main'):
                clima = result['main']
                if result['weather'][0]['id'] in cielo.keys():
                    clima.update({"cielo": cielo[result['weather'][0]['id']]})
                else:
                    clima.update(
                        {"cielo": result['weather'][0]['description']})
                clima.update({"temp": clima["temp"]-273})
                clima.update({"temp_max": clima["temp_max"]-273})
                clima.update({"temp_min": clima["temp_min"]-273})
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


def consumototal(**args):

    borneras_aire = args.get('aire')
    borneras_luz = args.get('luz')
    borneras_tomas = args.get('corrientes')

    r_luz, r_aire, r_tomas = [], [], []
    suma_aire, suma_luz, suma_tomas, suma_total = 0, 0, 0, 0

    clima = GET_CLIMA()
    count = 0

    while True:

        count += 1
        # despues de una hora, actualizar el clima
        if count == 360:
            clima = GET_CLIMA()
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

        #time.sleep(1)
    gevent.sleep(0.1)    



class consumoEnergetico(BaseNamespace, BroadcastMixin):

    def on_receive(self, msg):

        if msg == "quinto":

            borneras_aire_5t = ["9061", "9062", "9063"]
            borneras_luz_5t = ["9014", "9016"]
            borneras_tomas_5t = ["9013", "9015", "9064", "9071", "9072", "9074", "9075"]
            consumototal(aire=borneras_aire_5t, luz=borneras_luz_5t, corrientes=borneras_tomas)

        elif msg == "segundo":

            borneras_aire_2d = ["9031", "9033", "9035"]
            borneras_luz_2d = ["9034", "9051", "9052", "9053", "9054", "9055", "9056"]
            borneras_tomas_2d = ["9021", "9022", "9023"]
            consumototal(aire=borneras_aire_5t, luz=borneras_luz_5t, corrientes=borneras_tomas)

@app.get('/')
@app.get('/quinto')
def root():
    return bottle.template('quinto')

@app.get('/segundo')
def root():
    return bottle.template('segundo')

@app.get('/_static/<filepath:path>')
def get_static(filepath):
    return bottle.static_file(filepath, root='./static/')

@app.get('/socket.io/<path:path>')
def socketio_service(path):
    socketio_manage(bottle.request.environ,
                    {'/consumo': consumoEnergetico}, bottle.request)

if __name__ == '__main__':
    print 'Listening on port {0} ip {1}'.format(ip, port)
    bottle.run(app=app,
               host=ip,
               port=port,
               server='geventSocketIO',
               debug=True,
               reloader=True,
              )