$(document).ready(function () {

});

var create_vote = function () {
    var catid = $(this).attr("data-catid");
    var value = $(`#form${catid} option:selected`).val(); 
    console.log(value);   
    if (value !== "") {
        var data = { choice: value };
        var args = { type: "POST", url: `/polls/${catid}/vote/`, data: data, complete: create_vote_complete };
        $.ajax(args);
    }
    else {
        //alert("Please select a choice")
        display_danger_message("Please select an option", $("#js-vote-msg"+catid));
        console.log('choice not selected, ajax call not triggered');
        // We should display a helpful error message
    }
    return false; // stops djangos httprespone and allows ajax to take over
};

$(".js-vote").click(create_vote);


var create_vote_complete = function (res, status) {
    if (status == "success") {
        const idData = res.responseJSON.id_data;
        const pltGraph = JSON.parse(res.responseJSON.plotly_plot);
        var questionId = idData[0].question_id;
        var pltConfig = {responsive: true};
        display_message("Thank you for voting!", $("#js-vote-msg"+questionId));
        $("#form"+questionId).remove();

        if ($("#polls-on-focus").length > 0) {
           // Plotly.newPlot("plot-car"+questionId, pltGraph.data, pltGraph.layout, config );
            if ($("[id^=form]").length > 0){
             //   setTimeout(function() { $("#heading"+questionId).remove(); }, 3500);
                setTimeout(function() { $("#collapse"+questionId).remove(); }, 3500);
            }
            else {
                setTimeout(function() { $("#polls-on-focus").remove(); }, 3500);
            }
        }
        else {
            Plotly.newPlot("plot-div"+questionId, pltGraph.data, pltGraph.layout, pltConfig );
        }
    }
    else {
        const idData = res.responseJSON.id_data;
        var questionId = idData[0].question_id;
        console.log('Voting not successful');
        display_danger_message("You have already voted!", $("#js-vote-msg"+questionId));
        $("#form"+questionId).remove();
    }
}
var display_message = function (msg, elem) {
    var msg_div = $('<div class="alert alert-success" role="alert"><h4 class="mb-0">' + msg + '</h4></div>');
    elem.append(msg_div).fadeIn('slow').animate({ opacity: 1.0 }, 3000).fadeOut('slow', function () { msg_div.remove(); });
};

var display_danger_message = function (msg, elem) {
    var msg_div = $('<div class="alert alert-danger" role="alert"><h4 class="mb-0">' + msg + '</h4></div>');
    elem.append(msg_div).fadeIn('slow').animate({ opacity: 1.0 }, 3000).fadeOut('slow', function () { msg_div.remove(); });
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


// Poll page buttons

function expandCollapseSwitch() {

    if ($(this).data("closedAll")) {
        $(".js-accordion-collapse").collapse("show");
        $("#expandCollapseSwitch").text("Collapse All");

    }
    else {
        $(".js-accordion-collapse").collapse("hide");
        $("#expandCollapseSwitch").text("Expand All");
    }
    // save last state
    $(this).data("closedAll", !$(this).data("closedAll"));
};

function resultsShowSwitch() {

    if (!$(this).data("resultsShown")) {
        $('.js-show-toggle').hide();
        $("#resultsShowSwitch").text("Show Plots");
    }
    else {
        $('.js-show-toggle').show();
        $("#resultsShowSwitch").text("Hide Plots");
    }
    // save last state
    $(this).data("resultsShown", !$(this).data("resultsShown"));
}


$("#expandCollapseSwitch").click(expandCollapseSwitch);
$("#resultsShowSwitch").click(resultsShowSwitch);   

$("#id_choice_text").addClass("selectpicker");

