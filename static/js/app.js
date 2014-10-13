var App = function() {
	this.initialize.apply(this, arguments);
};

App.prototype = {
	initialize : function() {
		var that = this;
		$('form.create-destroy').submit($.proxy(this.toggleFormSubmit, this));
		$('#notification-toggle').click(function() {
			$.get("/notification_feed/", function(data) {
				$("#notification-container").html(data);
			});
		});
        setTimeout(that.autofollow, 1000);
	},
    autofollow: function() {
        $.ajax({
            type : "get",
            url : '/auto_follow/'
        });
    },
	lockForm : function($form) {
		var $btn = $form.find('input[type="submit"]');
		$btn.prop('disabled', true);
	},
	toggleFormState : function() {
		var $btn = this.find('input[type="submit"]');
		$btn.prop('disabled', false);
		var text = $btn.val();
		var toggle = $btn.data('toggle');
		$btn.data('toggle', text);
		$btn.val(toggle);
		if (this.find('input[name="remove"]').length > 0) {
			this.find('input[name="remove"]').remove();
			$btn.removeClass('btn-danger');
		} else {
			this.append('<input name="remove" type="hidden" value="1"> ');
			$btn.addClass('btn-danger');
		}
	},
	toggleFormSubmit : function(event) {
		var $form = $(event.target);
		$.ajax({
			type : "POST",
			url : $form.attr('action'),
			data : $form.serialize(),
			success : $.proxy(this.toggleFormState, $form)
		});
		this.lockForm($form);
		return false;
	}
};

window.app = new App();
app.Realtime = function() {
	this.initialize.apply(this, arguments);
};

app.Realtime.prototype = {
	initialize : function(feedId, token, elementIdentifier) {
		this.feedId = feedId;
		this.token = token;
		this.elementIdentifier = elementIdentifier;
		this.client = streamClient;
		this.feed = this.client.feed(feedId, this.token);
		var scope = this;
		function changeBound() {
			return scope.changed.apply(scope, arguments);
		}


		this.feed.subscribe(changeBound);
		this.element = $(elementIdentifier);
	},
	changed : function(data) {
		var unseen = data.unseen;
		this.element.html(unseen);
		if (unseen == 0) {
			this.element.hide();
		} else {
			this.element.show();
		}
	}
};
