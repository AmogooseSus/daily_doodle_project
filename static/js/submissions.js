$().ready(function(e) {
   $(".dynamic-change").each(function() {
       $(this).click(function(e) {
          let toShowId =  $(this).data("prompt");
          console.log(toShowId)
          $(".dynamic").each(function() {
            $(this).addClass("hidden")
          })
          $("#" + toShowId).removeClass("hidden");
       })
   })
})