var piso = $("button.active").text().split(" ")[0];
var objectivo_url = "static/data/objetivos" + piso + ".json";

var objetivos = (function() {
    var json = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': objectivo_url,
        'dataType': "json",
        'success': function (data) {
            json = data;
        }
    });
    return json;
})();

var socket = io.connect('/consumo', {
	'force new connection': true
});

var dias_semana = ["domingo", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado"];

socket.on('connect', function() {
    console.log("Connected.");
});

socket.on('consumo_total', function(data) {
	var ahora = new Date(),
		dia_semana = dias_semana[ahora.getDay()],
		hora_dia = ahora.getHours().toString();
	
	// Consumo en este momento
	var consumo_total = data.power_total,
		consumo_aire = data.power_aire,
		consumo_luz = data.power_luz,
		consumo_tomas = data.power_tomas;

	// Objetivo del current dia, a la current hora	
	var objetivo_total = objetivos[dia_semana][hora_dia].total,
		objetivo_aire = objetivos[dia_semana][hora_dia].aire,
		objetivo_luz = objetivos[dia_semana][hora_dia].luz,
		objetivo_tomas = objetivos[dia_semana][hora_dia].tomas;
	
	if (consumo_total > objetivo_total) {
		$("body").css("background-color", "#d32f2e");
	} else {
		$("body").css("background-color", "#8cc34b");
	}

	var texto_aire = "",
		texto_luz = "",
		texto_tomas = "";

	if (consumo_aire > objetivo_aire) {
		texto_aire = "Consumo Aire: " + Math.round(consumo_aire) + ". Objetivo Aire: " + objetivo_aire + ". ";
		
		if (data.clima == "Soleado") {
			texto_aire += "Sabemos que hace calor, pero";
		} else {
			texto_aire += "Guachín, ni siquiera hace calor y";
		}

		texto_aire += " estás pasado con el aire.";
	} 

	if (consumo_luz > objetivo_luz) {
		texto_luz = "Consumo Luz: " + Math.round(consumo_luz) + ". Objetivo Luz: " + objetivo_luz + ". ";
		
		if (data.clima == "Soleado") {
			texto_luz += "Sabemos que hace calor, pero";
		} else {
			texto_luz += "Guachín, ni siquiera hace calor y";
		}

		texto_luz += " estás pasado con la luz.";
	}

	if (consumo_tomas > consumo_tomas) {
		texto_tomas = "Consumo Tomas: " + Math.round(consumo_tomas) + ". Objetivo Tomas: " + consumo_tomas + ". ";
		
		if (data.clima == "Soleado") {
			texto_tomas += "Sabemos que hace calor,";
		} else {
			texto_tomas = "Guachín, ni siquiera hace calor y";
		}

		texto_aire += " estás pasado con las tomas.";
	}

	$("#valorTotal").text(Math.round(consumo_total));
	$("#valorAire").text(texto_aire);
	$("#valorLuz").text(texto_luz);
	$("#valorTomas").text(texto_tomas);

	console.log(data);

});

socket.on('error', function(e){
	console.log("error")
})

socket.on('disconnect', function(e){
	console.log("Disconnect.")
})