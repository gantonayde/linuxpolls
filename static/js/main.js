$(document).ready(function () {

});

var create_vote = function () {
    var value = $("form input[name='choice']:checked").val();
    var catid = $(this).attr("data-catid");
    if (value !== undefined) {
        var data = { choice: value };
        var args = { type: "POST", url: "/polls/polls/"+catid+"/ajaxvote/", data: data, success: check_date, complete: create_vote_complete };
        $.ajax(args);
    }
    else {
        console.log('create_vote else statement, radio button not selected, value is undefined');
        document.getElementById("voted-text").innerHTML = "Please select an option!";
        // We should display a helpful error message
    }
    return false; // stops djangos httprespone and allows ajax to take over
};

$(".js-vote").click(create_vote);

var check_date = function (res) {
    console.log(res.data);
  }

var create_vote_complete = function (res, status) {
    if (status == "success") {
        console.log(res);
        console.log(res.responseJSON);
        //console.log(res);
        const votes = res.responseJSON.data;
        $( '#vote'+votes[0].question_id ).removeClass('btn btn-primary'); 
        $( '#vote'+votes[0].question_id ).addClass('btn btn-success'); 
        
        document.getElementById("voted-text").innerHTML = "Voted!";
        
        //document.getElementById("graph"+votes[0].question_id).innerHTML = "";
        document.getElementById("plot-div"+votes[0].question_id).innerHTML = "";
        
        const bokehGraph = JSON.parse(res.responseJSON.graph);
        const pltGraph = JSON.parse(res.responseJSON.plt);
       // Plotly.plot("plotly"+votes[0].question_id, pltGraph, {});
        var config = {responsive: true};
        Plotly.newPlot("plot-div"+votes[0].question_id, pltGraph.data, pltGraph.layout, config );
       // Bokeh.embed.embed_item(bokehGraph);

        for (var i = 0; i < votes.length ; i++) {
            //console.log(votes[i].votes, votes[i].id);
            document.getElementById("vote-num"+votes[i].id).innerHTML = votes[i].votes;
            $('input[name="choice"]').prop('checked', false);
        }
    }
    else {
        console.log('Error in else statement');
        console.log(res.responseText);
        display_message(res.responseText, $(".js-message"));
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


// Poll page buttons

function expandCollapseSwitch() {

    if ($(this).data("closedAll")) {
        $(".accordion-collapse").collapse("show");
        $("#expandCollapseSwitch").text("Collapse All");
    }
    else {
        $(".accordion-collapse").collapse("hide");
        $("#expandCollapseSwitch").text("Expand All");
    }
    // save last state
    $(this).data("closedAll", !$(this).data("closedAll"));
};

function resultPollSwitch() {

    if (!$(this).data("resultsShown")) {
        $("#pills-poll-tab").removeClass("active");
        $("#pills-poll").removeClass("show active");
        $("#pills-results-tab").addClass("active");
        $("#pills-results").addClass("show active");
        $("#resultPollSwitch").text("Show Poll");
    }
    else {
        $("#pills-results-tab").removeClass("active");
        $("#pills-results").removeClass("show active");
        $("#pills-poll-tab").addClass("active");
        $("#pills-poll").addClass("show active");
        $("#resultPollSwitch").text("Show Results");
    }
    // save last state
    $(this).data("resultsShown", !$(this).data("resultsShown"));
}

$("#expandCollapseSwitch").click(expandCollapseSwitch);
$("#resultPollSwitch").click(resultPollSwitch);   