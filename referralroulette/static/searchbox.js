$(document).ready(function() {
    $('#searchbox').select2({
        theme: "bootstrap4",
        placeholder: 'Search here...',
        allowClear: true,
    });
    $('b[role="presentation"]').hide();
    $('#searchbox').on('select2:select', function(e) {
        window.location.href = '../for/' + e.params.data['id'];
    });
});