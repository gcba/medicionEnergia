import json
import csv
from datetime import datetime
import urllib
import sys

def epochhuman(epoch):
	dt = datetime.fromtimestamp(epoch / 1000)
	s = dt.strftime('%Y-%m-%d %H:%M:%S')
	return s 
		
#quinto piso
borneras_aire_5t = ["9061", "9062", "9063"]
borneras_luz_5t = ["9014", "9016"]
borneras_tomas_5t = ["9013", "9015", "9064", "9071", "9072", "9074", "9075"]
#segundo piso
borneras_aire_2d = ["9031", "9033", "9035"]
borneras_luz_2d = ["9021", "9022", "9023"]
borneras_tomas_2d = ["9034", "9051", "9052", "9053", "9054", "9055", "9056"]

quintopiso = borneras_aire_5t + borneras_luz_5t + borneras_tomas_5t
segundopiso = borneras_aire_2d + borneras_luz_2d + borneras_tomas_2d

def main(desde, hasta):

	for n in quintopiso + segundopiso:
		url = "http://52.10.233.24/v1/circuits/{0}/latest/{1}/{2}".format(n, desde, hasta)
		print "cargando... url"
		print url

		res = urllib.urlopen(url)
		filejson = json.load(res)
		
		__file = "{0}_{1}_{2}.csv".format(n, desde, hasta)
		f = csv.writer(open(__file, "wb+"))
		
		print "cargando... file"
		print __file

		f.writerow(["vrms", "irms", "power", "timestamp"])

		for i in range(filejson['total']):
		    f.writerow([
						filejson['data'][i]['proc']['vrms'],
						filejson['data'][i]['irms'],
						filejson['data'][i]['power'],
						epochhuman(filejson['data'][i]['collector_timestamp'])
			])

		del filejson
		del f
		print "fin {0}".format(__file)
		del __file

if __name__ == '__main__':
	"""
		Ejemplo , modo de uso.
			formato epoch referencia epochconverter.com

		python gethistorico.py
		Ingresar en formato epoch: desde hasta: 1426862657000 1427467457000
	"""
	sys.argv = raw_input('Ingresar en formato epoch en milisegundos: desde hasta: ').split()
	args = sys.argv
	main(args[0], args[1])