import robo4
import json

class webcnt:

    def __init__ (self):
        self._robo = robo4.robo4()


    def _webpage_js(self, fjs):
        msgheader = "Content-Type: text/javascript\r\n"
        print(fjs)
        f = open(fjs)
        js = f.read()
        msgbody = str(js)
        return msgheader, msgbody

    def _webpage_css(self, fcss):
        msgheader = "Content-Type: text/css\r\n"
        f = open(fcss)
        css = f.read()
        msgbody = str(css)
        return msgheader, msgbody

    def _webpage_index(self):
        msgheader = "Content-Type: text/html\r\n"
        f = open("index.html")
        html = f.read()
        msgbody = str(html)
        return msgheader, msgbody

    def _webpage_direct(self):
        msgheader = "Content-Type: text/html\r\n"
        f = open("direct.html")
        html = f.read()
        msgbody = str(html)
        return msgheader, msgbody

    def _webpage_adjust(self):
        msgheader = "Content-Type: text/html\r\n"
        f = open("adjust.html")
        html = f.read()
        msgbody = str(html)
        return msgheader, msgbody

    def _api_get_angles(self, getpara):
        fr, hr, fl, hl = self._robo.get_angles()
        ans = {"fr":fr, "hr":hr, "fl":fl, "hl":hl}
        msgbody = json.dumps(ans)
        msgheader = "Content-Type: application/json\r\n"
        msgheader += "Access-Control-Allow-Origin: *\r\n"
        return msgheader, msgbody

    def _api_get_angles_ini(self, getpara):
        fr_ini, hr_ini, fl_ini, hl_ini = self._robo.get_angles_ini()
        ans = {"fr_ini":fr_ini, "hr_ini":hr_ini, "fl_ini":fl_ini, "hl_ini":hl_ini}
        msgbody = json.dumps(ans)
        msgheader = "Content-Type: application/json\r\n"
        msgheader += "Access-Control-Allow-Origin: *\r\n"
        return msgheader, msgbody

    def _api_set_angles(self, getpara):
        fr = getpara["fr"]
        hr = getpara["hr"]
        fl = getpara["fl"]
        hl = getpara["hl"]
        self._robo.set_angle_direct(fr, hr, fl, hl)
        ans = {"fr":fr, "hr":hr, "fl":fl, "hl":hl}
        msgbody = json.dumps(ans)
        msgheader = "Content-Type: application/json\r\n"
        msgheader += "Access-Control-Allow-Origin: *\r\n"
        return msgheader, msgbody

    def _api_set_angles_ini(self, getpara):
        fr_ini = getpara["fr_ini"]
        hr_ini = getpara["hr_ini"]
        fl_ini = getpara["fl_ini"]
        hl_ini = getpara["hl_ini"]
        self._robo.set_angles_ini(fr_ini, hr_ini, fl_ini, hl_ini)
        self._robo.set_angle_direct(0, 0, 0, 0)
        ans = {"fr_ini":fr_ini, "hr_ini":hr_ini, "fl_ini":fl_ini, "hl_ini":hl_ini}
        msgbody = json.dumps(ans)
        msgheader = "Content-Type: application/json\r\n"
        msgheader += "Access-Control-Allow-Origin: *\r\n"
        return msgheader, msgbody

    def _api_get_motions(self, getpara):
        ans = self._robo.motions
        msgbody = json.dumps(ans)
        msgheader = "Content-Type: application/json\r\n"
        msgheader += "Access-Control-Allow-Origin: *\r\n"
        return msgheader, msgbody

    def _api_get_paneldef(self, getpara):
        ans = self._robo.paneldef
        msgbody = json.dumps(ans)
        msgheader = "Content-Type: application/json\r\n"
        msgheader += "Access-Control-Allow-Origin: *\r\n"
        return msgheader, msgbody

    def _api_exe_command(self, getpara):
        ans = {"cmd_name": "not_specified"}
        if 'cmd_name' in getpara:
            cmd_name = getpara["cmd_name"]
            ans = {"cmd_name": "host_undefined"}
            if self._robo.set_request_name(cmd_name):
                ans = {"cmd_name": cmd_name}
        msgbody = json.dumps(ans)
        msgheader = "Content-Type: application/json\r\n"
        msgheader += "Access-Control-Allow-Origin: *\r\n"
        return msgheader, msgbody

    def _api_exe_cmd_list(self, payload):
        list = json.loads(payload)
        found = False
        for i in range(len(self._robo.motions)):
            if self._robo.motions[i][0] == list[0]:
                self._robo.motions[i] = list
                found = True
                break
        if not found:
            self._robo.motions.append(list)
        ans = {"cmd_name": "NG"}
        if self._robo.set_request_name(list[0]):
            ans = {"cmd_name": list[0]}
        msgbody = json.dumps(ans)
        msgheader = "Content-Type: application/json\r\n"
        msgheader += "Access-Control-Allow-Origin: *\r\n"
        return msgheader, msgbody

    def _api_motions_replace_cmd(self, payload):
        list = json.loads(payload)
        found = False
        for i in range(len(self._robo.motions)):
            if self._robo.motions[i][0] == list[0]:
                self._robo.motions[i] = list
                found = True
                break
        ans = {"cmd_name": list[0]}
        if not found:
            ans = {"cmd_name": "NG"}
        msgbody = json.dumps(ans)
        msgheader = "Content-Type: application/json\r\n"
        msgheader += "Access-Control-Allow-Origin: *\r\n"
        return msgheader, msgbody

    def _api_motions_add_cmd(self, payload):
        list = json.loads(payload)
        found = False
        for i in range(len(self._robo.motions)):
            if self._robo.motions[i][0] == list[0]:
                found = True
                break
        ans = {"cmd_name": "NG: already exists"}
        if not found:
            self._robo.motions.append(list)
            ans = {"cmd_name": list[0]}
        msgbody = json.dumps(ans)
        msgheader = "Content-Type: application/json\r\n"
        msgheader += "Access-Control-Allow-Origin: *\r\n"
        return msgheader, msgbody

    def _api_motions_delete_cmd(self, getpara):
        cmd_name = getpara["cmd_name"]
        found = False
        for i in range(len(self._robo.motions)):
            if self._robo.motions[i][0] == cmd_name:
                del self._robo.motions[i]
                found = True
                break
        ans = {"cmd_name": cmd_name + " Not found"}
        if found:
            ans = {"cmd_name": cmd_name}
        msgbody = json.dumps(ans)
        msgheader = "Content-Type: application/json\r\n"
        msgheader += "Access-Control-Allow-Origin: *\r\n"
        return msgheader, msgbody

    def _api_save_motions(self, getpara):
        for i in reversed(range(len(self._robo.motions))):
            if self._robo.motions[i][0] == "execmd_1":
                del self._robo.motions[i]
            elif self._robo.motions[i][0] == "execmd_2":
                del self._robo.motions[i]
        fstr = "motions = " + json.dumps(self._robo.motions)
        try:
            f = open('robo4_motions.py', 'w')
            f.write(fstr)
            f.close()
            ans = {"answer": "OK"}
        except:
            ans = {"answer": "NG"}
        msgbody = json.dumps(ans)
        msgheader = "Content-Type: application/json\r\n"
        msgheader += "Access-Control-Allow-Origin: *\r\n"
        return msgheader, msgbody


    def check_request(self, request):
        postpara = {}
        getpara = {}
        payload = ''
        try:
            payload = request.split('\\r\\n')[-1].replace("'","")
            if payload != '':
                temp = payload.split('&')
                for s in temp:
                    s2 = s.split('=')
                    if s2[1].isdigit():
                        s2[1] = int(s2[1])
                    elif s2[1][0] == '-':
                        s2[1] = 0 - int(s2[1][1:])
                    postpara[s2[0]] = s2[1]
            print(postpara)
        except IndexError:
            pass

        try:
            request = request.split()[1]
            temp0 = request.split('?')[-1]
            if temp0 != '':
                temp = temp0.split('&')
                for s in temp:
                    s2 = s.split('=')
                    if s2[1].isdigit():
                        s2[1] = int(s2[1])
                    elif s2[1][0] == '-':
                        s2[1] = 0 - int(s2[1][1:])
                    getpara[s2[0]] = s2[1]
            print(getpara)            
        except IndexError:
            pass

        msgheader = ""
        msgbody = ""

        if request.find('.css') != -1:
            tmp0 = request.split('.css')
            tmp1 = tmp0[0].split('/')
            if len(tmp1) == 2:
                msgheader, msgbody = self._webpage_css(tmp1[1] + '.css')            

        elif request.find('.js') != -1:
            tmp0 = request.split('.js')
            tmp1 = tmp0[0].split('/')
            if len(tmp1) == 2:
                msgheader, msgbody = self._webpage_js(tmp1[1] + '.js')            

        elif request.find('/index.html') != -1:
            msgheader, msgbody = self._webpage_index()

        elif request.find('/direct.html') != -1:
            msgheader, msgbody = self._webpage_direct()

        elif request.find('/adjust.html') != -1:
            self._robo.set_angle_direct(0, 0, 0, 0)
            msgheader, msgbody = self._webpage_adjust()

        elif request.find('/api/get_angles') != -1:
            msgheader, msgbody = self._api_get_angles(getpara)            

        elif request.find('/api/get_ini_angles') != -1:
            msgheader, msgbody = self._api_get_angles_ini(getpara)            

        elif request.find('/api/get_motions') != -1:
            msgheader, msgbody = self._api_get_motions(getpara)         

        elif request.find('/api/get_paneldef') != -1:
            msgheader, msgbody = self._api_get_paneldef(getpara)         

        elif request.find('/api/set_angles?') != -1:
            msgheader, msgbody = self._api_set_angles(getpara)            

        elif request.find('/api/set_ini_angles?') != -1:
            msgheader, msgbody = self._api_set_angles_ini(getpara)            

        elif request.find('/api/exe_command?') != -1:
            msgheader, msgbody = self._api_exe_command(getpara)   

        elif request.find('/api/exe_cmd_list') != -1:
            msgheader, msgbody = self._api_exe_cmd_list(payload)  

        elif request.find('/api/save_motions') != -1:
            msgheader, msgbody = self._api_save_motions(payload)  

        elif request.find('/api/motions_add_cmd') != -1:
            msgheader, msgbody = self._api_motions_add_cmd(payload)  

        elif request.find('/api/motions_replace_cmd') != -1:
            msgheader, msgbody = self._api_motions_replace_cmd(payload)  

        elif request.find('/api/motions_delete_cmd') != -1:
            msgheader, msgbody = self._api_motions_delete_cmd(getpara)  

        else:
            print('---- else case !!! ----')
            msgheader, msgbody = self._webpage_index()

        return msgheader, msgbody
