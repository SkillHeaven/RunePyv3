from panda3d.core import Vec3
from direct.showbase.ShowBase import ShowBase

class Character:

    def __init__(self, render, loader, position=Vec3(0, 0, 0), scale=1):
        self.model = loader.loadModel("models/smiley")
        self.model.reparentTo(render)
        self.model.setPos(position)
        self.model.setScale(scale)

    def move_to(self, pos):
        self.model.setPos(pos)

    def get_position(self):
        return self.model.getPos()