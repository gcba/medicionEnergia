var r = require('request');
var HOST = "http://52.10.233.24/v1/circuits/"
	, circuits = ["9061", "9062", "9063", "9064"];


/*
	los cuatros se actualizan al mismo tiempo?
	y sino, cual es el intervalo entre cada sensor?

	cuanto tiempo tarda el procesamiento de 4 request considerando que los 4 sensores se actualizan al mismo tiempo?
	sino se actualizan al mismo tiempo, segun la diferencia entre actualizacion de cada sensor, enviar la peticicion de
*/


setInterval(function(){
	console.log("################################")
	console.log("por solicitar 4 requests en menos de seis segundos")
	r({uri: HOST + circuits[0] + "/latest"}, function(err1, resp1, data1){
		r({uri: HOST + circuits[1] + "/latest"}, function(err2, resp2, data2){
			r({uri: HOST + circuits[2] + "/latest"}, function(err3, resp3, data3){
				r({uri: HOST+ circuits[3] + "/latest"}, function(err4, resp4, data4){
					console.log(data1)
					console.log(data2)
					console.log(data3)
					console.log(data4)
				})
			})
		})
	})
}, 6000)
