var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .rangeRound([height, 0]);

var color = d3.scale.ordinal()
    .range(["#1977DD", "#47E4C2", "#522CA6"]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .tickFormat(d3.format(".2s"));

var svg = d3.select("#bar-graph").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv("static/data/5tocategorias.csv", function(error, data) {
  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Fecha"; }));

  data.forEach(function(d) {
    var y0 = 0;
    d.categorias = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
    d.total = d.categorias[d.categorias.length - 1].y1;
  });

  x.domain(data.map(function(d) { return d.Fecha; }));
  y.domain([0, d3.max(data, function(d) { return d.total; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Consumo");

  var dia = svg.selectAll(".dia")
      .data(data)
    .enter().append("g")
      .attr("class", "g")
      .attr("transform", function(d) { return "translate(" + x(d.Fecha) + ",0)"; });

  var tooltip = d3.select("#bar-graph").append("div")   
    .attr("class", "tooltip")               
    .style("opacity", 0)
    .style("background-color", "white")
    .style("color", "black")
    .style("padding", "20px");

dia.selectAll("rect")
    .data(function(d) { return d.categorias; })
    .enter().append("rect")
        .attr("class", function(d) { return d.name })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.y1); })
        .attr("height", function(d) { return y(d.y0) - y(d.y1); })
        .style("fill", function(d) { return color(d.name); })
        .on("mouseover", function(d) {      
            tooltip.transition()        
                .duration(100)      
                .style("opacity", .9);      
                tooltip.html(d.name + ": " + -1*(d.y0-d.y1) + "w");
            d3.selectAll($("rect:not(." + $(this).attr("class") + ")"))
                .style("opacity", 0.3);
            })
        .on("mouseout", function(d) {       
            tooltip.transition()        
                .duration(200)      
                .style("opacity", 0);
            d3.selectAll("rect").style("opacity", 1);
            })
        .on("mousemove", function(){
            return tooltip.style("top", (event.pageY-10)+"px")
                    .style("left",(event.pageX+10)+"px");});

  var legend = svg.selectAll(".legend")
      .data(color.domain().slice().reverse())
    .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 18)
      .attr("height", 18)
      .attr("class", function(d) { return d; })
      .style("fill", color);

  legend.append("text")
      .attr("x", width - 24)
      .attr("y", 9)
      .attr("dy", ".35em")
      .attr("class", function(d) { return d; })
      .style("text-anchor", "end")
      .text(function(d) { return d; });

});