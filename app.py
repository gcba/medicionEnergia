#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

import gevent
import time
import random
import urllib
import json
import httplib
import os
import time
import types

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

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
    try:
        result = []
        # print url
        response = urllib.urlopen(url)
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
                return clima
            else:
                return 0
        else:
            return 0
    except:
        print "failed host {0}".format(url)
        return 0


def GET_CLIMA():
    clima = GET(API_CLIMA)
    if clima == 0:
        clima = "null"
    return clima


class consumoEnergetico(BaseNamespace, BroadcastMixin):

    def recv_connect(self):
        def sendapi():

            r_luz, r_aire, r_tomas = [], [], []
            suma_aire, suma_luz, suma_tomas, suma_total = 0, 0, 0, 0

            clima = GET_CLIMA()
            count = 0

            borneras_aire = ["9061", "9062", "9063"]
            borneras_luz = ["9014", "9016"]
            borneras_tomas = [
                "9013", "9015", "9071", "9072", "9073", "9074", "9075"]

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

                time.sleep(5)
            gevent.sleep(0.1)
        self.spawn(sendapi)


class Application(object):

    def __init__(self):
        self.buffer = []

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/') or 'index.html'

        if path.startswith('static/') or path == 'index.html':
            try:
                data = open(path).read()
            except Exception:
                return not_found(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'/consumo': consumoEnergetico})
        else:
            return not_found(start_response)


def not_found(start_response):
    start_response('500 Not Found', [])
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']


if __name__ == '__main__':
    print 'Listening on port {0} ip {1}'.format(ip, port)
    SocketIOServer((ip, port), Application(), resource="socket.io", transports=[
                   'websocket', 'xhr-polling']).serve_forever()
