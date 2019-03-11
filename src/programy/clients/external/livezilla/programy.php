<?php
$requestobj = json_decode($_POST["livezilla_user_api_request"]);
$responseNode = array();
$responseNode["ResponseTo"] = "";
$responseNode["Id"] = rand(1111111,9999999);
$responseNode["SearchKB"] = false;
$url = "http://localhost:8989/api/rest/v1.0/ask?question=".rawurlencode($requestobj->Value)."&userid=".$requestobj->VisitorId;
$sdata = json_decode(file_get_contents($url));
$responseNode["Value"] = $sdata[0]->response->answer;
if(!empty($responseNode["Value"]))

            echo json_encode($responseNode);

?>