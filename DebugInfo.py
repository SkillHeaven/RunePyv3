from direct.gui.DirectGui import OnscreenText
from panda3d.core import TextNode, Vec3

class DebugInfo:
    def __init__(self):
        self.text_object = OnscreenText(text="", pos=(-1.3, 0.9), scale=0.05,
                                        fg=(1, 1, 1, 1), align=TextNode.ALeft)

    def update_tile_info(self, mpos, tile_x, tile_y):
        self.text_object.setText(f"Mouse: ({mpos.getX()}, {mpos.getY()})\nTile: ({tile_x}, {tile_y})")
        #print(f"Mouse: ({mpos.getX()}, {mpos.getY()}) - Tile: ({tile_x}, {tile_y})")

    def update_distance_from_center(self, tile_x, tile_y):
        distance = (Vec3(tile_x, tile_y, 0) - Vec3(0, 0, 0)).length()
        direction = (Vec3(tile_x, tile_y, 0) - Vec3(0, 0, 0)).normalized()
        current_text = self.text_object.getText()
        new_text = current_text + f"\nDistance: {distance:.2f}\nDirection: ({direction.getX():.2f}, {direction.getY():.2f})"
        self.text_object.setText(new_text)