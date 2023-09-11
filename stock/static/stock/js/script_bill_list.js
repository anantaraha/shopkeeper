$(document).ready(function() {
    jQuery.expr[':'].icontains = function(a, i, m) {
        return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
    };

    /* Initial treatment */
    $('#input_bill').val('');
    $('#input_bill').focus();

    /* Bill search typing event */
    $('#input_bill').on('input', function() {
        let typed = $(this).val();
        if (typed.trim() == '') {
            $('#bill_list tbody tr').show();
        } else {
            $('#bill_list tbody tr').hide();
            $('#bill_list tbody tr:icontains("' + typed + '")').show();
        }
    });
});