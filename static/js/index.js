$().ready(() => {
    // properties for chosen top drawing
    let chosenElement = $("#intial");
    let previousId = null;
    let chosenId = $("#intial").data("drawing");

    // register event handlers for every next button
    $(".clickable").each(function() {
        $(this).click(function(e)  {
            if($(this) !== $(chosenElement)) {
                $(chosenElement).removeClass("bg-white");
                $(chosenElement).addClass("bg-indigo-100");
                $(chosenElement).addClass("opacity-50");
                previousId = chosenId;
                chosenElement = $(this);
                $(chosenElement).removeClass("bg-indigo-100 opacity-50");
                $(chosenElement).addClass("bg-white");
                chosenId = $(chosenElement).data("drawing");
                switch_drawing()
            }
        })
    })
    

    function switch_drawing() {
        // hide previous section
        $("#" + previousId).addClass("hidden")
        // show current section
        $("#" + chosenId).removeClass("hidden")
    }
})  