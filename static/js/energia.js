var piso = "5to";
if (!$("#cmn-toggle-4").prop("checked")){
	piso = "2do";
}
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

// Event handler - cambio de piso
$("#cmn-toggle-4").on("change", function(){
	// Si se vuelve checked, redirect at 5to piso
	if($(this).prop("checked")) {
		document.location.href = '/quinto';
	} else {
		document.location.href = '/segundo';
	}
});


/****************
 * NOTIFICACIONES DE HORARIOS
 ****************/

var end_of_day = "Son las 18hs, hora de fijarse que nada quede prendido innecesariamente a la noche. ¿Luces? ¿Aires? ¿Computadoras? ¿Dispensers?",
	end_of_viernes = "¡Cuidado! No dejar nada prendido innecesariamente el fin de semana",
	start_of_day = "Buen día. ¿Había algo prendido innecesariamente cuando llegaron a la oficina? Por favor, dejarlo asentado en el documento compartido del proyecto.";

//the window reload function. you could of course do anything here
function displayNotificacion(hora) {
    if(! ('Notification' in window) ){
		alert('Web Notification is not supported');
		return;
	}

	Notification.requestPermission(function(permission){
		var texto_notification = "";
		switch(hora){
			case 1830:
				texto_notification = end_of_viernes;
				break;
			case 18:
				texto_notification = end_of_day;
				break;
			case 830:
				texto_notification = start_of_day;
				break;
		}
		var notification = new Notification("Consumo Energético",{body:texto_notification});
	});
}

//helper function to build up the desire time trigger
function getTargetTime(hour,minute) {
  var t = new Date();
  t.setHours(hour);
  t.setMinutes(minute);
  t.setSeconds(0);
  t.setMilliseconds(0);
  return t;
}

//get your offset to wait value
var day_today = new Date().getDay();
var timenow =  new Date().getTime();
var timetarget_1830 = getTargetTime(18,30).getTime(),
	timetarget_18 = getTargetTime(18,0).getTime(),
	timetarget_830 = getTargetTime(8,30).getTime();
var offsetmilliseconds_1830 = timetarget_1830 - timenow,
	offsetmilliseconds_18 = timetarget_18 - timenow,
	offsetmilliseconds_830 = timetarget_830 - timenow;

//set the timeouts for the horas
if (offsetmilliseconds_1830 >= 0 && day_today == 5){
	setTimeout(function(){displayNotificacion(1830);}, offsetmilliseconds_1830);
}
if (offsetmilliseconds_18 >= 0){
	setTimeout(function(){displayNotificacion(18);}, offsetmilliseconds_18);
}
if (offsetmilliseconds_830 >= 0){
	setTimeout(function(){displayNotificacion(830);}, offsetmilliseconds_830);
}

/****************
 * SOCKET
 ****************/

var socket = io.connect('/consumo', {
	'force new connection': true
});

socket.on('connect', function() {
    console.log("Connected.");
	socket.emit('receive', piso);
});

socket.on('consumo_total', function(data) {
	// no sacar console.log , porque si lo pones abajo y antes aparece un error, me corta el debug
	console.log(data);

	// Consumo en este momento
	var consumo_total = data.power_total;
	var clima = data.clima;
	var notificaciones = data.notificaciones;
	var estoy_pasado = data.estoy_pasado;

	if (notificaciones.length > 0) {
		if(! ('Notification' in window) ){
			alert('Web Notification is not supported');
			return;
		}

		Notification.requestPermission(function(permission){
			var notification = new Notification("Consumo energético",{body:notificaciones[0]});
		});
	}

	if (estoy_pasado.total) {
		$("body").css("background-color", "#d32f2e");
		$("h1#estadoGeneral").text("¡Atención!");
		$("h2#fraseGeneral").html("El consumo de la oficina es más alto que el permitido." + "<br/>" +  "¡Tienen que bajarlo!");
		$(".warnings").show();
		$("#carita").attr("src", "_static/img/emoticons_bad.png");
	} else {
		$("body").css("background-color", "#8cc34b");
		$("h1#estadoGeneral").text("¡Bien!");
		$("h2#fraseGeneral").html("El consumo de la oficina está dentro de los valores permitidos." + "<br/>" +  "¡Sigan así!");
		$(".warnings").hide();
		$("#carita").attr("src", "_static/img/emoticons_good.png");
	}

	var texto_aire = "",
		texto_luz = "",
		texto_tomas = "";

	if (estoy_pasado.aire) {
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

	if (estoy_pasado.luces) {
		texto_luz += "Las luces de la oficina están consumiendo más de lo permitido. ¿No hay ninguna prendida sin necesidad? ";
		if (clima) {
			if (clima.cielo == "Soleado" || clima.cielo == "Parcialmente soleado") {
				texto_luz += "El día está soleado, la luz natural ayuda a bajar el consumo. ";
			} else {
				texto_luz += "El día está nublado, sí, pero pueden mejorar el consumo. ";
			}
		}
	}

	if (estoy_pasado.tomas) {
		texto_tomas = "Las computadoras, dispensers de agua, impresoras, televisores y otros aparatos electrónicos enchufados a la pared están consumiendo más de lo permitido. ¿No hay ninguno prendido sin necesidad? Pueden mejorar el consumo. ";
	}

	$("#valorTotal").text(Math.round(consumo_total));
	$("#valorAire").typed({
	    strings: [texto_aire],
	    contentType: 'html',
	    callback: function() {
	    	$("#valorLuz").typed({
			    strings: [texto_luz],
			    contentType: 'html',
			    callback: function() {
			    	$("#valorTomas").typed({
					    strings: [texto_tomas],
					    contentType: 'html' // or 'text'
					});
			    }
			});
	    }
	});

	console.log(data);

});

socket.on('error', function(e){
	console.log("error")
})

socket.on('disconnect', function(e){
	console.log("Disconnect.")
})

/****************
 * TOOLTIP BOOTSTRAP
 ****************/

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})