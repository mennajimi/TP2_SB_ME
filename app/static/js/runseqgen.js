$(document).ready(readyData);

function readyData(){
    $("#validate").click(function(){
        validation_param($("#model").val());
        })
}

function validation_param (model){
        json={'model':model};
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(json),
            url: '/bob'
        }).done(function(data, status){
           console.log(data.ok);
           location.reload();
        }).fail(function(){
            alert("Submission failed");
        }).always(function(){
            console.log("done");
        });
    }



