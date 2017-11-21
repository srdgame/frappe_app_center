$(document).ready(function() {
	$('.ui.segments .ui.basic.segment.no-padding-bottom .right.floated.header .ion-ios-arrow-up.icon.link').click(function(){
		if ($(this).hasClass('ion-ios-arrow-up')) {
			$('.ui.segments .ui.basic.segment.no-padding .flot-chart').hide();
			$(this).removeClass('ion-ios-arrow-up').addClass('ion-ios-arrow-down');
		} else {
			$('.ui.segments .ui.basic.segment.no-padding .flot-chart').show();
			$(this).removeClass('ion-ios-arrow-down').addClass('ion-ios-arrow-up');
		}
	});
	$('.ui.segments .ui.basic.segment.no-padding-bottom .right.floated.header .ion-ios-close-empty.icon.link').click(function() {
		$(this.parentNode.parentNode.parentNode).hide();
	});

	$('.ui.clearing.segment .right.floated.header .ion-ios-arrow-up.icon.link').click(function(){
		if ($(this).hasClass('ion-ios-arrow-up')) {
			$(this.parentNode.parentNode).find('.ui.grid').hide();
			$(this).removeClass('ion-ios-arrow-up').addClass('ion-ios-arrow-down');
		} else {
			$(this.parentNode.parentNode).find('.ui.grid').show();
			$(this).removeClass('ion-ios-arrow-down').addClass('ion-ios-arrow-up');
		}

	});

	$('.ui.clearing.segment .right.floated.header .ion-ios-close-empty.icon.link').click(function(){
		$(this.parentNode.parentNode).hide();
	});
});

