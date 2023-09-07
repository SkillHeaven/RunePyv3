from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import random
from Character import Character
from DebugInfo import DebugInfo


class TileMap(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.debug_info = DebugInfo()
        tile_size = 1
        map_radius = 5  # Number of tiles from the center to the edge, not including center
        map_width = map_height = map_radius * 2 + 1
        self.tiles = []

        self.middle_mouse_down = False
        self.last_mouse_pos = (0, 0)

        base.mouseWatcherNode.set_modifier_buttons(ModifierButtons())
        base.buttonThrowers[0].node().set_modifier_buttons(ModifierButtons())

        tile_fit_scale = tile_size * 0.5  # Scale the model to 50% of the tile size for some padding
        self.character = Character(self.render, self.loader, Vec3(0, 0, 0.5), scale=tile_fit_scale)

        self.disableMouse()

        for x in range(-map_radius, map_radius + 1):  # will loop from -5 to 5
            for y in range(-map_radius, map_radius + 1):
                tile = self.create_tile((x * tile_size, y * tile_size, 0), tile_size)
                random_color = (random.random(), random.random(), random.random(), 1)
                tile.setColor(random_color)
                tile.setName(f"tile_{x}_{y}")

        self.accept("wheel_up", self.zoom, [-1])
        self.accept("wheel_down", self.zoom, [1])
        self.accept('mouse1', self.tile_click_event)

        self.setBackgroundColor(0.5, 0.5, 0.5)
        self.camera.setPos(0,0,10)
        self.camera.lookAt(0,0,0)

        self.accept('mouse3', self.middle_mouse_down_event)
        self.accept('mouse3-up', self.middle_mouse_up_event)
        self.taskMgr.add(self.middle_mouse_drag_event, 'middleMouseTask')
        self.taskMgr.add(self.update_tile_hover, 'updateTileHoverTask')

    def create_tile(self, position, size):
        card_maker = CardMaker("tile")
        card_maker.setFrame(-size/2, size/2, -size/2, size/2) #size of the card
        tile = self.render.attachNewNode(card_maker.generate())
        tile.setPos(*position)
        tile.setHpr(0,-90,0)
        tile.setName(f"tile_{position[0]}_{position[1]}")
        return tile

    def get_mouse_tile_coords(self):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            tile_x = round(mpos.getX() * 10)
            tile_y = round(mpos.getY() * 10)
            return mpos, tile_x, tile_y
        return None, None, None

    def zoom(self, direction):
        zoom_speed = 10
        cam_vec = self.render.getRelativeVector(self.camera, Vec3.forward())
        self.camera.setPos(self.camera.getPos() - cam_vec * direction * zoom_speed)
    def middle_mouse_down_event(self):
        self.middle_mouse_down = True
        if self.mouseWatcherNode.hasMouse():
            self.last_mouse_pos = self.mouseWatcherNode.getMouse()

    def middle_mouse_up_event(self):
        self.middle_mouse_down = False

    def middle_mouse_drag_event(self, task):
        if not self.middle_mouse_down:
            return task.cont
        if self.mouseWatcherNode.hasMouse():
            current_mouse_pos = self.mouseWatcherNode.getMouse()
            delta_x = current_mouse_pos[0] - self.last_mouse_pos[0]
            self.camera.setH(self.camera.getH() - delta_x * 100)  # Adjust sensitivity as needed
            self.last_mouse_pos = current_mouse_pos
        return task.cont

    def get_tile_from_mouse(self):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            tile_x = round(mpos.getX() * 10)
            tile_y = round(mpos.getY() * 10)
            return tile_x, tile_y
        return None, None

    def update_tile_hover(self, task):
        mpos, tile_x, tile_y = self.get_mouse_tile_coords()
        if mpos:
            self.debug_info.update_tile_info(mpos, tile_x, tile_y)

        return task.cont

    def tile_click_event(self):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            tile_x = round(mpos.getX() * 10)
            tile_y = round(mpos.getY() * 10)

            # Print the coordinates
            print(f"Clicked - Mouse: ({mpos.getX()}, {mpos.getY()}) | Tile: ({tile_x}, {tile_y})")

            # Update debug info display
            self.debug_info.update_tile_info(mpos, tile_x, tile_y)

            clicked_tile = None
            try:
                clicked_tile = self.render.find(f"**/tile_{tile_x}_{tile_y}")
            except Exception as e:
                print(f"Error finding tile: {e}")
            if clicked_tile:
                self.character.move_to(Vec3(tile_x, tile_y, 0.5))

                # After moving, get the character's position
                char_pos = self.character.get_position()
                print(f"Character moved to: ({char_pos.getX()}, {char_pos.getY()}, {char_pos.getZ()})")

if __name__ == "__main__":
    app = TileMap()
    app.run()
