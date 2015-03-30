<!DOCTYPE html>
<meta charset="utf-8">
<head>
	<script type="text/javascript" src="_static/js/odometer.min.js"></script>
	<script type="text/javascript" src="_static/js/socket.io.js"></script>
	<script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
	<link href="_static/css/odometer.css" rel="stylesheet">
	<link href="_static/css/bootstrap.min.css" rel="stylesheet">
	<link href="_static/css/styles.css" rel="stylesheet">
</head>
<body>
	<div class="botones-pisos btn-group btn-group-lg" role="group" aria-label="...">
	  <a href="/segundo"><button type="button" class="btn btn-default active">2do Piso</button></a>
	  <a href="/quinto"><button type="button" class="btn btn-default">5to Piso</button></a>
	</div>
	<div class="outer">
		<div class="middle">
			<div class="inner">
				<div class="contenidoTexto">
					<h1 id="estadoGeneral">Consumo energético</h1>
					<h2 id="fraseGeneral">2do Piso</h2>
					
					<div class="col-lg-9 col-md-9 col-sm-9 col-xs-12 warnings text-center">
						<p id="valorAire"></p>
						<p id="valorLuz"></p>
						<p id="valorTomas"></p>
					</div>

					<div class="clear">
						<img id="carita" src="_static/img/emoticons_good.png"/>
					</div>
				</div>
				<div id="valorTotal" class="odometer"></div>	
			</div>
		</div>
	</div>
	<div id="footer">
		<p>Eficiencia Energética en Edificios Públicos. Lo que aprendés y ahorrás en el trabajo impacta en la energía de tu casa, los hospitales, los colegios, los comercios y la industria del país. Mejorar el consumo es tarea de todos. Proyecto desarrollado en Laboratorio de Gobierno en conjunto con Less Industries y Alexis Caporale. Si tenes dudas o consultas escribinos a gobiernoabierto @ buenosaires.gob.ar .</p>
	</div>

	<script type="text/javascript" src="_static/js/energia.js"></script>
</body>
