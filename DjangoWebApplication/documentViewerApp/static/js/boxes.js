$(document).ready(function(){

 $("[type=image").click(function(){  //effect on images when mouse hovering 
 			$(this).addClass("yellow");
 });


$("[type=image]").draggable(function(){
	drag: function(event){

	alert("dragstart");
	event.dataTransfer.setData("Text",event.target.id);

});

$("[#imagecontainer").drop(function(event){
	alert("drop");
	ev.preventDefault();
 });

$("#imagecontainer").dragover(function(event){
	alert("dragover");
	event.preventDefault();
	var dataa=ev.dataTransfer.getData("Text");
	event.target.appendChild(document.getElementById(dataa));
 });

});


