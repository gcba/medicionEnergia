from gevent import monkey; monkey.patch_all()
import gevent
import time
import random
import urllib
import json

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

def clima():
    res = urllib.urlopen("http://api.openweathermap.org/data/2.5/weather?id=3435910")
    rclima = json.load(res)
    estado = rclima['weather'][0]['description'].lower().encode()
    return estado

class consumoEnergetico(BaseNamespace, BroadcastMixin):
    def recv_connect(self):
        def sendapi():
            r = []
            restado = clima()
            count = 0
            borneras = ["9061", "9062", "9063", "9013", "9015", "9071", "9072", "9073", "9074", "9075", "9014", "9016"]
            while True:
                count += 1
                if count == 3500000:
                    restado = clima()
                    count = 0
                for i in borneras:
                    response = urllib.urlopen("http://52.10.233.24/v1/circuits/{0}/latest".format(i))
                    result = json.load(response)
                    #print result['data'][0]['proc']
                    r.append(result['data'][0]['proc']["power"])
                percent = sum(r)
                #print percent
                r=[]
                self.emit('consumo_total', {'power': percent, "clima": restado})
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
            # elif path.endswith(".svg"):
            #     content_type = "application/x-shockwave-flash"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'/consumo': consumoEnergetico})
        else:
            return not_found(start_response)


def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']


if __name__ == '__main__':
    print 'Listening on port http://0.0.0.0:8080 and on port 10843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8080), Application(),
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 10843)).serve_forever()
