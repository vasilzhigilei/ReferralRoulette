$(document).ready(function() {
    $('.js-example-basic-single').select2({
        theme: "bootstrap4",
        placeholder: 'Search here...',
        allowClear: true,
    });
    $('b[role="presentation"]').hide();
});