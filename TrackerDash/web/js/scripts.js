$(document).ready(function ()   {
    // But there is a little problem
    // we need to pad 0-9 with an extra
    // 0 on the left for hours, seconds, minutes

    var pad_time_value = function(x) {
        return x < 10 ? '0'+x : x;
    };

    var updateClock = function() {
        var d = new Date();
        var hours = pad_time_value( d.getHours() );
        var minutes = pad_time_value( d.getMinutes() );
        var seconds = pad_time_value( d.getSeconds() );
        var current_time = [hours,minutes,seconds].join(':');
        $('#digital_clock').html(current_time);

    };

    updateClock();

    // Calling updateClock() every 1 second
    setInterval(updateClock, 1000);

}());
