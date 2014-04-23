

var canvas= d3.select("#content").append("svg")
	.attr("height",600)
	.attr("width", 400);

var yposition=50;
var xposition=250;


var text = canvas.append("text")
	.attr("y", yposition)
	.attr("x", xposition)
	.attr("width", 300)
    .attr("dy", ".35em")
    .attr("text-anchor", "middle")
    .style("font", "20 50px Helvetica Neue")
    .text("   Start  ");

var bbox = text.node().getBBox();
var lineData = [
{"x": bbox.x-10, "y": yposition }
 ];


var rectangle = canvas.append("a").attr("xlink:href" , "/documentViewerApp/thumbnailmaker").append("rect")
 	.attr("x", bbox.x-10)
    .attr("y", bbox.y-10)
	.attr("width", bbox.width+20)
	.attr("height", bbox.height+20)
    .style("fill", "#ccc")
    .style("fill-opacity", ".3")
    .style("stroke", "#666")
    .style("stroke-width", "1.5px");

