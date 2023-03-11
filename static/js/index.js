$().ready(() => {
    // properties for chosen top drawing
    let chosen = $("#intial").data("drawing");
    let chosen_index = 0;

    // register event handlers for every next button
    $(".clickable").each(() => {
        $(this).click((e) => {
            chosen = $(this).attr("id")
            $(".clickable").each(() => {
                $(this).attr
            })
            switch_drawing()
        })
    })
    

    function switch_drawing() {
        // hide all sections
        // get the drawing section with id of chosen and set class to show 
    }
})  