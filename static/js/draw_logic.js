$().ready(() => {
    //canvas properties
    let canvas = $("#canvas")[0];
    let ctx = canvas.getContext("2d");
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
    let pencilColour = "#ffffff";

    $("#canvas").mousedown((e) => {
        mouseDown = true;
        ctx.beginPath();
    })
    $("#canvas").mouseup((e) => {
        mouseDown = false;
        ctx.closePath();
    })
    $("#canvas").mousemove(handle_drawing);

    function handle_drawing(e) {
        if(!mouseDown) return;
        if(tool_selected == pencil) {
            handle_pencil(e);
        }
        else if(tool_selected == eraser) {
            handle_eraser(e);
        }
        
    }

    function handle_pencil(e) {
        ctx.strokeStyle = pencilColour;
        ctx.lineTo(e.offsetX,e.offsetY);
        ctx.stroke();
       
    }

    function handle_eraser(e) {
        ctx.strokeStyle = canvasColour;
        ctx.lineTo(e.offsetX,e.offsetY);
        ctx.stroke();
    }

    $("#pen-size").change((e) => {
        let size =$("#pen-size")[0].value
        pencilWidth = size;
        ctx.lineWidth = pencilWidth;
    })

    $("#eraser-size").change((e) => {
        let size = $("#eraser-size")[0].value
        eraserWidth = size;
        ctx.lineWidth = eraserWidth;
    })

    $("#pencil").click((e) => {
        console.log("test")
        tool_selected = pencil;
        console.log(tool_selected);
    })

    $("#eraser").click((e) => {
        tool_selected = eraser;
        console.log(tool_selected);
    })

    $("#clear").click((e) => {
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    })

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
    
    $("#submit").click((e) => {
        let image = canvas.toDataURL("image/jpeg");
        $.ajax({
            type: "POST",
            url: "/dailydoodle/draw/",
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            data: {
                imageBase64: image,
            },
            enctype:"multipart/form-data",

        }).done((e) => {
            console.log("saved drawing");
        })
    })

});