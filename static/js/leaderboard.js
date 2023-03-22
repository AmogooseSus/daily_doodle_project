$().ready(function() {

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

    $("#search-bar").keyup(function (e) {
        let value = $("#search-bar")[0].value;
        if(value === "") {
           toggleLeaderboardAndSearch(false);
        }
        else {
            if(value.length <= 0) return;
            $.ajax({
                type: "POST",
                url: "/dailydoodle/leaderboard/",
                headers: {"X-CSRFToken": getCookie("csrftoken")},
                data: {
                    name: "search",
                    query: value,
                },
            })
            .done((response) => {
                console.log(response);
                data = response["user_data"]
                data = Object.values(data)
                $("#search-results").empty()
                data.forEach(element => {
                    console.log(element)
                    let boardData = $(`<div class="w-full bg-main h-auto py-4 px-8 flex flex-row justify-evenly">
                        <h2>${element.position}</h2>
                        <div class="flex flex-row p-4 items-center">
                            <img class="rounded-lg h-8 w-10" src="${element.profile_picture}" alt="Profile Picture" />
                            <h1 class="ml-2 break-all text-secondary_gray text-center font-semibold">${element.username}</h1>
                        </div>
                        <h2>${element.most_liked_drawing == null ? "None yet" : element.most_liked_drawing}</h2>
                        <h2>${element.upvotes_recieved}</h2>
                    </div>`)
                    $("#search-results").append(boardData)
                });
                toggleLeaderboardAndSearch(true)
            })
        }
    });


    function toggleLeaderboardAndSearch(tohide) {
        if(tohide) {
            $("#leaderboard").addClass("hidden");
            $("#search-results").removeClass("hidden");
        }
        else {
            $("#leaderboard").removeClass("hidden");
            $("#search-results").addClass("hidden");
        }
    }
    
})