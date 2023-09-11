$(document).ready(function () {
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    let date = new Date();
    let date_text = months[date.getMonth()] + ' ' + date.getDate();
    let day_text = days[date.getDay()];
    $('#date_text').text(date_text);
    $('#day_text').text(day_text);
});