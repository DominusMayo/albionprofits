$(document).on("click", ".item td img", function(e){

		var itemId = $(this).attr("data-item-id"),
			trObj = $(this).closest("tr");

		if($(trObj).hasClass("checked")){
			$(trObj).removeClass("checked");
		} else {
			$(trObj).addClass("checked");
		}
	});