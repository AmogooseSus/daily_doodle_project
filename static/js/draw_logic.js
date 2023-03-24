$().ready(() => {
    //canvas properties
    let canvas = $("#canvas")[0];
    let ctx = canvas.getContext("2d",{ willReadFrequently: true });
    let mouseDown = false;
    let canvasColour = "#C0D0E7";
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    //give canvas intial background
    ctx.fillStyle = canvasColour;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Tool bar and properties
    let pencil = $("#pencil")[0];
    let eraser = $("#eraser")[0];
    //default selected tool to pencil
    let tool_selected = pencil;
    let pencilWidth = $("#pen-size")[0].value;
    let eraserWidth = $("#eraser-size")[0].value;
    let pencilColour = "#000000";
    ctx.lineCap = "round";
    ctx.lineJoin = "round";

    // undo , redo stacks
    let redoStack = [];
    let redoTop = -1;
    let undoStack = [];
    let undoTop = -1;

    // svg tool colours
    let picked = "#D84E60";
    let unpicked = "#374395";

    // references list
    let references = []
    let max_amount = 3;

    $("#canvas")

    
    $("#canvas").bind( "mousedown pointerdown",(e) => {
        mouseDown = true;
        ctx.beginPath();
        // reset redoStack if new line started on clear canvas
        if(undoTop == -1) {
            redoStack = [];
            redoTop = -1;
        }
    })
    $("#canvas").bind("mouseup pointerup",(e) => {
        mouseDown = false;
        // add image data to undo stack and increment index
        undoStack.push(ctx.getImageData(0,0,canvas.width,canvas.height));
        undoTop++;
    })
    $("#canvas").on("pointermove",handle_drawing)
    $("#canvas").mousemove(handle_drawing);


    function handle_drawing(e) {
        if(!mouseDown) return;
        if(tool_selected == pencil) {
            ctx.lineWidth = pencilWidth;
            ctx.strokeStyle = pencilColour;
        }
        else if(tool_selected == eraser) {
            ctx.lineWidth = eraserWidth;
            ctx.strokeStyle = canvasColour;
        }  
        drawLine(e.offsetX,e.offsetY);
    }

    function drawLine(x,y) {
        ctx.lineTo(x,y);
        ctx.stroke();
    }


    // event listeners for tool changes and tool adjusters
    $("#pen-size").change((e) => {
        pencilWidth = $("#pen-size")[0].value
    })

    $("#eraser-size").change((e) => {
        eraserWidth =  $("#eraser-size")[0].value
    })

    $("#pencil").click(function() {
        tool_selected = pencil;
        $(this).children().children().attr("fill",picked);
        $("#eraser").children().children().attr("fill",unpicked);
    })

    $("#eraser").click(function() {
        tool_selected = eraser;
        $(this).children().children().attr("fill",picked);
        $("#pencil").children().children().attr("fill",unpicked);
    })

    $("#clear").click((e) => {
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        let lastUndo = undoStack.pop()
        if(lastUndo !== undefined) {
            redoStack.push(lastUndo)
            redoTop++;
        }
        undoTop = -1;
        undoStack = [];
    })

    $("#color").change((e) => {
        pencilColour = $("#color")[0].value;
    })

    $("#undo").click((e) => {
        // pop the last change on canvas and draw the previous change 
        if(undoTop > 0) {
            redoStack.push(undoStack.pop());
            redoTop++;
            undoTop--;
            ctx.putImageData(undoStack[undoTop],0,0);
        }
        else{
            // when we reach the end of the stack just clear the canvas
            $("#clear").click();
        }

    })

    $("#redo").click((e) => {
        // pop the the last redo and re-draw it on canvas
        if(redoTop >= 0) {
            let redo = redoStack.pop();
            undoStack.push(redo);
            undoTop++;
            redoTop--;
            ctx.putImageData(redo,0,0);
        }
    
    })


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
        let image = canvas.toDataURL("image/jpeg");
        $.ajax({
            type: "POST",
            url: "/dailydoodle/draw/",
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            data: {
                imageBase64: image,
                name: "submit",
            },
            enctype:"multipart/form-data",

        }).done((e) => {
            console.log("saved drawing");
            location.href = "/dailydoodle/";
        })
    })

    // reference image searching funtionality
    let query = $("#search-bar")[0].value
    $("#search").click((e) => {
        if(query.length <= 0) return;
        console.log(query)
        if(! (references.length < max_amount)) {
            alert("You already have 3 max references");
            return;
        }
        $.ajax({
            type: "POST",
            url: "/dailydoodle/draw/",
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            data: {
                name: "search",
                query: query,
            },
        })
        .done((response) => {
            console.log(response);
            data = JSON.parse(response["data"]);
            $("#results").html("");
            $("#results-container").removeClass("hidden");
            data.forEach(element => {
                let thumbnail = $(`<img src=${element["thumb"]} class="rounded-lg mt-2"/>`);
                $(thumbnail).click(function(e) {
                    addToReferences(this);
                })
                $("#results").append(thumbnail);
            });
        })
    })
    
    $("#search-bar").keyup( (e) => { 
        query = $("#search-bar")[0].value
    });

    $("#close-search").click(function(e) {
        $("#results-container").addClass("hidden");
    })

    function addToReferences(image) {
        if(! (references.length < max_amount)) return;
        references.push(image);
        if(references.length >= max_amount) {
            $("#results-container").addClass("hidden");
        }
        renderReferences();
    }

    function renderReferences() {
        references.forEach((element) => {
             $("#selected").append(element);
        })
    }
    
});

