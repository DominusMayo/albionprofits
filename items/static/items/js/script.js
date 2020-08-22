$(document).on("click", ".item td img", function(){

	let trObj = $(this).closest("tr");

	if($(trObj).hasClass("checked")){
			$(trObj).removeClass("checked");
		} else {
			$(trObj).addClass("checked");
		}
	});