import urllib
import json
import time
r = []


borneras = ["9061", "9062", "9063", "9013", "9015", "9071", "9072", "9073", "9074", "9075", "9014", "9016"]

while True:

	r = []
	print 30 * "#"
	for i in borneras:
		response = urllib.urlopen("http://52.10.233.24/v1/circuits/{0}/latest".format(i))
		result = json.load(response)
		#print result['data'][0]['proc']
		r.append(result['data'][0]['proc']["power"])
	end = sum(r)
	print end