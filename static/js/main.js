$(document).ready(function () {

});

var create_vote = function () {
    var value = $("form input[name='choice']:checked").val();
    var catid = $(this).attr("data-catid");
    if (value != "") {
        var data = { choice: value };
        var args = { type: "POST", url: "/polls/polls/"+catid+"/ajaxvote/", data: data, complete: create_vote_complete };
        $.ajax(args);
    }
    else {
        console.log('else');
        // We should display a helpful error message
    }
    return false;
};

$("#vote").click(create_vote);


var create_vote_complete = function (res, status) {
    if (status == "success") {
        console.log('Success');
        $( '#vote' ).removeClass('btn btn-primary'); 
        $( '#vote' ).addClass('btn btn-success'); 
        document.getElementById("voted-text").innerHTML = "Voted!";
    }
    else {
        console.log('Error')
        display_message(res.responseText, $(".message"));
    }
}
var display_message = function (msg, elem) {
    var msg_div = $('<div><p>' + msg + '</p></div>');
    elem.append(msg_div).fadeIn('slow').animate({ opacity: 1.0 }, 7000).fadeOut('slow', function () { msg_div.remove(); });
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});