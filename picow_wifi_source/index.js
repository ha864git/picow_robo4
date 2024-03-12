const url = "";

let latest_off = ""; /// Remembers if off operation is required

window.onload = function () {
    const XHR = new XMLHttpRequest();
    XHR.open("GET", url + "/api/get_paneldef", true);
    XHR.send();
    XHR.onreadystatechange = (e) => {
        if (XHR.readyState === XMLHttpRequest.DONE) {
            const status = XHR.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                const paneldef = JSON.parse(XHR.responseText);
                paneldef.forEach(function (value) {
                    const elmnt = document.getElementById("btn" + value.key);
                    elmnt.addEventListener("mousedown", () => {
                        event.preventDefault();
                        execGetCmd(value.on);
                        latest_off = value.off;
                    });
                    elmnt.addEventListener("touchstart", () => {
                        event.preventDefault();
                        execGetCmd(value.on);
                        latest_off = value.off;
                    });
                    if (value.off !== "") {
                        elmnt.addEventListener("mouseup", () => {
                            event.preventDefault();
                            execGetCmd(value.off);
                            latest_off = "";
                        });
                        elmnt.addEventListener("touchend", () => {
                            event.preventDefault();
                            execGetCmd(value.off);
                            latest_off = "";
                        });
                        elmnt.addEventListener("mouseout", () => {
                            event.preventDefault();
                            if (latest_off !== "") {
                                execGetCmd(value.off);
                                latest_off = "";
                            }
                        });
                        elmnt.addEventListener("mouseout", () => {
                            event.preventDefault();
                            if (latest_off !== "") {
                                execGetCmd(value.off);
                                latest_off = "";
                            }
                        });
                    }
                });
            }
        }
    }
}

function execGetCmd(cmd_name) {
    const XHR = new XMLHttpRequest();
    XHR.open("GET", url + "/api/exe_command?cmd_name=" + cmd_name, true);
    XHR.send();
    XHR.onreadystatechange = (e) => {
        if (XHR.readyState === XMLHttpRequest.DONE) {
            const status = XHR.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                console.log(XHR.responseText);
            }
        }
    }
}

