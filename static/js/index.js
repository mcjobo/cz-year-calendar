$("#generate-calendar").click(function(e) {
    //var wi = window.open('about:blank', '_blank');
    $.ajax({
    type: "GET",
    url: "/generate",
    data: {"key": $("input").val()},
    success: function(result){
        var res = JSON.parse(result);
        console.log(result, res.pdfUrl);
        //wi.location.href = '/static/cal.pdf';
        window.open(result.pdfUrl, "_blank")
        $('#pdfLink').html('<a target="_blank" href='+res.pdfUrl+'>Jahreskalender</a>');
    }});
    e.preventDefault();
});

$(document).ready(function(){


$.ajaxSetup({
    statusCode: {
    //        console.log('status code');
        401: function(err){
            console.log('Login Failed.', err.responseJSON);
            window.location.href = "/static/login.html";
        // or whatever...
        }
    }
  });


});
