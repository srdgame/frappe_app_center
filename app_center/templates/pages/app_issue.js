
$(document).ready(function() {
	// For issue detail page
	$('.ui.feed .event .meta .fix').click(function () {
		$('.ui.issue_action.comment.form input[name="action"]').val("Closed");
		$('.ui.issue_action.modal .header').html('{{_("Issue fixed")}}');
		$('.ui.issue_action.modal')
			.modal({
				closable: true
			})
			.modal('show')
		;
	});
	$('.ui.feed .event .meta .invalid').click(function () {
		$('.ui.issue_action.comment.form input[name="action"]').val("Invalid");
		$('.ui.issue_action.modal .header').html('{{_("Invalid issue")}}');
		$('.ui.issue_action.modal')
			.modal({
				closable: true
			})
			.modal('show')
		;
	});
});