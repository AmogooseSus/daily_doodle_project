$().ready(() => {
    let canvas = $("#canvas")[0];
    let ctx = canvas.getContext("2d");
    let mouseDown = false;
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    ctx.fillStyle = "#C0D0E7";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Tool bar
    let pencil = $("#pencil")[0];
    let eraser = $("#eraser")[0];
    let pencilWidth = $("#pen-size")[0].value;
    let eraserWidth = $("#eraser-size")[0].value;

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
        handle_pencil(e);
        
    }

    function handle_pencil(e) {
        console.log("test")
        ctx.lineTo(e.offsetX,e.offsetY);
        ctx.stroke();
       
    }

    function handle_eraser(e) {

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
        let img = $(`<img src=${image} />`);
        $("body").append(img);
    })

});