$().ready(() => {

    let upvoteText = $("#upvotes-display")[0]
    let drawing_id =  $("#comment").data("drawing_id");


    function handleUpvoteText(amount) {
        $("#upvotes-display").text(amount);
    }

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

    // Create a post request to save the comment for this drawing we then re render the comments so user doesn't have to refresh
    $("#submit").click((e) => {
        let comment_text = $("#comment")[0].value;
        $.ajax({
            type: "POST",
            url: `/dailydoodle/drawing/${drawing_id}`,
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            data: {
               name: "comment",
               comment_text: comment_text,
            },
        }).done((e) => {
            console.log("saved comment");
            renderComments();
        })
    })

    $("#upvote").click((e) => {
        $.ajax({
            type: "POST",
            url: `/dailydoodle/drawing/${drawing_id}`,
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            data: {
               name: "upvote",
            },
        }).done((response) => {
            upvotes = JSON.parse(response["upvotes"]);
            console.log(upvotes)
            handleUpvoteText(upvotes);
        })
    })

    $(".comment").each(function() {
        $(this).click(function(e) {
            let username = $(this).find("h1").text()
            location.href = `/dailydoodle/submissions/${username}`
        })
    })
})  