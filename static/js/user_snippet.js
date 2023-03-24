$().ready(function() {
    $(".snippet").each(function() {
        $(this).click(function(e) {
            let username = $(this).find("h4").text();
            location.href = `/dailydoodle/submissions/${username}/`;  
         })
    })
})