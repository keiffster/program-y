// jQuery Document
$(document).ready(function(){

    $("#chatbox").append ("<p><b>Bot:</b>Hello, my name is Y-Bot, how can I help you today?</p>" );
    $("#chatbox").append ("<p><hr /></p>" );

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

        xhttp.open("GET", "/api/v1.0/ask?question="+question+"&sessionid=1234567890");
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.send();

 		return false;
	});

});
