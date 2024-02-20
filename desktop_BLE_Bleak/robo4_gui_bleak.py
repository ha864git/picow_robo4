from multiprocessing import Process, Queue
import asyncio
import sys
import bleak_uart_ifq

import PySimpleGUI as sg

def worker(qtx, qrx):
    
    tab1_layout  = [
        [sg.Column(
            [
                [
                    sg.Button('↑', font=('Arial',40), size=(4, 1), key='Button1'),
                ]
            ], justification='c')
        ],
        [sg.Column(
            [
                [
                    sg.Button('⟲', font=('Arial',40), size=(4, 1), key='Button2'),
                    sg.Button(' ', font=('Arial',40), size=(4, 1), key='Button3'),
                    sg.Button('⟳', font=('Arial',40), size=(4, 1), key='Button4')
                ]
            ], justification='c')
        ],
        [sg.Column(
            [
                [
                    sg.Button('↓', font=('Arial',40), size=(4, 1), key='Button5'),
                ]
            ], justification='c')
        ],
        [sg.Column(
            [
                [
                    sg.Button('up', font=('Arial',40), size=(4, 1), key='Button6'),
                ]
            ], justification='c')
        ],
        [sg.Column(
            [
                [
                    sg.Button('paw', image_filename='HandLeft.png', size=(4, 1), key='Button7'),
                    sg.Button('sit', font=('Arial',40), size=(4, 1), key='Button8'),
                    sg.Button('other paw', image_filename='HandRight.png', size=(4, 1), key='Button9')
                ]
            ], justification='c')
        ],
        [sg.Column(
            [
                [
                    sg.Button('down', font=('Arial',40), size=(4, 1), key='Button10'),
                ]
            ], justification='c')
        ],
    ]

    tab2_layout = [
        [sg.Column(
            [     
                [sg.Frame('RIGHT SIDE',
                    [
                        [
                            sg.Text('Hind leg',size=(22,1)),
                            sg.Text('Front leg',size=(20,1)),
                        ],
                        [
                            sg.Slider(key='-RightHindLeg-', range=(80,100), default_value=90, resolution=1, disable_number_display=False, orientation='h', size=(20, None), enable_events=True),
                            sg.Slider(key='-RightFrontLeg-', range=(80,100), default_value=90, resolution=1, disable_number_display=False, orientation='h', size=(20, None), enable_events=True)
                        ]
                    ])
                ]
            ], justification='c')
        ],
        [sg.Column(
            [     
                [sg.Frame('LEFT SIDE',
                    [
                        [
                            sg.Text('Front leg',size=(22,1)),sg.Text('Hind leg',size=(20,1)),
                        ],
                        [
                            sg.Slider(key='-LeftFrontLeg-', range=(80,100), default_value=90, resolution=1, disable_number_display=False, orientation='h', size=(20, None), enable_events=True),
                            sg.Slider(key='-LeftHindLeg-', range=(80,100), default_value=90, resolution=1, disable_number_display=False, orientation='h', size=(20, None), enable_events=True)
                        ]
                    ])
                ]
            ], justification='c')
        ],
        [sg.Column([[sg.Button('UPDATE', key='-update-')]], justification='c')],
        [sg.Text('',size=(22,1), key='-rightfront-')],
        [sg.Text('',size=(22,1), key='-righthind-')],
        [sg.Text('',size=(22,1), key='-leftfront-')],
        [sg.Text('',size=(22,1), key='-lefthind-')],
    ]

    layout = [
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab('PANEL', tab1_layout, key="tab1"),
                        sg.Tab('ADJUST', tab2_layout, key="tab2"),
                    ]
                ], key="tab_group", enable_events=True)
        ],
    ]

    while True:
        item = qrx.get()
        if item == 'conected':
            break
        elif item == 'notfound':
            sys.exit(1)

    window = sg.Window(
        title='BLE control panel for Biped Robot',
        layout=layout
    )
    window.finalize()

    button1 = window['Button1']
    button2 = window['Button2']
    button3 = window['Button3']
    button4 = window['Button4']
    button5 = window['Button5']
    button6 = window['Button6']
    button7 = window['Button7']
    button8 = window['Button8']
    button9 = window['Button9']
    button10 = window['Button10']

    button1.bind('<ButtonPress>', " Press", propagate=False)
    button2.bind('<ButtonPress>', " Press", propagate=False)
    button3.bind('<ButtonPress>', " Press", propagate=False)
    button4.bind('<ButtonPress>', " Press", propagate=False)
    button5.bind('<ButtonPress>', " Press", propagate=False)
    button6.bind('<ButtonPress>', " Press", propagate=False)
    button7.bind('<ButtonPress>', " Press", propagate=False)
    button8.bind('<ButtonPress>', " Press", propagate=False)
    button9.bind('<ButtonPress>', " Press", propagate=False)
    button10.bind('<ButtonPress>', " Press", propagate=False)

    button1.bind('<ButtonRelease>', " Release", propagate=False)
    button2.bind('<ButtonRelease>', " Release", propagate=False)
#    button3.bind('<ButtonRelease>', " Release", propagate=False)
    button4.bind('<ButtonRelease>', " Release", propagate=False)
    button5.bind('<ButtonRelease>', " Release", propagate=False)
#    button6.bind('<ButtonRelease>', " Release", propagate=False)
#    button7.bind('<ButtonRelease>', " Release", propagate=False)
#    button8.bind('<ButtonRelease>', " Release", propagate=False)
#    button9.bind('<ButtonRelease>', " Release", propagate=False)
#    button10.bind('<ButtonRelease>', " Release", propagate=False)

    def check_cmd(event):
        cmds = [
            ['Button1', 'forward', 'stop'],
            ['Button2', 'turn_left', 'stop'],
            ['Button3', 'stop', 'stop'],
            ['Button4', 'turn_right', 'stop'],
            ['Button5', 'backward', 'stop'],
            ['Button6', 'stop', 'stop'],
            ['Button7', 'paw', 'stop'],
            ['Button8', 'sit', 'stop'],
            ['Button9', 'other_paw', 'stop'],
            ['Button10', 'down', 'stop']
        ]
        args = event.split(' ')
        if len(args) == 2:
            for cmd in cmds:
                if args[0] == cmd[0]:
                    if args[1] == 'Press':
                        return cmd[1]
                    elif args[1] == 'Release':
                        return cmd[2]
        return ''

    while True:
        event, values = window.read(timeout=100,timeout_key='-timeout-')

        if event == sg.WIN_CLOSED:
            break
    
        elif event in '-timeout-':
            if qrx.qsize() != 0:
                rxstr = qrx.get()
            #    print('rxstr', rxstr)
                paras = rxstr.split(' ')
                if paras[0] == 'ri':
                    angles = paras[1].split(',')
                    if len(angles) == 4:
                        window['-RightHindLeg-'].Update(180 - int(angles[1]))
                        window['-RightFrontLeg-'].Update(int(angles[0]))
                        window['-LeftFrontLeg-'].Update(180 - int(angles[2]))
                        window['-LeftHindLeg-'].Update(int(angles[3]))
                        window['-rightfront-'].Update('angles_init[0] = ' + angles[0])
                        window['-righthind-'].Update('angles_init[1] = ' + angles[1])
                        window['-leftfront-'].Update('angles_init[2] = ' + angles[2])
                        window['-lefthind-'].Update('angles_init[3] = ' + angles[3])
                elif rxstr == 'quit':
                    break   # exit loop --> window close

        elif event in '-update-':
            fr_ini = int(values['-RightFrontLeg-'])
            hr_ini = int(values['-RightHindLeg-'])
            fl_ini = int(values['-LeftFrontLeg-'])
            hl_ini = int(values['-LeftHindLeg-'])
            txstr = 'si ' + str(fr_ini) + ',' + str(hr_ini) + ',' + str(fl_ini) + ',' + str(hl_ini) + ''
            qtx.put(txstr)
            window['-rightfront-'].Update('angles_init[0] = ' + str(fr_ini))
            window['-righthind-'].Update('angles_init[1] = ' + str(hr_ini))
            window['-leftfront-'].Update('angles_init[2] = ' + str(fl_ini))
            window['-lefthind-'].Update('angles_init[3] = ' + str(hl_ini))

        elif event=="tab_group":
            select_tab = values["tab_group"]
            if select_tab=="tab2":
                qtx.put('get angles_init')
                qtx.put('sa 0,0,0,0')

        ans = check_cmd(event)
        if ans != '':
            qtx.put(ans)

    qtx.put('quit')

    window.close()

    print('done worker')


if __name__ == "__main__":
    qtx = Queue()
    qrx = Queue()
    process = Process(target=worker, args=(qtx, qrx, ))
    process.start()

    ble = bleak_uart_ifq.ble_uart(qtx, qrx, ["mpy-uart", "BBC micro:bit"])

    try:
        asyncio.run(ble.uart_ifq())
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass

    process.join()
