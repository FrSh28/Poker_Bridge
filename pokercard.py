'''
Copyright 2018 Yi-Fan Shyu. Some rights reserved.
CC BY-NC-SA
'''
from visual import*
from PIL import Image
import random as rd

def cardindex(a, b):
    return a * 13 + (b - 1)

def cardposition(n):
    if n%2:
        a = int(n/2)
        tpos = [vector(120*i, 0, 2*i) for i in range(-a, a+1)]
        return tpos
    else:
        a = n-1
        tpos = [vector(120*i*0.5, 0, 2*i*0.5) for i in range(-a, a+1, 2)]
        return tpos

vec_0 = vector(0, 0, 0)
p1, p2, p3, p4, initcard, throwaway = 0, 1, 2, 3, 4, 5
cards = []
def initpoker(gamecenter):
    initcardf = frame(pos = gamecenter, visible = False, destpos = vector(gamecenter), movet = 0, v = vec_0, destangle = 0, rotatet = 0, rps = 0, raxis = vec_0)
    for csuit in range(4):
        for cnum in range(1, 14):
            cindex = cardindex(csuit, cnum)
            im = Image.open("CardImage\\poker"+str(cindex)+".tga")
            tex = materials.texture(data = im, mapping = "sign", interpolate = False)
            cards.append(frame(frame = initcardf, pos = (0, 0, 77.5-cindex*1.5), axis = (0, 0, 1), suit = csuit, num = cnum, belong = initcard,
                               visible = True, edge = [vector(125, 0, 85), vector(-125, 0, 85), vector(125, 0, -85), vector(-125, 0, -85)],
                               destpos = vector(0, 0, cindex*1.51), movet = 0, v = vec_0, destangle = 0, rotatet = 0, rps = 0, raxis = vec_0))
            box(frame = cards[-1], pos = (0, 0, 0), axis = (1, 0, 0), height = 250, width = 170, length = 1.49, color = (1, 0.2, 0.15), material = tex)
    initcardf.rotate(axis = (1, 0, 0), angle = radians(-90))
    return initcardf

def shuffles(pokerf):
    for c in pokerf.objects:
        c.v = norm(vector(rd.uniform(-10, 10), rd.uniform(-10, 10), 0)) * 1500
        c.a = -c.v
    t = 0
    dt = 0.01
    move = True
    while move:
        rate(1/dt)
        for c in pokerf.objects:
            c.pos += c.v*dt;
            c.v += c.a*dt
            if abs(vector(c.pos.x, c.pos.y, 0)) < 5:
                c.pos = (0, 0, c.pos.z)
                c.v = vec_0
                c.a = vec_0
                move = False
    for c in pokerf.objects:
        c.pos = (0, 0, c.pos.z)
        c.v = vec_0
        c.a = vec_0

def movecard(card, endpos, endforward):
    card.v = (endpos-card.pos)*50
    card.rps = (card.axis).diff_angle(endforward)*50
    mt = 0
    mdt = 0.01
    move = 1
    rot = 1
    while move or rot:
        rate(1/mdt)
        mt += mdt
        if move:
            card.pos += card.v*mdt
            card.v = (endpos-card.pos)*50
            if abs(card.v)<5:
                card.pos = endpos
                card.v = 0
                move = 0
        if rot:
            card.rotate(angle = card.rps*mdt, axis = cross(card.axis, endforward))
            card.rps = (card.axis).diff_angle(endforward)*50
            if abs(card.rps)<0.02:
                card.axis = endforward
                card.rps = 0
                rot = 0

def clientmovecard(suit, num, movepos, forward):
    cindex = cardindex(suit, num)
    movecard(cards[cindex], cards[cindex].pos+movepos, forward)
    return cards[cindex]
    

passwordtext = [" |_ _ _ _  ", "  X|_ _ _  ", "  X X|_ _  ", "  X X X|_  ", "  X X X X| "]
class player:
    def __init__(self, IDnum, gamecenter, tablelength, forward):
        self.ID = IDnum
        self.name = ""
        self.view = forward
        self.cardf = frame(pos = gamecenter + tablelength*0.5*norm(vector(-forward.x, 0, -forward.z)) + vector(0, 200 ,0), axis = cross(vector(0, 1, 0), -forward))
        self.stricknum = -1
        self.strickpos = [((tablelength*0.35-(tablelength*0.35)/6*i)*norm(self.cardf.axis) + vector(0, gamecenter.y+0.1*i, 0) + (tablelength*0.3)*norm(vector(-forward.x, 0, -forward.z))) for i in range(13)]
        self.cardf.rotate(axis = self.cardf.axis, angle = radians(-25))
        self.throwpos = (gamecenter + (tablelength*0.1)*norm(vector(-forward.x, 0, -forward.z)))
        self.cards = []
        self.cardnum = 0
        self.cardpos = cardposition(13)
    
    def setname(self, n):
        self.name = n
    
    def addcard(self, pokerf, suit, num):
        cindex = cardindex(suit, num)
        cards[cindex].belong = self.ID
        temppos = pokerf.frame_to_world(cards[cindex].pos)
        cards[cindex].frame = None
        cards[cindex].pos = temppos
        cards[cindex].axis = (0, -1, 0)
        if self.ID:
            direction = +1
        else:
            direction = -1
        cards[cindex].rps = direction*(cards[cindex].frame_to_world(vector(0, 1, 0))-cards[cindex].pos).diff_angle(norm(vector(self.cardf.pos.x, 0, self.cardf.pos.z)))*50
        cards[cindex].raxis = vector(0, -1, 0)
        rdt = 0.01
        while True:
            rate(1/rdt)
            cards[cindex].rotate(angle = cards[cindex].rps*rdt, axis = cards[cindex].raxis)
            cards[cindex].rps = direction*(cards[cindex].frame_to_world(vector(0, 1, 0))-cards[cindex].pos).diff_angle(norm(vector(self.cardf.pos.x, 0, self.cardf.pos.z)))*50
            if abs(cards[cindex].rps) < 0.05:
                break
        cards[cindex].rotate(angle = cards[cindex].rps, axis = cards[cindex].raxis)
        movecard(cards[cindex], (self.cardf).frame_to_world(self.cardpos[self.cardnum]), norm(vector(self.cardf.pos.x, 0, self.cardf.pos.z)))
        cards[cindex].frame = self.cardf
        self.cards.append(cards[cindex])
        self.cards[-1].pos = self.cardpos[self.cardnum]
        self.cards[-1].axis = vector(0, 0, 1)
        self.cardnum += 1

    def getstrickpos(self):
        self.stricknum += 1
        return self.strickpos[self.stricknum]
    
    def throwcard(self, thrcard):
        thrcard.belong = throwaway
        temppos = self.cardf.frame_to_world(thrcard.pos)
        tempaxis = self.cardf.frame_to_world(thrcard.axis)
        thrcard.frame = None
        thrcard.pos = temppos
        thrcard.axis = tempaxis
        movecard(thrcard, self.throwpos, vector(0, 1, 0))
        del self.cards[self.cards.index(thrcard)]
        self.cardnum -= 1
        self.cardpos = cardposition(self.cardnum)
        for i in range(self.cardnum):
            self.cards[i].pos = self.cardpos[i]
    
    def __del__(self):
        self.cardf.visible = False
        del self.cardf
        for c in self.cards:
            c.visible = False
            for o in c.objects:
                o.visible = False
        del self.cards[:]
        
    
def initplayer(center, length):
    players = [player(p1, vector(center), length/2, vector(-cos(radians(30)), -sin(radians(30)), 0)),
               player(p2, vector(center), length/2, vector(0, -sin(radians(30)), -cos(radians(30)))),
               player(p3, vector(center), length/2, vector(cos(radians(30)), -sin(radians(30)), 0)),
               player(p4, vector(center), length/2, vector(0, -sin(radians(30)), cos(radians(30))))]
    return players

def terminate():
    for c in cards:
        c.visible = False
        for o in c.objects:
            o.visible = False
    del cards[:]
    

