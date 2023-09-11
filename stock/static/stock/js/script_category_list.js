$(document).ready(function() {
    jQuery.expr[':'].icontains = function(a, i, m) {
        return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
    };

    /* Initial treatment */
    $('#input_category').val('');
    $('#input_category').focus();

    /* Category search typing event */
    $('#input_category').on('input', function() {
        let typed = $(this).val();
        if (typed.trim() == '') {
            $('#category_list tbody tr').show();
        } else {
            $('#category_list tbody tr').hide();
            $('#category_list tbody tr:icontains("' + typed + '")').show();
        }
    });
});