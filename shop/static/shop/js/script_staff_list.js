$(document).ready(function() {
    jQuery.expr[':'].icontains = function(a, i, m) {
        return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
    };

    /* Initial treatment */
    $('#input_staff').val('');
    $('#input_staff').focus();

    /* Staff search typing event */
    $('#input_staff').on('input', function() {
        let typed = $(this).val();
        if (typed.trim() == '') {
            $('#staff_list tbody tr').show();
        } else {
            $('#staff_list tbody tr').hide();
            $('#staff_list tbody tr:icontains("' + typed + '")').show();
        }
    });
});