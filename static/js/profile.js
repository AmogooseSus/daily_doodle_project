$().ready(function() {
    $("#user-image").click(function(e) {
        $("#pic-changer").click()
    })


    $("input[type=file]").on('change',function(){
       $("#submit").click()
    });    

    let queryParams = new URLSearchParams(window.location.search);
    let changedUsername = queryParams.get("changed_username");
    let changedProfile = queryParams.get("changed_picture");
    if(changedUsername) {
        alert("User name was changed successfully");
    }
    if(changedProfile) {
        alert("Profile picture changed successfully");
    }
})