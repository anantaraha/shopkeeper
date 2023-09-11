$(document).ready(function() {
    $('#btn_return').click(function() {
        location.replace('/shop/cart/');
    });
    $('#btn_print').click(function printMemo() {
        let content = $('#memo_content').html();
        let openWindow = window.open("", "title", "attributes");
        openWindow.document.write(content);
        openWindow.document.close();
        openWindow.focus();
        openWindow.print();
        openWindow.close();
    });
})