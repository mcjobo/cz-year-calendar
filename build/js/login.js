
var google_url = "";

$(document).ready(function(){

    $.ajax({
        url: "/calendar/get_auth_request",
        data: {"provider": 'google'},
        success: function(result){
            console.log("url: ", result);
            google_url = result;
        }
    });
});


$("#login-google").click(function(e) {
    window.open(google_url, "_self")
    e.preventDefault();
});
