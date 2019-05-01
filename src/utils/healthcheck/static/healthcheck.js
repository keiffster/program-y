// jQuery Document
$(document).ready(function(){

    check_health = function(service) {

        var xhttp = new XMLHttpRequest();
        xhttp.onload = function () {
            if (this.status == 200 && this.responseText != null) {
                var treedata = JSON.parse(this.responseText);
                $("#healthcheck").fancytree(treedata)
            }
        }

        xhttp.open("GET", service);
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.send();

 		return false;
    }

    check_health("/api/health/v1.0/ping")

});
