var outerWidth = 200
var outerHeight = 200
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = outerWidth - margin.left - margin.right,
    height = outerHeight - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .tickFormat(d3.format("d"))
    .ticks(d3.max([real_votes, bogus_votes, unknown_votes]))
    .tickSize(10)
    .scale(y)
    .orient("left");

var svg = d3.select("#barplot").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var data = [{x: 'Real',    y: real_votes},
		    {x: 'Bogus',   y: bogus_votes},
	        {x: 'Unknown', y: unknown_votes}];

x.domain(data.map(function(d) { return d.x; }));
y.domain([0, d3.max(data, function(d) { return +d.y; })]);
  		
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
.text("Votes");

svg.selectAll(".bar")
.data(data)
.enter().append("rect")
.attr("class", "bar")
.attr("x", function(d) { return x(d.x); })
.attr("width", x.rangeBand())
.attr("y", function(d) { return y(+d.y); })
.attr("height", function(d) { return height - y(+d.y); });
