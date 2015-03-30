var piso = $("button.active").text().split(" ")[0];
var objectivo_url = "_static/data/objetivos" + piso + ".json";

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

socket.on('connect', function() {
    console.log("Connected.");
	socket.emit('receive', piso);
});

var dias_semana = ["domingo", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado"];

socket.on('consumo_total', function(data) {	
	var clima = data.clima;

	var ahora = new Date(),
		dia_semana = dias_semana[ahora.getDay()],
		hora_dia = ahora.getHours().toString();
	
	// Consumo en este momento
	var consumo_total = data.power_total,
		consumo_aire = data.power_aire,
		consumo_luz = data.power_luz,
		consumo_tomas = data.power_tomas;

	// PARA DEBUGGING
	// var consumo_total = 100,
	// 	consumo_aire = 50,
	// 	consumo_luz = 30,
	// 	consumo_tomas = 20;

	// Objetivo del current dia, a la current hora	
	var objetivo_total = objetivos[dia_semana][hora_dia].total,
		objetivo_aire = objetivos[dia_semana][hora_dia].aire,
		objetivo_luz = objetivos[dia_semana][hora_dia].luz,
		objetivo_tomas = objetivos[dia_semana][hora_dia].tomas;

	// PARA DEBUGGING
	// var objetivo_total = 0,
	// 	objetivo_aire = 0,
	// 	objetivo_luz = 0,
	// 	objetivo_tomas = 0;
	
	if (consumo_total > objetivo_total) {
		$("body").css("background-color", "#d32f2e");
		$("h1#estadoGeneral").text("¡Atención!");
		$("h2#fraseGeneral").text("El consumo de la oficina es más alto que el permitido. ¡Tienen que bajarlo!");
		$(".warnings").show();
	} else {
		$("body").css("background-color", "#8cc34b");
		$("h1#estadoGeneral").text("¡Bien!");
		$("h2#fraseGeneral").text("El consumo de la oficina está dentro de los valores permitidos. ¡Sigan así!");
		$(".warnings").hide();
	}

	var texto_aire = "",
		texto_luz = "",
		texto_tomas = "";

	console.log(data);

	if (consumo_aire > objetivo_aire) {
		texto_aire += "Los aires acondicionados están consumiendo más de lo permitido. ¿Están en 24°C? ¿Son todos necesarios? ";
		if (clima) {
			if (clima.temp > 25) {
				texto_aire += "Hace calor, sí, pero pueden mejorar el consumo. ";
				if (clima.cielo != "Soleado" || clima.cielo != "Parcialmente soleado") {
					texto_aire += "¡Está nublado! ";
				}
			} else {
				texto_aire += "¡No hace calor! ";
				if (clima.cielo != "Soleado" || clima.cielo != "Parcialmente soleado") {
					texto_aire += "¡Está nublado! ";
				}
				texto_aire += "Pueden mejorar el consumo.";
			}	
		}
	} 

	if (consumo_luz > objetivo_luz) {
		texto_luz += "Las luces de la oficina están consumiendo más de lo permitido. ¿No hay ninguna prendida sin necesidad? ";
		if (clima) {
			if (clima.cielo == "Soleado" || clima.cielo == "Parcialmente soleado") {
				texto_luz += "El día está soleado, la luz natural ayuda a bajar el consumo. ";
			} else {
				texto_luz += "El día está nublado, sí, pero pueden mejorar el consumo. ";
			}	
		}
	}

	if (consumo_tomas > objetivo_tomas) {
		texto_tomas = "Las computadoras, dispensers de agua, impresoras, televisores y otros aparatos electrónicos enchufados a la pared están consumiendo más de lo permitido. ¿No hay ninguno prendido sin necesidad? Pueden mejorar el consumo. ";
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