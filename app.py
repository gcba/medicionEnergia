#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent
import os
import bottle

from bottle import error
from socketio import socketio_manage
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace
from gevent import monkey
from scripts.getconsumo import consumototal

monkey.patch_all()
app = bottle.Bottle()

if os.environ.get('OPENSHIFT_PYTHON_DIR'):
    zvirtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],
                            'virtenv', 'bin', 'activate_this.py')
    execfile(zvirtenv, dict(__file__=zvirtenv))
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
else:
    ip = "0.0.0.0"
    port = 8080


class consumoEnergetico(BaseNamespace, BroadcastMixin):

    def on_receive(self, msg):

        if msg == "5to":

            borneras_aire_5t = ["9061", "9062", "9063"]
            borneras_luz_5t = ["9014", "9016"]
            borneras_tomas_5t = [
                "9013", "9015", "9064", "9071", "9072", "9074", "9075"]
            consumototal(
                self, aire=borneras_aire_5t, luz=borneras_luz_5t, corrientes=borneras_tomas_5t)

        elif msg == "2do":

            borneras_aire_2d = ["9031", "9033", "9035"]
            borneras_luz_2d = [
                "9034", "9051", "9052", "9053", "9054", "9055", "9056"]
            borneras_tomas_2d = ["9021", "9022", "9023"]
            consumototal(
                self, aire=borneras_aire_2d, luz=borneras_luz_2d, corrientes=borneras_tomas_2d)


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


@error(404)
@error(500)
def handler_error(error):
    return 'Nothing here, sorry'


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
               debug=False,
               reloader=False,
               )
