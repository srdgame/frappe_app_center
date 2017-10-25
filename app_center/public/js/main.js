$(document).ready(function() {
    $('a[data-toggle="popup"]').each(function() {
        $(this).popup({
            popup: $(this).attr('data-content'),
            position: $(this).attr('data-position'),
            on: 'click'
        })
    });

    $('a[data-toggle="slide"]').on('click', function(e) {
        e.preventDefault();

        var target = this.hash;
        var $target = $(target);

        $('html, body').stop().animate({
            'scrollTop': $target.offset().top - 60
        }, 900, 'swing');
    });

    $('#verticalMenu').niceScroll({ cursorcolor: "transparent" });
    $('.ui.accordion').accordion();
    $('.ui.dropdown').dropdown();
    $('.ui.checkbox').checkbox();
    $('.ui.progress').progress();

    $('#showToggle').hide();
    $('#hideToggle').show();
    $('#hideToggle').click(function() {
        $('#hideToggle').hide();
        $('#showToggle').show();
        $('#sideMenu').addClass('hide');
    });
    $('#showToggle').click(function() {
        $('#showToggle').hide();
        $('#hideToggle').show();
        $('#sideMenu').removeClass('hide');
    });

    $.ajaxSetup( {
		headers: { // 默认添加请求头
			"X-Frappe-CSRF-Token": frappe.csrf_token,
		}
	} );

	$('.menu.transition .item').click(function () {
	    var lang = $(this).attr("language");

		var userinfo = {
			"language": lang,
			"doctype": "User",
			"name":frappe.user
		};

		var postdata = {
			"data": JSON.stringify(userinfo),
			"web_form": "edit-profile",
			"cmd": "frappe.website.doctype.web_form.web_form.accept"
		};
		$.ajax({
			type: 'POST',
			url: "/",
			contentType: "application/x-www-form-urlencoded", //必须有
			data: postdata,
			dataType: "json",
			success: function (r) {
				if (r.message) {
					window.location.reload();
				}
			},
			error: function () {
				console.log("异常!");
			}
		});
	});
});
