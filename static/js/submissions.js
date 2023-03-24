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

   $(".displayed-image").each(function() {
     $(this).click(function(e) {
         location.href= `/dailydoodle/drawing/${$(this).attr("id")}`;
     })
   })

   $("#search-bar").keyup(function (e) {
       let query = $("#search-bar")[0].value
       $(".prompt-div").each(function(e)  {
          let promptValue = $(this).find("h1").text();
          if(promptValue.includes(query)) {
            $(this).removeClass("hidden");
          }
          else {
            $(this).addClass("hidden");
          }
       })
   })

  
})