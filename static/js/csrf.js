function getCookie(name) {
    let value = null;
    if(document.cooke && document.cookie !== "") {
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

let csrftoken = getCookie("csrftoken");
