const url = "";

window.onload = function () {
    const XHR = new XMLHttpRequest();
    XHR.open("GET", url + "/api/get_angles", true);
    XHR.send();

    XHR.onreadystatechange = (e) => {
        if (XHR.readyState === XMLHttpRequest.DONE) {
            const status = XHR.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                const paras = JSON.parse(XHR.responseText);
                console.log(paras);
                set_onload("fl", paras.fl);
                set_onload("hl", paras.hl);
                set_onload("fr", paras.fr);
                set_onload("hr", paras.hr);
                let elm = document.getElementsByClassName("trapa");
                for (let i = elm.length - 1; i >= 0; i--) {
                    elm[i].classList.remove("trapa");
                }
            }
        }
    }
}

function set_angles() {
    let fr = parseInt(document.getElementById("number_fr").value);
    let hr = parseInt(document.getElementById("number_hr").value);
    let fl = parseInt(document.getElementById("number_fl").value);
    let hl = parseInt(document.getElementById("number_hl").value);
    let para = "fl=" + fl + "&hl=" + hl + "&fr=" + fr + "&hr=" + hr;
    const XHR = new XMLHttpRequest();
    XHR.open("GET", url + "/api/set_angles?" + para, true);
    XHR.send();

    XHR.onreadystatechange = (e) => {
        if (XHR.readyState === XMLHttpRequest.DONE) {
            const status = XHR.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                const paras = JSON.parse(XHR.responseText);
                console.log(paras);
            }
        }
    }
}

function set_onload(which_leg, set_angle) {
    let ang = set_angle - 90;
    if (which_leg[1] == "l") { ang = 0 - ang }
    document.getElementById("range_" + which_leg).value = 0 - ang;
    document.getElementById("number_" + which_leg).value = ang;
    let elem = document.getElementById("leg_" + which_leg);
    elem.style.setProperty('transform', 'rotate(' + (90 + ang) + 'deg)');
//    elem.style.setProperty('opacity', '1');
//    document.querySelector("#range_" + which_leg).classList.add("ld");
}

function number2range(w) {
    let ang = parseInt(document.getElementById("number_" + w).value);
    ang = 0 - ang;
    document.getElementById("range_" + w).value = ang;
    rotate_leg(w, ang);
}

function range2number(w) {
    let ang = parseInt(document.getElementById("range_" + w).value);
    document.getElementById("number_" + w).value = 0 - ang;
    rotate_leg(w, ang);
}

function rotate_leg(w, ang) {
    document.getElementById("leg_" + w).style.setProperty('transform', 'rotate(' + (90 - ang) + 'deg)');
}
