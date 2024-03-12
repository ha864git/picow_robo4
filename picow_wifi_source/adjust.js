const url = "";

window.onload = function () {
    const XHR = new XMLHttpRequest();
    XHR.open("GET", url + "/api/get_ini_angles", true);
    XHR.send();

    XHR.onreadystatechange = (e) => {
        if (XHR.readyState === XMLHttpRequest.DONE) {
            const status = XHR.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                const paras = JSON.parse(XHR.responseText);
                console.log(paras);
                document.getElementById("fl_ini").value = paras.fl_ini;
                document.getElementById("hl_ini").value = paras.hl_ini;
                document.getElementById("fr_ini").value = paras.fr_ini;
                document.getElementById("hr_ini").value = paras.hr_ini;
                document.getElementById("fl_ini").classList.remove('ra');
                document.getElementById("hl_ini").classList.remove('ra');
                document.getElementById("fr_ini").classList.remove('ra');
                document.getElementById("hr_ini").classList.remove('ra');
            }
        }
    }
}

function set_angles_ini() {
    const fl_ini = document.getElementById("fl_ini").value;
    const hl_ini = document.getElementById("hl_ini").value;
    const fr_ini = document.getElementById("fr_ini").value;
    const hr_ini = document.getElementById("hr_ini").value;
    const para = "fl_ini=" + fl_ini + "&hl_ini=" + hl_ini + "&fr_ini=" + fr_ini + "&hr_ini=" + hr_ini;
    const XHR = new XMLHttpRequest();
    XHR.open("GET", url + "/api/set_ini_angles?" + para, true);
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
