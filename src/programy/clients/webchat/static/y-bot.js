// jQuery Document
$(document).ready(function(){

    $(".question").click(function() {

        var question = $(this).text()

        var xhttp = new XMLHttpRequest();
        xhttp.onload = function () {
            if (this.status == 200 && this.responseText != null) {
                var response = JSON.parse(this.responseText);

                $("#chatbox").append ("<p><b>You:</b> "+response.response.question+"</p>" );
                $("#chatbox").append ("<p><b>Bot:</b> "+response.response.answer+"</p>" );
                $("#chatbox").append ("<p><hr /></p>" );

                $("#chatbox")[0].scrollTop = $("#chatbox")[0].scrollHeight;

            }
        }

        xhttp.open("GET", "/api/v1.0/ask?question="+question+"&clientid=webchat");
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.send();

 		return false;
    });

	$("#submitmsg").click(function(){

        var question = $("#usermsg").val();
        $("#usermsg").val("");

        var xhttp = new XMLHttpRequest();
        xhttp.onload = function () {
            if (this.status == 200 && this.responseText != null) {
                var response = JSON.parse(this.responseText);

                $("#chatbox").append ("<p><b>You:</b> "+response.response.question+"</p>" );
                $("#chatbox").append ("<p><b>Bot:</b> "+response.response.answer+"</p>" );
                $("#chatbox").append ("<p><hr /></p>" );

                $("#chatbox")[0].scrollTop = $("#chatbox")[0].scrollHeight;

            }
        }

        xhttp.open("GET", "/api/v1.0/ask?question="+question+"&clientid=webchat");
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.send();

 		return false;
	});

});
