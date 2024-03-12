#
# panel define
#
#  "button_number": { "key": "nummber", "on": "command_name1", "off": "command_name2"}
#    nummber       --- panel button nummber
#    command_name1 --- execute a comannd when mousedown, touchstart
#    command_name2 --- execute a command when mouseup, touchend, mouseout, touchcancel
#
paneldef = [
    { "key": "1", "on": "forward", "off": "stop" },
    { "key": "2", "on": "turn_left", "off": "stop" },
    { "key": "3", "on": "stop", "off": "" },
    { "key": "4", "on": "turn_right", "off": "stop" },
    { "key": "5", "on": "backward", "off": "stop" },
    { "key": "6", "on": "stop", "off": "" },
    { "key": "7", "on": "other_paw", "off": "" },
    { "key": "8", "on": "sit", "off": "" },
    { "key": "9", "on": "paw", "off": "" },
    { "key": "10", "on": "down", "off": "" },
]