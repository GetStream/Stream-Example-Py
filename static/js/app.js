var App = function () {
    this.initialize.apply(this, arguments);
};

App.prototype = {
    initialize: function() {
        var that = this;
        $('form.create-destroy').submit($.proxy(this.toggleFormSubmit, this));
    },
    lockForm: function($form) {
        var $btn = $form.find('input[type="submit"]');
        $btn.prop('disabled', true);
    },
    toggleFormState: function() {
        var $btn = this.find('input[type="submit"]');
        $btn.prop('disabled', false);
        var text = $btn.val();
        var toggle = $btn.data('toggle');
        $btn.data('toggle', text);
        $btn.val(toggle);
        if (this.find('input[name="remove"]').length > 0) {
            this.find('input[name="remove"]').remove();
            $btn.removeClass('btn-danger');
        }
        else {
            this.append('<input name="remove" type="hidden" value="1"> ');
            $btn.addClass('btn-danger');
        }
    },
    toggleFormSubmit: function(event) {
        var $form = $(event.target);
        $.ajax({
            type: "POST",
            url: $form.attr('action'),
            data: $form.serialize(),
            success: $.proxy(this.toggleFormState, $form)
        });
        this.lockForm($form);
        return false;
    }
}

window.app = new App();
