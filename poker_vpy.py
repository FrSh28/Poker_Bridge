'''
Copyright 2018 Yi-Fan Shyu. Some rights reserved.
CC BY-NC-SA
'''
from visual import*
from communicate import*
from pokercard import*

rdmess = ""
wrmess = ""

connect()
wrmess = "connected"+"\0"
write(wrmess)
wrmess = ""

keyf = ["left", "right", "up", "down", "tab", " "]

unit = 2500     # 1 meter

scene = display(title = "Poker::Bridge", x = 0, y = 0, height = 800, width = 1000, center = (0, 0, 0),
                lights = [local_light(pos = (0, 0.6*unit, 0), color = (0.4, 0.35, 0.05))], visible = False)
scene.ambient = color.gray(0.5)
scene.forward = (-cos(radians(20)), -sin(radians(20)), 0)
scene.range = (4000, 4000, 4000)
scene.autoscale = False
scene.userzoom = False
scene.userspin = False

#room
box(pos = (0, 0.75*unit, 0), length = 6*unit, height = 2.5*unit, width = 6*unit)
#light
light = frame(pos = scene.lights[0].pos, visible = True)
sphere(frame = light, pos = (0, 0, 0), radius = 0.1*unit, color = (0.9, 0.9, 0.5), material = materials.emissive)
extrusion(frame = light, pos = [(0, -0.1*unit, 0), (0, 0.2*unit, 0)], shape = shapes.circle(radius = 0.25*unit, thickness = 0.03*unit),
          color = color.gray(0.4), scale = [(1, 1), (0, 0)])
cylinder(frame = light, pos = (0, 0, 0), axis = (0, 1.3*unit, 0), radius = 0.02*unit, color = color.gray(0.4))
#table
box(pos = (0, -0.02*unit, 0), axis = (0, 0, 1), height = 0.04*unit, length = 1.2*unit, width = 1.2*unit, material = materials.wood)
cylinder(pos = (0, -0.5*unit, 0), axis = (0, 0.03*unit, 0), radius = 0.5*unit, material = materials.wood)
cylinder(pos = (0, -0.5*unit, 0), axis = (0, 0.48*unit, 0), radius = 0.05*unit, material = materials.wood)
#cover
scene.visible = True
cover = sphere(pos = (0, 0, 0), radius = 0.3*unit, opacity = 0.3, visible = False)
covercard = sphere(pos = (0, 0, 0), color = color.black, radius = 0.3*unit, visible = True)

playagain = True
while playagain:
    #create game
    playagain = False
    poker = initpoker(scene.center)
    players = initplayer(scene.center, 1.8*unit)

    #call demo
    callboard = frame(pos = (0.4*unit, 0.3*unit, 0), axis = (1, 0, 0), visible = False)
    box(frame = callboard, pos = (0, 0, 0), height = 0.35*unit, width = 0.5*unit, length = 0.001*unit, axis = (1, 0, 0), color = color.gray(0.3), opacity = 0.7)
    kind = ["C", "D", "H", "S", "NT"]
    buttons = []
    texts = []
    record = []
    for i in range(7):
        for j in range(5):
            buttons.append(box(frame = callboard, pos = (0.0005*unit, (0.1-j*0.05)*unit, (0.21-i*0.07)*unit), height = 0.048*unit, width = 0.068*unit, length = 0.001*unit, axis = (1, 0, 0), color = color.gray(0.7)))
            if j == 0 or j == 3:
                tcolor = color.black
            elif j == 1 or j == 2:
                tcolor = color.red
            else:
                tcolor = color.white
            texts.append(text(frame = callboard, text = str(i+1)+kind[j], align = "center",  pos = (0.001*unit, (0.085-j*0.05)*unit, (0.21-i*0.07)*unit), height = 50, axis = (0, 0, -1), color = tcolor))
    buttons.append(box(frame = callboard, pos = (0.0005*unit, -0.15*unit, 0), height = 0.048*unit, width = 0.1*unit, length = 0.001*unit, axis = (1, 0, 0), color = color.gray(0.7)))
    texts.append(text(frame = callboard, text = "PASS", align = "center",  pos = (0.001*unit, -0.16*unit, 0), height = 50, axis = (0, 0, -1), color = color.green))
    for i in range(4):
        record.append(text(frame = callboard, text = "p"+str(players[i].ID+1)+" :     ", align = "center",  pos = (0.001*unit, 0.14*unit, (0.18-0.12*i)*unit), height = 50, axis = (0, 0, -1), color = color.white))
    def call(p, cur):
        while scene.mouse.events:
            scene.mouse.getevent()
        temp = None
        tempcolor = color.gray(0.7)
        buttons[-1].color = color.gray(0.7)
        if p.ID == 0:
            callboard.axis = (1, 0, 0)
            callboard.rotate(angle = radians(25), axis = (0, 0, 1))
            callboard.pos = (0.3*unit, 0.3*unit, 0)
        elif p.ID == 1:
            callboard.axis = (0, 0, 1)
            callboard.rotate(angle = radians(25), axis = (-1, 0, 0))
            callboard.pos = (0, 0.3*unit, 0.3*unit)
        elif p.ID == 2:
            callboard.axis = (-1, 0, 0)
            callboard.rotate(angle = radians(25), axis = (0, 0, -1))
            callboard.pos = (-0.3*unit, 0.3*unit, 0)
        elif p.ID == 3:
            callboard.axis = (0, 0, -1)
            callboard.rotate(angle = radians(25), axis = (1, 0, 0))
            callboard.pos = (0, 0.3*unit, -0.3*unit)
        callboard.visible = True
        while True:
            rate(100)
            newobj = scene.mouse.pick
            if newobj in buttons:
                if not(temp == buttons.index(newobj)):
                    if not(temp == None):
                        buttons[temp].color = tempcolor
                    temp = buttons.index(newobj)
                    tempcolor = buttons[temp].color
                    if temp > cur:
                        buttons[temp].color = color.gray(1)
            elif newobj in texts:
                if not(temp == texts.index(newobj)):
                    if not(temp == None):
                        buttons[temp].color = tempcolor
                    temp = buttons.index(newobj)
                    tempcolor = buttons[temp].color
                    if temp > cur:
                        buttons[temp].color = color.gray(1)
            else:
                if not(temp == None):
                    buttons[temp].color = tempcolor
                temp = None
            
            if scene.mouse.events:
                mou = scene.mouse.getevent()
                if not(temp == None):
                    if mou.click == "left" and (cur == None or temp > cur):
                        if not(temp == 35):
                            cur = temp
                            for k in range(temp+1):
                                buttons[k].color = color.gray(0.4)
                        callmess = texts[temp].text
                        break
        callboard.visible = False
        if p.ID == 0:
            callboard.rotate(angle = radians(25), axis = (0, 0, -1))
        elif p.ID == 1:
            callboard.rotate(angle = radians(25), axis = (1, 0, 0))
        elif p.ID == 2:
            callboard.rotate(angle = radians(25), axis = (0, 0, 1))
        elif p.ID == 3:
            callboard.rotate(angle = radians(25), axis = (-1, 0, 0))
        return callmess, cur

    #password
    setting = frame(visible = False)
    setdemo = label(frame = setting, text = "", border = 60, height = 40, pos = scene.center, background = color.gray(0.7), color = color.black, xoffset = 0, yoffset = 0, line = False, box = False)
    settype = label(frame = setting, text = "", font = "monospace", height = 30, pos = scene.center, background = color.gray(0.2), color = color.gray(0.5), xoffset = 0, yoffset = -30, line = False, box = False)
    def typepass():
        while scene.kb.keys:
            scene.kb.getkey()
        i=0
        passw = "    "
        while True:
            ev = scene.waitfor("keydown")
            try:
                keyf.index(ev.key)
            except:
                if ev.key == "backspace":
                    if i>0 and passw[i-1] != " ":
                        i -= 1
                        settype.text = passwordtext[i]
                        passw = passw[:i]+" "+passw[i+1:]
                elif ev.key == "\n":
                    if i == 4:
                        break
                elif i<4 and len(ev.key):
                    passw = passw[:i]+str(ev.key)+passw[i+1:]
                    i += 1
                    settype.text = passwordtext[i]
        return passw

    #pass
    def trypass(p):
        setting.visible = True
        while True:
            setdemo.text = p.name+"\npassword:\n "
            settype.text = passwordtext[0]
            password = ""
            password = str(typepass())
            wrmess = password+"\0"
            write(wrmess)
            wrmess = ""
            rdmess = ""
            while True:
                rdmess = str(read())
                if cmp(rdmess, "None") and len(rdmess):
                    break
            messlist = rdmess.split("\0")
            if not cmp(messlist[0], "True"):
                break

    #cover
    covercard.visible = False
    cover.pos = scene.mouse.camera
    covercard.pos = scene.mouse.camera

    #start
    for i in range(10):
        rate(100)
        scene.forward = (-cos(radians(20)), -sin(radians(20)), 0)
        scene.range = (4000, 4000, 4000)
    while scene.mouse.events:
        scene.mouse.getevent()
    startmess = label(text = "Click to Start", font = "sans", border = 80, height = 40, pos = scene.center, background = color.gray(0.6), color = color.black, xoffset = 0, yoffset = 0, line = False, box = False)
    t = 0
    dt = 0.01
    scene.visible = True
    while not scene.mouse.events:
        rate(1/dt)
        t += dt
        scene.forward = (-cos(radians(20))*cos(0.1*t), -sin(radians(20)), -cos(radians(20))*sin(0.1*t))
        cover.pos = scene.mouse.camera
    light.visible = False
    for i in range(10):
        rate(100)
        scene.forward = (-1, -1, 0)
        scene.forward = (0, -1, 0)
        scene.range = (1500, 1500, 1500)
    covercard.pos = scene.mouse.camera
    covercard.visible = True
    cover.visible = False
    scene.mouse.getevent()
    startmess.visible = False
    del startmess

    #set player
    wrmess = "setplayer"+"\0"
    write(wrmess)
    wrmess = ""
    setting.visible = True
    for p in players:
        wrmess = str(p.ID)+"\0"
        write(wrmess)
        wrmess = ""
        name = "                "
        setdemo.text = "player "+str(p.ID+1)+" name:\n "
        settype.text = name
        i=0
        while True:
            ev = scene.waitfor("keydown")
            try:
                keyf.index(ev.key)
            except:
                if ev.key == "backspace":
                    if i>0 and name[i-1] != " ":
                        i -= 1
                        settype.text = settype.text[:i]+" "+settype.text[i+1:]
                        name = name[:i]+" "+name[i+1:]
                elif ev.key == "\n":
                    if i>0:
                        name = name[:i]
                        break
                    else:
                        name = "player_"+str(p.ID+1)
                        break
                elif i<10 and len(ev.key):
                    name = name[:i]+str(ev.key)+name[i+1:]
                    settype.text = settype.text[:i]+str(ev.key)+settype.text[i+1:]
                    i += 1
        messlist = name.split(" ")
        name = messlist[0]
        setdemo.text = name+"\npassword:\n "
        p.setname(name)
        settype.text = passwordtext[0]
        password = ""
        password = str(typepass())
        wrmess = name+" "+password+"\0"
        write(wrmess)
        wrmess = ""
    setting.visible = False
    covercard.visible = False

    #shuffles
    poker.visible = True
    poker.v = vector(0, 0.1*unit, 0)
    poker.a = -0.5*poker.v
    poker.raxis = vector(1, 0, 0)
    poker.rps = 60
    t = 0
    dt = 0.01
    end = 0
    while True:
        rate(1/dt)
        t += dt
        poker.pos += poker.v*dt
        poker.v += poker.a*dt
        if t>0.3 and t<3.29:
            poker.rotate(angle = radians(poker.rps*dt), axis = poker.raxis)
        if end and abs(poker.pos-vector(0, 78, 0)) < 5:
            break
        if abs(poker.v)<5:
            end = 1
    poker.pos = (0, 78, 0)
    poker.v = vec_0
    poker.a = vec_0
    poker.rps = 0
    sleep(1)
    shuffles(poker)

    #get card info & deal
    rdmess = ""
    while True:
        rdmess = str(read())
        if cmp(rdmess, "None") and len(rdmess):
            break
    messlist = rdmess.split("\0")
    if cmp(messlist[0], "cardinfo"):
        exit()
    
    for i in range(4):
        rdmess = ""
        while True:
            rdmess = str(read())
            if cmp(rdmess, "None") and len(rdmess):
                break
        messlist = rdmess.split("\0")
        ID = int(messlist[0])
        for j in range(13):
            rdmess = ""
            while True:
                rdmess = str(read())
                if cmp(rdmess, "None") and len(rdmess):
                    break
            messlist = rdmess.split("\0")
            cardinfo = messlist[0].split(" ")
            players[ID].addcard(poker, int(cardinfo[0]), int(cardinfo[1]))

    light.visible = True

    #call the king
    wrmess = "calltheking"+"\0"
    write(wrmess)
    wrmess = ""
    curking = None
    king = ""
    while True:
        while True:
            rdmess = str(read())
            if cmp(rdmess, "None") and len(rdmess):
                break
        messlist = rdmess.split("\0")
        if not cmp(messlist[0], "setOK"):
            break
        elif not cmp(messlist[0], "restart"):
            playagain = True
            break
        p = players[int(messlist[0])]
        covercard.visible = True
        for i in range(10):
            rate(100)
            scene.forward = p.view
            scene.range = (1700, 1700, 1700)
            covercard.pos = scene.mouse.camera
            cover.pos = scene.mouse.camera
        rdmess = ""
        trypass(p)
        covercard.visible = False
        setting.visible = False
        tempmess, curking = call(p, curking)
        covercard.visible = True
        tempmess = str(tempmess)
        record[p.ID].text = "p"+str(p.ID+1)+" :  "+tempmess
        if tempmess == "PASS":
            wrmess = "pass"+"\0"
        else:
            wrmess = tempmess[0]
            king = tempmess
            if tempmess[1] == "C":
                wrmess += " clubs"+"\0"
            elif tempmess[1] == "D":
                wrmess += " diamonds"+"\0"
            elif tempmess[1] == "H":
                wrmess += " hearts"+"\0"
            elif tempmess[1] == "S":
                wrmess += " spades"+"\0"
            elif tempmess[1] == "N":
                wrmess += " notrump"+"\0"
        write(wrmess)
        wrmess = ""
    callboard.visible = False
    for o in callboard.objects:
        o.visible = False
    del callboard
    del buttons[:]
    del texts[:]
    del record[:]
    if playagain:
        terminate()
        for o in setting.objects:
            o.visible = False
        del setting
        del setdemo
        del settype
        for c in poker.objects:
            c.visible = False
            for o in c.objects:
                o.visible = False
        del players[:]
        continue

    #play
    suit = ["C", "D", "H", "S"]
    strnum = ["", "A ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "10", "J ", "Q ", "K ", ]
    covercard.pos = scene.mouse.camera
    covercard.visible = True
    roundcount = 0
    roundnum = label(text = "Round: "+str(roundcount)+"    ", font = "serif", height = 30, pos = scene.center, color = color.gray(0.7), xoffset = 355, yoffset = 345, line = False, box = False)
    kingdemo = label(text = "   King: "+king, font = "serif", height = 30, pos = scene.center, color = color.gray(0.7), xoffset = -355, yoffset = 345, line = False, box = False)
    playerplay = label(text = "p1:"+"     "+"p2:"+"     "+"p3:"+"     "+"p4:"+"     ", font = "sans", height = 30, pos = scene.center, color = color.gray(0.7), xoffset = 0, yoffset = 320, line = False, box = False)
    wrmess = "gaming"+"\0"
    write(wrmess)
    wrmess = ""
    while roundcount < 13:
        roundcount += 1
        roundnum.text = "Round: "+str(roundcount)+"    "
        playcards = []
        play = ["     ", "     ", "     ", "     "]
        playerplay.text = "p1: "+play[p1]+" p2: "+play[p2]+" p3: "+play[p3]+" p4: "+play[p4]
        for i in range(4):
            while True:
                rdmess = str(read())
                if cmp(rdmess, "None") and len(rdmess):
                    break
            messlist = rdmess.split("\0")
            p = players[int(messlist[0])]
            covercard.visible = True
            for i in range(10):
                rate(100)
                scene.forward = p.view
                covercard.pos = scene.mouse.camera
            rdmess = ""
            trypass(p)
            covercard.visible = False
            setting.visible = False
            available = []
            while True:
                rdmess = ""
                while True:
                    rdmess = str(read())
                    if cmp(rdmess, "None") and len(rdmess):
                        break
                messlist = rdmess.split("\0")
                if not cmp(messlist[0], "ends"):
                    break
                cardinfo = messlist[0].split(" ")
                available.append(clientmovecard(int(cardinfo[0]), int(cardinfo[1]), vector(0, 0.01*unit, 0), vector(0, 0, 1)))
            while scene.mouse.events:
                scene.mouse.getevent()
            temp = None
            while True:
                rate(100)
                newobj = scene.mouse.pick
                if hasattr(newobj, "frame") and (newobj.frame in available):
                    if not(temp == newobj.frame):
                        if not(temp == None):
                            clientmovecard(temp.suit, temp.num, vector(0, -0.01*unit, 0), temp.axis)
                        temp = newobj.frame
                        clientmovecard(temp.suit, temp.num, vector(0, 0.01*unit, 0), temp.axis)
                else:
                    if not(temp == None):
                        clientmovecard(temp.suit, temp.num, vector(0, -0.01*unit, 0), temp.axis)
                    temp = None
                if scene.mouse.events:
                    mou = scene.mouse.getevent()
                    if not(temp == None):
                        if mou.click == "left":
                            clientmovecard(temp.suit, temp.num, vector(0, -0.02*unit, 0), temp.axis)
                            break
            play[p.ID] = suit[temp.suit]+" "+strnum[temp.num]
            playerplay.text = "p1: "+play[p1]+" p2: "+play[p2]+" p3: "+play[p3]+" p4: "+play[p4]
            wrmess = str(temp.suit)+" "+str(temp.num)+"\0"
            write(wrmess)
            wrmess = ""
            playcards.append(temp)
            p.throwcard(temp)
        sleep(0.1)
        light.visible = False
        for i in range(10):
            rate(100)
            scene.forward = (-1, -1, 0)
            scene.forward = (0, -1, 0)
            scene.range = (1500, 1500, 1500)
        while scene.kb.keys:
            scene.kb.getkey()
        while scene.mouse.events:
            scene.mouse.getevent()
        scene.waitfor("click keydown")
        while True:
            rdmess = str(read())
            if cmp(rdmess, "None") and len(rdmess):
                break
        messlist = rdmess.split("\0")
        win = players[int(messlist[0])]
        temppos = win.getstrickpos()
        i = 0
        for card in playcards:
            movecard(card, temppos+vector(0, 1*i, 0), vector(0, 1, 0))
            i += 1
        sleep(0.1)
        light.visible = True
    playerplay.visible = False
    del playerplay
    setting.visible = False
    for o in setting.objects:
        o.visible = False
    del setting
    del setdemo
    del settype
        
    #score
    for i in range(10):
        rate(100)
        scene.forward = (-cos(radians(20)), -sin(radians(20)), 0)
        scene.range = (4000, 4000, 4000)
    cover.pos = scene.mouse.pos
    cover.visible = True
    winboard = label(text = "winner:\n \n \n \n \n \n ", font = "sans", border = 70, height = 40, pos = scene.center, background = color.gray(0.6), color = color.black, xoffset = 0, yoffset = 0, line = False, box = False, visible = False)
    loseboard = label(text = "", font = "sans", height = 35, pos = scene.center, opacity = 0, background = color.black, color = color.black, xoffset = 0, yoffset = -15, line = False, box = False, visible = False)
    t = 0
    dt = 0.01
    while True:
        rdmess = str(read())
        if cmp(rdmess, "None") and len(rdmess):
            break
    messlist = rdmess.split("\0")
    if cmp(messlist[0], "score"):
        exit()
    while True:
        rdmess = str(read())
        if cmp(rdmess, "None") and len(rdmess):
            break
    messlist = rdmess.split("\0")
    winner = players[int(messlist[0])]
    for i in range(2):
        while True:
            rdmess = str(read())
            if cmp(rdmess, "None") and len(rdmess):
                break
        messlist = rdmess.split("\0")
        messlist = messlist[0].split(" ")
        if not(cmp(messlist[0], str(winner.ID))):
            winboard.text = "winner:\n"+winner.name+"\n"+players[winner.ID-2].name+"\nScore : "+messlist[1]+"\n \n \n "
        else:
            loseboard.text = players[winner.ID-1].name+"\n"+players[winner.ID-3].name+"\nScore : "+messlist[1]
    winboard.visible = True
    loseboard.visible = True
    while scene.mouse.events:
        scene.mouse.getevent()
    while not scene.mouse.events:
        rate(1/dt)
        t += dt
        scene.forward = (-cos(radians(20))*cos(0.1*t), -sin(radians(20)), -cos(radians(20))*sin(0.1*t))
        cover.pos = scene.mouse.camera
    roundnum.visible = False
    del roundnum
    kingdemo.visible = False
    del kingdemo
    winboard.visible = False
    del winboard
    loseboard.visible = False
    del loseboard

    #again
    cover.pos = scene.mouse.camera
    cover.visible = True
    againboard = label(text = "Play Again?\n \n \n ", font = "sans", border = 70, height = 40, pos = scene.center, background = color.gray(0.6), color = color.black, xoffset = 0, yoffset = 0, line = False, box = False)
    yes = label(text = "Yes", font = "sans", border = 10, height = 40, pos = scene.center, background = color.gray(0.4), color = color.green, xoffset = -10, yoffset = 0, line = False, box = False)
    no = label(text = "No", font = "sans", border = 10, height = 40, pos = scene.center, background = color.gray(0.4), color = color.red, xoffset = 10, yoffset = 0, line = False, box = False)
    note = label(text = "use Left , Right and Enter key", font = "sans", height = 25, pos = scene.center, opacity = 0, background = color.black, color = color.black, xoffset = 0, yoffset = -50, line = False, box = False)
    chosen = "yes"
    yes.background = color.gray(0.7)
    t = 0
    dt = 0.01
    while scene.kb.keys:
        scene.kb.getkey()
    while True:
        rate(1/dt)
        t += dt
        scene.forward = (-cos(radians(20))*cos(0.1*t), -sin(radians(20)), -cos(radians(20))*sin(0.1*t))
        cover.pos = scene.mouse.camera
        if scene.kb.keys:
            key = scene.kb.getkey()
            if key == "left" and chosen == "no":
                chosen = "yes"
                yes.background = color.gray(0.7)
                no.background = color.gray(0.4)
            elif key == "right" and chosen == "yes":
                chosen = "no"
                no.background = color.gray(0.7)
                yes.background = color.gray(0.4)
            if key == "\n":
                if chosen == "yes":
                    wrmess = "playagain"+"\0"
                    playagain = True
                    break
                else:
                    wrmess = "False"+"\0"
                    playagain = False
                    break
    write(wrmess)
    wrmess = ""
    covercard.pos = scene.mouse.camera
    covercard.visible = True
    cover.visible = False
    againboard.visible = False
    del againboard
    yes.visible = False
    del yes
    no.visible = False
    del no
    note.visible = False
    del note
    
    terminate()
    for c in poker.objects:
        c.visible = False
        for o in c.objects:
            o.visible = False
    del players[:]

exit()



