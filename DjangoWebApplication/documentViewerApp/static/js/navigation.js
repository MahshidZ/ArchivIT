

PAGE_WIDTH = 400;
PAGE_HEIGHT = 300;
FIRST_BOX_X_MARGIN = 10 ;
FIRST_BOX_Y_MARGIN = 20;
BOX_WIDTH = 40;
BOX_BORDER_RADUIS = '.35em';
BOX_X_PADDING = 10;
BOX_Y_PADDING = 10;
BOX_COLOR_OPACITY = '.3';
BOX_STROKE_WIDTH = '1.5px';
BOX_TEXT_OVERSIZE = 20;
VERTICAL_DISTANCE_BETWEEN_BOXES = 50;

var canvas = d3.select('#leftmenu').append('svg')
	.attr('height', PAGE_WIDTH)
	.attr('width', PAGE_HEIGHT)
  .append("g")
  .attr("transform", "translate(" + FIRST_BOX_X_MARGIN + "," + FIRST_BOX_Y_MARGIN + ")");

var treeData = [
    {
        "name": "Thumbnail Maker",
        "pageaddress": "/documentViewerApp/thumbnailmaker",
        "x": 10,
        "y": 60,
        "parent": "null",
        "children": [
            {
                "name": "Input Data",
                "pageaddress": "/documentViewerApp/InputData",
                "x": 10,
                "y": 80,
                "parent": "Thumbnail Maker",
                "children": [
                    {
                        "name": "Clustering",
                        "pageaddress": "/documentViewerApp/categoriesall",
                        "x": 10,
                        "y": 100,
                        "parent": "Input Data",
                        "children": [
                    {
                        "name": "Training Set Builder",
                        "pageaddress": "/documentViewerApp/TrainingSetBuild",
                        "x": 10,
                        "y": 120,
                        "parent": "Clustering",
                        "children": [
                    {
                        "name": "Classification",
                        "pageaddress": "/documentViewerApp/Classification",
                        "x": 10,
                        "y": 140,
                        "parent": "Training Set Builder"
                    },
                    {
                        "name": "Evaluation",
                        "pageaddress": "/documentViewerApp/Evaluation",
                        "x": 20,
                        "y": 100,
                        "parent": "Training Set Builder"
                    }

                ]
                    }
                ]
                    }
                ]
            }
        ]
    }
];
  
var i = 0;
var tree = d3.layout.tree()
  .size([180, 10]);
 
var diagonal = d3.svg.diagonal()
  .projection(function(d) { return [d.x, d.y]; });
  
root = treeData[0];
update(root);
 
function update(source) {
 
  // Compute the new tree layout.
  var nodes = tree.nodes(root).reverse(),
      links = tree.links(nodes);
 
  // Normalize for fixed-depth.
  nodes.forEach(function(d) { d.y = d.depth * BOX_WIDTH ; })
  nodes.forEach(function(d) { d.w = d.name.length * 5 + 20 ; });
 
  // Declare the nodes…
  var node = canvas.selectAll("g.node")
    .data(nodes, function(d) { return d.id || (d.id = ++i); });
 
  // Enter the nodes.
  var nodeEnter = node.enter().append("g")
    .attr("class", "node")
    .attr("transform", function(d) { 
      return "translate(" + d.x + "," + d.y + ")" });
 
  nodeEnter.append("a")
    .attr('xlink:href' , function(d){return d.pageaddress})
      .append('rect')
        .attr("width", function(d){return d.w})
        .attr("height", "20")

  nodeEnter.append('a')
     .attr('xlink:href' , function(d){return d.pageaddress})
 
  nodeEnter.append("text")
    .attr("x", function(d) { 
      return d.x })
    .attr("dy", ".35em")
    .attr("text-anchor", function(d) { 
      return d.children || d._children ? "end" : "start"; })
    .text(function(d) { return d.name; });
 
  // Declare the links…
  var link = canvas.selectAll("path.link")
    .data(links, function(d) { return d.target.id; });
 
  // Enter the links.
  link.enter().insert("path", "g")
    .attr("class", "link")
    .attr("d", diagonal);
 
}
 


