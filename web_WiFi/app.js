let motions = [];
let latest_cmd = "";
let timeoutID = null;


function inc_tover_next(leg) {
    timeoutID = setTimeout(function () {
        anginc(leg);
        inc_tover_next(leg);
    }, 50);
}

function timerset_inc(leg) {
    anginc(leg);
    timeoutID = setTimeout(function () {
        anginc(leg);
        inc_tover_next(leg);
    }, 600);
}

function dec_tover_next(leg) {
    timeoutID = setTimeout(function () {
        angdec(leg);
        dec_tover_next(leg);
    }, 50);
}

function timerset_dec(leg) {
    angdec(leg);
    timeoutID = setTimeout(function () {
        angdec(leg);
        dec_tover_next(leg);
    }, 600);
}

function clearRepeatBtn() {
    clearTimeout(timeoutID);
}

function check_num(input_str) {
    let input_value = parseInt(input_str);
    if (input_value < -80) {
        input_value = -80;
    } else if (input_value > 80) {
        input_value = 80;
    } else if (isNaN(input_value)) {
        input_value = 0;
    }
    return input_value;
}

window.onload = function () {

    const legs = ["fr", "hr", "fl", "hl"];
    legs.forEach(function (element) {
        document.getElementById("number_" + element).addEventListener("focusout", (event) => {
            event.target.value = check_num(event.target.value);
            number2range(element);
        });
        document.getElementById("range_btn_inc_" + element).addEventListener("mousedown", () => {
            event.preventDefault();
            timerset_inc(element);
        });
        document.getElementById("range_btn_inc_" + element).addEventListener("touchstart", () => {
            event.preventDefault();
            timerset_inc(element);
        });
        document.getElementById("range_btn_inc_" + element).addEventListener("mouseup", () => {
            event.preventDefault();
            clearRepeatBtn();
        });
        document.getElementById("range_btn_inc_" + element).addEventListener("touchend", () => {
            event.preventDefault();
            clearRepeatBtn();
        });
        document.getElementById("range_btn_inc_" + element).addEventListener("mouseout", () => {
            event.preventDefault();
            clearRepeatBtn();
        });
        document.getElementById("range_btn_inc_" + element).addEventListener("touchcancel", () => {
            event.preventDefault();
            clearRepeatBtn();
        });
        document.getElementById("range_btn_dec_" + element).addEventListener("mousedown", () => {
            event.preventDefault();
            timerset_dec(element);
        });
        document.getElementById("range_btn_dec_" + element).addEventListener("touchstart", () => {
            event.preventDefault();
            timerset_dec(element);
        });
        document.getElementById("range_btn_dec_" + element).addEventListener("mouseup", () => {
            event.preventDefault();
            clearRepeatBtn();
        });
        document.getElementById("range_btn_dec_" + element).addEventListener("touchend", () => {
            event.preventDefault();
            clearRepeatBtn();
        });
        document.getElementById("range_btn_dec_" + element).addEventListener("mouseout", () => {
            event.preventDefault();
            clearRepeatBtn();
        });
        document.getElementById("range_btn_dec_" + element).addEventListener("touchcancel", () => {
            event.preventDefault();
            clearRepeatBtn();
        });

    });

    const XHR = new XMLHttpRequest();
    XHR.open("GET", url + "/api/get_motions", true);
    XHR.send();
    XHR.onreadystatechange = (e) => {
        if (XHR.readyState === XMLHttpRequest.DONE) {
            const status = XHR.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                motions = JSON.parse(XHR.responseText);
                cmd_name = motions[0][0];
                create_cmd_list(cmd_name);
                document.getElementsByClassName("set_transparent")[0].classList.remove("set_transparent");
            }
        }
    }
}

function create_cmd_list(cmd_name) {
    let ht = "";
    ht += "<tr>";
    ht += "<td>command</td>";
    ht += "<td>PLAY</td>";
    ht += "<td>SAVE</td>";
    ht += "</tr>";
    motions.forEach(function (element) {
        if (element[0] !== "execmd_1" && element[0] !== "execmd_2") {
            ht += "<tr><td><button type=\"button\" class=\"cname";
            if (cmd_name === element[0]) {
                ht += " is-btn-active\"";
            } else {
                ht += "\"";
            }
            ht += " onclick=\"listcmd(this)\">" + element[0] + "</button></td > ";
            ht += "<td><button class=\"mlistbtn\" type=\"button\" onclick=\"execmd(this)\">▶</button></td>";
            ht += "<td><button class=\"mlistbtn\" type=\"button\" onclick=\"save_list(this)\">←</button></td>";
            //            ht += "<td><button class=\"mlistbtn\" type=\"button\" onclick=\"addcmd(this)\">＋</button></td>";
            //            ht += "<td><button class=\"mlistbtn\" type=\"button\" onclick=\"delcmd(this)\">－</button></td>";
            ht += "</tr>"
        }
    });
    document.getElementById('cmd_list').innerHTML = ht;
    create_mlist(cmd_name);
}

function focus_out(obj) {
    let input_value = parseInt(obj.innerHTML);
    if (obj.cellIndex < 5) {
        if (input_value < -80) {
            obj.innerHTML = "-80";
        } else if (input_value > 80) {
            obj.innerHTML = "80";
        } else if (isNaN(input_value)) {
            obj.innerHTML = "0";
        }
    } else {
        if (input_value < 0) {
            obj.innerHTML = "1";
        } else if (input_value > 15) {
            obj.innerHTML = "15";
        } else if (isNaN(input_value)) {
            obj.innerHTML = "1";
        }
    }
}

function del_line(obj) {
    const tbl = document.getElementById('mlist');
    if (tbl.rows.length > 2) {
        const tr = obj.parentNode.parentNode;
        const no = tr.rowIndex;
        tbl.deleteRow(no);
        for (let i = 1; i < tbl.rows.length; i++) {
            tbl.rows[i].cells[0].children[0].innerHTML = i;
        }
    }
}

function add_line(obj) {
    const tr = obj.parentNode.parentNode;
    const no = tr.rowIndex;
    const len = tr.cells.length;
    const tbl = document.getElementById('mlist');
    const newRow = tbl.insertRow(no);
    for (let j = 0; j < len; j++) {
        newRow.insertCell(j);
    }
    tbl.rows[no].cells[0].innerHTML = tbl.rows[no + 1].cells[0].innerHTML;
    tbl.rows[no].cells[0].children[0].classList.add('is-btn-active');
    tbl.rows[no].cells[0].children[0].classList.remove('is-btn-active');
    tbl.rows[no].cells[1].innerHTML = document.getElementById("number_fr").value;
    tbl.rows[no].cells[2].innerHTML = document.getElementById("number_hr").value;
    tbl.rows[no].cells[3].innerHTML = document.getElementById("number_fl").value;
    tbl.rows[no].cells[4].innerHTML = document.getElementById("number_hl").value;
    tbl.rows[no].cells[5].innerHTML = document.getElementById('pitchsel').selectedOptions[0].innerHTML;
    for (let i = len - 4; i < len; ++i) {
        tbl.rows[no].cells[i].innerHTML = tbl.rows[no + 1].cells[i].innerHTML;
    }
    for (let i = 1; i < tbl.rows.length; i++) {
        tbl.rows[i].cells[0].children[0].innerHTML = i;
    }
}

function save_line(obj) {
    const tr = obj.parentNode.parentNode;
    const no = tr.rowIndex;
    const tbl = document.getElementById('mlist');
    tbl.rows[no].cells[1].innerHTML = document.getElementById("number_fr").value;
    tbl.rows[no].cells[2].innerHTML = document.getElementById("number_hr").value;
    tbl.rows[no].cells[3].innerHTML = document.getElementById("number_fl").value;
    tbl.rows[no].cells[4].innerHTML = document.getElementById("number_hl").value;
    tbl.rows[no].cells[5].innerHTML = document.getElementById('pitchsel').selectedOptions[0].innerHTML;
}


function create_mlist(cmd) {
    let ht = "";
    let mode = "";
    ht += "<tr>";
    ht += "<td width=\"35px\">No.</td>";
    ht += "<td width=\"35px\">FR</td>";
    ht += "<td width=\"35px\">HR</td>";
    ht += "<td width=\"35px\">FL</td>";
    ht += "<td width=\"35px\">HL</td>";
    ht += "<td width=\"35px\">pitch</td>";
    ht += "<td width=\"40px\">PLAY</td>";
    ht += "<td width=\"40px\">SAVE</td>";
    ht += "<td width=\"40px\">ADD</td>";
    ht += "<td width=\"40px\">DEL</td>";
    ht += "<td ></td>";
    ht += "</tr>";
    for (let i = 0; i < motions.length; ++i) {
        if (motions[i][0] == cmd) {
            for (let j = 0; j < motions[i][2].length; j++) {
                ht += '<tr><td><button class="mlbtn" type="button" onclick="set_inp(this)">' + (j + 1) + '</button></td>';
                for (let k = 0; k < motions[i][2][j].length; ++k) {
                    ht += "<td class=\"mlistnum\" contenteditable=\"true\" onBlur=\"focus_out(this)\">" + motions[i][2][j][k] + "</td>";
                }
                ht += '<td><button class="mlistbtn" type="button" onclick="play_line(this)">▶</button></td>';
                ht += '<td><button class="mlistbtn" type="button" onclick="save_line(this)">←</button></td>';
                ht += '<td><button class="mlistbtn" type="button" onclick="add_line(this)">＋</button></td>';
                ht += '<td><button class="mlistbtn" type="button" onclick="del_line(this)">－</button></td>';
                ht += '</tr>'
            }
            mode = motions[i][1];
            break;
        }
    }
    document.getElementById("mlist").innerHTML = ht;

    set_input(1);
    elems = document.getElementsByClassName("mlbtn");
    elems[0].classList.add('is-btn-active');
    if (mode === "single") {
        document.getElementById('playsel').options[0].selected = true;
        document.getElementById('playsel').options[1].selected = false;
    } else {
        document.getElementById('playsel').options[1].selected = true;
        document.getElementById('playsel').options[0].selected = false;
    }
}

function execmd(obj) {
    let list3 = [];
    cmd_name = obj.parentNode.parentNode.children[0].textContent;
    motions.forEach(function (element) {
        if (cmd_name === element[0]) {
            list3 = JSON.parse(JSON.stringify(element));
        }
    });
    exec_list(list3);
}

function execmd_name(cmd_name) {
    let list3 = [];
    motions.forEach(function (element) {
        if (cmd_name === element[0]) {
            list3 = JSON.parse(JSON.stringify(element));
        }
    });
    exec_list(list3);
}

function try_line() {
    const fr = parseInt(document.getElementById("number_fr").value);
    const hr = parseInt(document.getElementById("number_hr").value);
    const fl = parseInt(document.getElementById("number_fl").value);
    const hl = parseInt(document.getElementById("number_hl").value);
    const pitch = parseInt(document.getElementById('pitchsel').selectedOptions[0].innerHTML);
    set_motion_line(fr, hr, fl, hl, pitch);
}

function play_line(obj) {
    const tr = obj.parentNode.parentNode;
    const fr = parseInt(tr.cells[1].innerHTML);
    const hr = parseInt(tr.cells[2].innerHTML);
    const fl = parseInt(tr.cells[3].innerHTML);
    const hl = parseInt(tr.cells[4].innerHTML);
    const pitch = parseInt(tr.cells[5].innerHTML);
    set_motion_line(fr, hr, fl, hl, pitch);
}

function set_motion_line(fr, hr, fl, hl, pitch) {
    const list2 = [[fr, hr, fl, hl, pitch]];
    const cmd_name = "";
    const mode = "single";
    const list3 = [cmd_name, mode, list2];
    exec_list(list3);
}

function listcmd(obj) {
    let elems = document.getElementsByClassName("cname");
    for (let i = 0; i < elems.length; i++) {
        elems[i].classList.remove('is-btn-active');
    }
    obj.classList.add('is-btn-active');
    create_mlist(obj.innerHTML);
}

function set_inp(obj) {
    let elems = document.getElementsByClassName("mlbtn");
    for (let i = 0; i < elems.length; i++) {
        elems[i].classList.remove('is-btn-active');
    }
    obj.classList.add('is-btn-active');
    set_input(obj.innerHTML);
}

function set_input(no) {
    let table = document.getElementById('mlist');
    let fr = table.rows[no].cells[1].innerText;
    let hr = table.rows[no].cells[2].innerText;
    let fl = table.rows[no].cells[3].innerText;
    let hl = table.rows[no].cells[4].innerText;
    let pitch = table.rows[no].cells[5].innerText;
    set_onload("fl", fl);
    set_onload("hl", hl);
    set_onload("fr", fr);
    set_onload("hr", hr);
    const elm = document.getElementById("pitchsel")
    for (let i = 0; i < elm.options.length; i++) {
        elm.options[i].selected = false;
    }
    elm.options[(pitch - 1)].selected = true;
}

function set_onload(which_leg, set_angle) {
    document.getElementById("number_" + which_leg).value = set_angle;
    number2range(which_leg);
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

function try_list() {
    let list3 = make_motionlist();
    exec_list(list3);
}

function exec_list(list3) {
    cmd_name = "execmd_1";
    if (cmd_name === latest_cmd) {
        cmd_name = "execmd_2";
    }
    latest_cmd = cmd_name;
    list3[0] = cmd_name;

    if (list3[1] === 'repeat') {
        document.getElementById("stopbtn").classList.add('blink');
    } else {
        const elems = document.getElementsByClassName("blink");
        for (let i = 0; i < elems.length; i++) {
            elems[i].classList.remove('blink');
        }
    }

    const XHR = new XMLHttpRequest();
    XHR.open("post", url + "/api/exe_cmd_list", true);
    //    XHR.setRequestHeader("Content-Type", "application/json");
    XHR.send(JSON.stringify(list3));
    XHR.onreadystatechange = (e) => {
        if (XHR.readyState === XMLHttpRequest.DONE) {
            const status = XHR.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                console.log(XHR.responseText);
            }
        }
    }
}

function make_motionlist() {
    const tbl = document.getElementById('mlist');
    let list2 = [];
    for (let i = 1; i < tbl.rows.length; i++) {
        let list1 = [];
        for (let j = 1; j < tbl.rows[1].cells.length - 4; j++) {
            list1.push(parseInt(tbl.rows[i].cells[j].innerText));
        }
        list2.push(list1);
    }
    const mode = document.getElementById('playsel').selectedOptions[0].innerHTML;
    const cmd_name = "";
    const list3 = [cmd_name, mode, list2];
    return list3;
}

function save_list(obj) {
    const tr = obj.parentNode.parentNode;
    const no = tr.rowIndex;
    const cmd_name = document.getElementById('cmd_list').rows[no].children[0].innerText;
    let list3 = make_motionlist();
    list3[0] = cmd_name;
    for (let k = 0; k < motions.length; k++) {
        if (cmd_name === motions[k][0]) {
            motions.splice(k, 1, list3);
            break;
        }
    }
    const XHR = new XMLHttpRequest();
    XHR.open("post", url + "/api/motions_replace_cmd", true);
    //    XHR.setRequestHeader("Content-Type", "application/json");
    XHR.send(JSON.stringify(list3));
    XHR.onreadystatechange = (e) => {
        if (XHR.readyState === XMLHttpRequest.DONE) {
            const status = XHR.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                console.log(XHR.responseText);
            }
        }
    }
}

function add_cmd() {
    const max_cmd = 10;
    let list3 = make_motionlist();
    for (let i = 1; i <= max_cmd; i++) {
        let found = false;
        let cmd_name = "New_" + i;
        motions.forEach(function (element) {
            if (element[0] === cmd_name) {
                found = true;
            }
        });
        if (!found) {
            list3[0] = cmd_name;
            motions.push(list3);
            create_cmd_list(cmd_name);
            break;
        }
    }
    const XHR = new XMLHttpRequest();
    XHR.open("post", url + "/api/motions_add_cmd", true);
    //    XHR.setRequestHeader("Content-Type", "application/json");
    //    XHR.setRequestHeader("Accept", "application/json");
    XHR.send(JSON.stringify(list3));
    XHR.onreadystatechange = (e) => {
        if (XHR.readyState === XMLHttpRequest.DONE) {
            const status = XHR.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                console.log(XHR.responseText);
            }
        }
    }
}

function delete_cmd() {
    let tbl = document.getElementById('cmd_list');
    let cmd_name0 = "";
    if (tbl.rows.length > 1) {
        let elems = document.getElementsByClassName("cname");
        for (let i = 0; i < elems.length; i++) {
            if (elems[i].classList.contains('is-btn-active')) {
                cmd_name0 = tbl.rows[i].children[0].innerText;
                tbl.deleteRow(i + 1);
                motions.splice(i, 1);
                let cmd_name = tbl.rows[0].children[0].innerText;
                if (i > 0) {
                    cmd_name = tbl.rows[i].children[0].innerText;
                }
                create_cmd_list(cmd_name);
                break;
            }
        }
    }
    if (cmd_name0 !== "") {
        const XHR = new XMLHttpRequest();
        XHR.open("GET", url + "/api/motions_delete_cmd?" + "cmd_name=" + cmd_name0, true);
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
}

function update_motions() {
    const XHR = new XMLHttpRequest();
    XHR.open("GET", url + "/api/save_motions?", true);
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

function anginc(w) {
    const elm = document.getElementById("number_" + w);
    val = parseInt(elm.value);
    if (isNaN(val)) { val = 0; }
    if (val >= 80) {
        val = 80 - 1;
    } else if (val < -80) {
        val = -80;
    }
    val += 1;
    elm.value = val;
    number2range(w);
}

function angdec(w) {
    const elm = document.getElementById("number_" + w);
    val = parseInt(elm.value);
    if (isNaN(val)) { val = 0; }
    if (val > 80) {
        val = 80;
    } else if (val <= -80) {
        val = -80 + 1;
    }
    val -= 1;
    elm.value = val;
    number2range(w);
}