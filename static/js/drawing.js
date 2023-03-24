$().ready(() => {
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
        if(comment_text ==  "" || comment_text.length <= 0 ) return;
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
            // show comment locally
            let username = $("#submit").data("username");
            let profile_picture = $("#submit").data("profilepicture");
            let date =  new Date();
            let formatted_date = date.toLocaleString();
            $("#comments").prepend(` <div class="flex flex-col w-full bg-main h-auto px-8 py-4  ">
            <h4 class="text-main_gray text-xs">${formatted_date}</h4> 
            <div class="flex flex-row  divide-x-2 divide-extra_blue">
            <div class="flex flex-row p-4 items-center comment hover:cursor-pointer self-start">
                <img class="rounded-lg h-14 w-16" src="${profile_picture}" alt="Profile Picture" />  
                <h1 class="ml-2 break-all text-secondary_gray text-center font-semibold">${username}</h1>
            </div>
            <h2 class="px-8 break-all w-fit">${comment_text}</h2>
            </div>
            </div> `);
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