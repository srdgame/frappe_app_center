function on_app_form_success() {
	setTimeout(function() {
		window.location.href = "/app_list";
	}, 2000);
};
$(document).ready(function() {
	$("#icon_file").change(function(event){
		var name=$(this).attr("name");
		var val = $(this).val();
		var tmppath = URL.createObjectURL(event.target.files[0]);
		$('.ui.image.button .image').attr('src', tmppath);
	});
});