$(document).ready(function() {
    jQuery.expr[':'].icontains = function(a, i, m) {
        return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
    };

    /* Initial treatment */
    $('#input_product').val('');
    $('#input_product').focus();

    /* Product search typing event */
    $('#input_product').on('input', function() {
        let typed = $(this).val();
        if (typed.trim() == '') {
            $('.tab-pane tbody tr').show();
        } else {
            $('.tab-pane tbody tr').hide();
            $('.tab-pane tbody tr:icontains("' + typed + '")').show();
        }
    });
});