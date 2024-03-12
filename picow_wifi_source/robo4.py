from machine import Timer
import micropython
import servo_sg90_kitronik5348
import robo4_angles_ini
import robo4_motions
import robo4_define_panel

class robo4:

    def __init__ (self):
        self._servomotor = servo_sg90_kitronik5348.PIOServo()
        self._angles = [90, 90, 90,90]
        self._angles_ini = [robo4_angles_ini.fr_ini, robo4_angles_ini.hr_ini, robo4_angles_ini.fl_ini, robo4_angles_ini.hl_ini]
        self._list_pointer = 0
        self._done = 1
        self._cmd_request = 'stop'
        self._update_angle()
        self._list2= []
        self._latest_d = ''
        self._playing_mode = ''
        self._repeat = 0
        self.motions = robo4_motions.motions
        self.paneldef = robo4_define_panel.paneldef
        self._intervalTimer = Timer()
        micropython.alloc_emergency_exception_buf(100)
        self._intervalTimer.init(mode=Timer.PERIODIC, freq=50, callback=self._timeover)

    def get_angles(self):
        fr = self._angles[0]
        hr = self._angles[1]
        fl = self._angles[2]
        hl = self._angles[3]
        return fr, hr, fl, hl

    def get_angles_ini(self):
        fr_ini = self._angles_ini[0]
        hr_ini = self._angles_ini[1]
        fl_ini = self._angles_ini[2]
        hl_ini = self._angles_ini[3]
        fstr = 'fr_ini = ' + str(fr_ini)
        fstr += '\n' + 'hr_ini = ' + str(hr_ini)
        fstr += '\n' + 'fl_ini = ' + str(fl_ini)
        fstr += '\n' + 'hl_ini = ' + str(hl_ini)
        return fr_ini, hr_ini, fl_ini, hl_ini

    def set_angles_ini(self, fr_ini, hr_ini, fl_ini, hl_ini):
        self._angles_ini = [fr_ini, hr_ini, fl_ini, hl_ini]
        fstr = 'fr_ini = ' + str(fr_ini)
        fstr += '\n' + 'hr_ini = ' + str(hr_ini)
        fstr += '\n' + 'fl_ini = ' + str(fl_ini)
        fstr += '\n' + 'hl_ini = ' + str(hl_ini)
        f = open('robo4_angles_ini.py', 'w')
        f.write(fstr)
        f.close()

    def set_angle_direct(self, fr, hr, fl, hl):
        cmd_diect = 'direct1'
        if self._latest_d == 'direct1':
            cmd_diect = 'direct2'
        self._latest_d = cmd_diect
        list = [cmd_diect, 'single', [[fr, hr, fl, hl, 0]]] 
        print(list)
        found = False
        for i in range(len(self.motions)):
            if self.motions[i][0] == list[0]:
                self.motions[i] = list
                found = True
                break
        if not found:
            self.motions.append(list)
        self.set_request_name(list[0])
    
    def set_request_name(self, name):
        for mo in self.motions:
            if mo[0] == name:
                self._cmd_request = name
                return True
        return False
        
    def _update_angle(self):
        for i in range(4):
            self._servomotor.goToPosition(i, self._angles[i] + self._angles_ini[i] - 90)

    def _timeover(self, timer):
        if self._done == 0:
            self._execute_a_command()
        else:
            self._check_command()

    def _execute_a_command(self):
        if len(self._list2) > 0:
            if self._list_pointer >= len(self._list2):
                self._list_pointer = 0
                if self._repeat == 0:
                    self._done = 1
                else:
                    if self._playing_mode != self._cmd_request:
                        self._cmd_stop()
            if 0 == self._set_angle(self._list2[self._list_pointer]):
                self._list_pointer += 1

    def _check_command(self):
        if self._playing_mode != self._cmd_request:
            print(self._playing_mode, self._cmd_request)
            for mo in self.motions:
                if mo[0] == self._cmd_request:
                    self._list2 = []
                    for p in mo[2]:
                        l = []
                        l.append(90 + p[0]) # FR
                        l.append(90 + p[1]) # HR
                        l.append(90 - p[2]) # FL
                        l.append(90 - p[3]) # HL
                        l.append(p[4])      # pitch
                        self._list2.append(l)
                    self._playing_mode = self._cmd_request
                    if mo[1] == "single":
                        self._cmd_single()
                    else:
                        self._cmd_repeat()
                    break

    def _set_angle(self, list):
        ans_set_angle = 0
        for i in range(4):
            self._angles[i] = self._get_angle(self._angles[i], list[i], list[-1])
            if self._angles[i] != list[i]:
                ans_set_angle += 1
            self._servomotor.goToPosition(i, self._angles[i] + self._angles_ini[i] - 90)
        return ans_set_angle

    def _get_angle(self, current, target, pitch):
        ans_get_angle = current
        if pitch == 0:
            ans_get_angle = target
        elif ans_get_angle >= target + pitch:
            ans_get_angle -= pitch
        elif ans_get_angle <= target - pitch:
            ans_get_angle += pitch
        else:
            ans_get_angle = target
        return ans_get_angle

    def _cmd_repeat(self):
        self._list_pointer = 0
        self._repeat = 1
        self._done = 0

    def _cmd_single(self):
        self._list_pointer = 0
        self._repeat = 0
        self._done = 0

    def _cmd_stop(self):
        self._list2 = [[90, 90, 90, 90, 3]]
        self._playing_mode = "stop"
        self._cmd_single()
