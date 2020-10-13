$(document).on("click", ".item td img", function(){

	let trObj = $(this).closest("tr");

	if($(trObj).hasClass("checked")){
			$(trObj).removeClass("checked");
		} else {
			$(trObj).addClass("checked");
		}
	});

$(document).on('click', '#search', function (e){
   e.preventDefault();
   let form = $('form');
   $.ajax({
    type: "GET",
    url: "search",
    data: form.serialize(),
    dataType: "html",
    cache: false,
    success: function(data) {
      $('.results').append(data);
    }
  });
});