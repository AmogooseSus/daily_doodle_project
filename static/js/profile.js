$().ready(function() {
    $("#user-image").click(function(e) {
        $("#pic-changer").click()
    })


    $("input[type=file]").on('change',function(){
       $("#submit").click()
    });    
})