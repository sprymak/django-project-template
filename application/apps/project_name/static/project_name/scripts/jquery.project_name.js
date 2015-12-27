(function ($) {

    var settings = {};

    $.fn.{{ project_name }} = function (options) {
        var element;
        settings = $.extend(settings, options);
        element = $(this);
        return this;
    };

})(jQuery);
