
$(document).ready(function() {
	// For issue detail page
	$('.ui.items .item .content .extra .primary.button').click(function () {
		var name = $(this).data('name');
		$('.ui.issue_action.comment.form input[name="issue"]').val(name);
		$('.ui.issue_action.comment.form input[name="action"]').val("Closed");
		$('.ui.issue_action.modal .header').html('{{_("Issue fixed")}}');
		$('.ui.issue_action.modal')
			.modal({
				closable: true
			})
			.modal('show')
		;
	});
	$('.ui.items .item .content .extra .cancel.button').click(function () {
		var name = $(this).data('name');
		$('.ui.issue_action.comment.form input[name="issue"]').val(name);
		$('.ui.issue_action.comment.form input[name="action"]').val("Invalid");
		$('.ui.issue_action.modal .header').html('{{_("Invalid issue")}}');
		$('.ui.issue_action.modal')
			.modal({
				closable: true
			})
			.modal('show')
		;
	});

	$('.ui.issue_action.comment.form').ajaxForm({
		dataType: 'json',
		resetForm: true,
		beforeSend: function() {
			console.log('Ajax Form Before Send!');
		},
		success: function(response, status, xhr, form) {
			form.find('.ui.success.message').html('Done!');
			form.addClass('success');
			var tab = $(".ui.tabular.menu .active.item").data("tab");
			setTimeout(function() {
				window.location.reload(false);
			}, 1000);
		},
		complete: function(xhr) {
		},
		error: function(xhr, status, error, form) {
			console.log('Form Exception:' + xhr.responseText);
			form.addClass('error');
			form.find('.ui.error.message').html(xhr.responseText);
			if (xhr.responseJSON._server_messages) {
				var _server_messages = JSON.parse(xhr.responseJSON._server_messages);
				form.find('.ui.error.message').html(_server_messages[0]);
			} else {
				var exc = JSON.parse(xhr.responseJSON.exc);
				form.find('.ui.error.message').html(exc);
			}
		}
	});
});

