$(document).ready(function() {
	$('.ui.segments .ui.segment .right.floated.header .ion-ios-arrow-up.icon.link').click(function(){
		if ($(this).hasClass('ion-ios-arrow-up')) {
			$(this.parentNode.parentNode.parentNode).find('.ui.segment.content').hide();
			$(this).removeClass('ion-ios-arrow-up').addClass('ion-ios-arrow-down');
		} else {
			$(this.parentNode.parentNode.parentNode).find('.ui.segment.content').show();
			$(this).removeClass('ion-ios-arrow-down').addClass('ion-ios-arrow-up');
		}
	});
	$('.ui.segments .ui.segment .right.floated.header .ion-ios-close-empty.icon.link').click(function() {
		$(this.parentNode.parentNode.parentNode).hide();
	});

});

