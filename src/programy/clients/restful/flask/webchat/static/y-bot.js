// jQuery Document
$(document).ready(function(){

    ask_question = function(question, show_question) {

        var xhttp = new XMLHttpRequest();
        xhttp.onload = function () {
            if (this.status == 200 && this.responseText != null) {
                var response = JSON.parse(this.responseText);

                if (show_question == true) {
                    $("#chatbox").append ("<p><b>You:</b> "+response.response.question+"</p>" );
                }
                $("#chatbox").append ("<p><b>Bot:</b> "+response.response.answer+"</p>" );
                $("#chatbox").append ("<p><hr /></p>" );

                $("#chatbox")[0].scrollTop = $("#chatbox")[0].scrollHeight;
            }
        }

        xhttp.open("GET", "/api/web/v1.0/ask?question="+question);
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.send();

 		return false;
    }

    ask_question("YINITIALQUESTION", false)

    $(".question").click(function() {
        var question = $(this).text()
        return ask_question(question, true)
    });

    $(document).on('click', '.postback', function(){
	    var question = "";
	    var attr = $(this).attr('postback');
        if (typeof attr !== typeof undefined && attr !== false) {
            question = attr
        } else {
            question = $(this).text();
        }
        return ask_question(question, true)
    });

	$("#submitmsg").click(function(){
        var question = $("#usermsg").val();
        $("#usermsg").val("");
        return ask_question(question, true)
	});

});
