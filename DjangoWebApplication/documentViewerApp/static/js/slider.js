


$(document).ready(function(){

	$("[type=range]").change(function(){
		var newv=$(this).val();
		$(this).next().text(newv);
	});

});


