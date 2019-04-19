from celeste import game

from . import celeste_object
from .player import Player
from .smoke import Smoke
from . import spring

import pico8 as p8

class FallFloor(celeste_object.CelesteObject):
    tile=23
    def __init__(self, x, y):
        super().__init__(x, y)
        self.state=0
        self.solid=True
        self.redraw = True

    def _break(self):
        if self.state==0:
            game.psfx(15)
            self.state=1
            self.delay=15 # how long until it falls
            game.objects.append(Smoke(self.x,self.y))
            s=self.collide(spring.Spring,0,-1)
            if s:
                spring._break()

    def update(self):
        # idling
        if self.state == 0:
            if (self.check(Player,0,-1) or
                self.check(Player,-1,0) or
                self.check(Player,1,0)):
                self._break()

        # shaking
        elif self.state==1:
            self.redraw = True
            self.delay-=1
            if self.delay<=0:
                self.state=2
                self.delay=60 #how long it hides for
                self.collideable=False

        # invisible, waiting to reset
        elif self.state==2:
            self.delay-=1
            if self.delay<=0 and not self.check(Player,0,0):
                game.psfx(7)
                self.state=0
                self.collideable=true
                game.objects.append(Smoke(self.x,self.y))

    def draw(self):
        if not self.redraw:
            return
        self.redraw = False
        if self.state!=2:
            if self.state!=1:
                p8.spr(23,self.x,self.y)
            else:
                p8.spr(23+(15-self.delay)/5,self.x,self.y)


# ugly monkey patch to allow CelesteObject to reference FallFloor
celeste_object.FallFloor = FallFloor
spring.FallFloor = FallFloor