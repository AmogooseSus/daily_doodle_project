$().ready(() => {

    // used to get csrf token from cookies
    function getCookie(name) {
        let value = null;
        if(document.cookie && document.cookie !== "") {
            let cookies  = document.cookie.split(";");
            for(let i = 0; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
                if(cookie.substring(0,name.length+1) === (name + "=")) {
                    value = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }

        return value;
    }


    // Create a post request to submit the drawing then rediect to homepage
    $("#submit").click((e) => {
        let comment_text = $("#comment")[0].value;
        let drawing_id =  $("#comment").data("drawing_id");
        $.ajax({
            type: "POST",
            url: `/dailydoodle/drawing/${drawing_id}`,
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            data: {
                name: "comment",
               comment_text: comment_text,
               drawing_id: drawing_id
            },
        }).done((e) => {
            console.log("saved comment");
        })
    })
})  