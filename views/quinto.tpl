<!DOCTYPE html>
<meta charset="utf-8">
<head>
	<script type="text/javascript" src="_static/js/odometer.min.js"></script>
	<script type="text/javascript" src="_static/js/socket.io.js"></script>
	<script type="text/javascript" src="_static/js/jquery-2.1.3.min.js"></script>
	<script type="text/javascript" src="_static/js/typed.js"></script>
	<script type="text/javascript" src="_static/css/components/bootstrap-sass-official/assets/javascripts/bootstrap.min.js"></script>
	<link href="_static/css/styles.min.css" rel="stylesheet">
	<link href="_static/css/odometer.css" rel="stylesheet">
</head>
<body>

<header class="navbar navbar-default navbar-static-top" id="top" role="navigation">
	<div class="header-gcba">
		<div class="header-inner">
			<div class="container">
				<a href="http://buenosaires.gob.ar" target="_blank">
					<div class="logo"></div>
				</a>
				<h2 class="slogan">En todo estás vos</h2>
			</div>
		</div>
	</div>
</header>

<div class="switch">
	<span class="labels-switch faded">2do</span>
	<input id="cmn-toggle-4" class="cmn-toggle cmn-toggle-round-flat" type="checkbox" checked="checked">
	<label for="cmn-toggle-4"></label>
	<span class="labels-switch">5to</span>
</div>



<div class="outer">
	<div class="middle">
		<div class="inner">
			<div class="contenidoTexto">
				<h1 id="estadoGeneral">Consumo energético</h1>
				<h2 id="fraseGeneral">5to Piso</h2>

				<div class="col-lg-9 col-md-9 col-sm-9 col-xs-12 warnings">
					<p id="valorAire"></p>
					<p id="valorLuz"></p>
					<p id="valorTomas"></p>
				</div>

				<div class="clear">
					<img id="carita" src="_static/img/emoticons_good.png"/>
				</div>
			</div>
			<div class="valores">
				<div id="valorTotal" class="odometer">0</div>
				<span class="badge">watts</span>
			</div>

		</div>
	</div>
</div>
<footer class="footer">
  <div class="container">
    <div class="row">
    <div class="col-md-8 ministerio definicion">
    	<span data-toggle="tooltip" data-placement="right" title="Lo que aprendés y ahorrás en el trabajo impacta en la energía de tu casa, los hospitales, los colegios, los comercios y la industria del país. Mejorar el consumo es tarea de todos. Proyecto desarrollado en Laboratorio de Gobierno en conjunto con Less Industries y Alexis Caporale. Si tenes dudas o consultas escribinos a gobiernoabierto @ buenosaires.gob.ar.">Eficiencia Energética en Edificios Públicos <span class="badge">?</span></span>
    </div>
    <div class="col-md-4 ministerio modernizacion">
    	Ministerio de Modernización
    </div>
    </div>
  </div>
</footer>
	<script type="text/javascript" src="_static/js/energia.js"></script>
</body>
