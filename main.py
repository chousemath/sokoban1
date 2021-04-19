from collections import defaultdict
import arcade

# Constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN_TITLE = 'Sokoban 1'
SPEED = 5

IMAGES = {
    'player': 'assets/images/player_05.png',
    'ground': 'assets/images/ground_05.png',
    'box': 'assets/images/crate_02.png',
    'wall': 'assets/images/ground_06.png',
    'target': 'assets/images/environment_06.png',
}
TILE_SIZE = 50
SCALING = {
    'player': TILE_SIZE/64,
    'ground': TILE_SIZE/64,
    'wall': TILE_SIZE/64,
    'box': TILE_SIZE/64,
    'target': TILE_SIZE/64,
}


class MyGame(arcade.Window):
    """Main application class"""

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.ground_list = None
        self.box_list = None
        self.wall_list = None
        self.wall_map = defaultdict(lambda: defaultdict(int))
        self.target_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        self.physics = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.player_list = arcade.SpriteList()
        self.box_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.ground_list = arcade.SpriteList(use_spatial_hash=True)
        self.target_list = arcade.SpriteList(use_spatial_hash=True)

        # set up the player and the player's position
        self.player_sprite = arcade.Sprite(IMAGES['player'], SCALING['player'])
        self.player_sprite.movement = {'key': None, 'end': None}
        self.player_sprite.center_x = TILE_SIZE/2
        self.player_sprite.center_y = TILE_SIZE/2
        self.player_list.append(self.player_sprite)

        # set up all the ground tiles
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                ground = arcade.Sprite(IMAGES['ground'], SCALING['ground'])
                ground.center_x = x + TILE_SIZE/2
                ground.center_y = y + TILE_SIZE/2
                self.ground_list.append(ground)

        wall_coordinates = [
            [25 + 100, 25 + 100],
            [25 + 200, 25 + 200],
            [25 + 200, 25 + 0],
        ]
        for coord in wall_coordinates:
            wall = arcade.Sprite(IMAGES['wall'], SCALING['wall'])
            wall.position = coord
            self.wall_list.append(wall)
            self.wall_map[coord[0]][coord[1]] = 1
        box_coordinates = [
            [25 + 500, 25 + 500],
            [25 + 400, 25 + 400],
        ]
        for coord in box_coordinates:
            box = arcade.Sprite(IMAGES['box'], SCALING['box'])
            box.position = coord
            self.box_list.append(box)
        target_coordinates = [
            [25 + 300, 25 + 400],
            [25 + 500, 25 + 600],
        ]
        for coord in target_coordinates:
            target = arcade.Sprite(IMAGES['target'], SCALING['target'])
            target.position = coord
            self.target_list.append(target)
        self.physics = arcade.PhysicsEngineSimple(
            self.player_sprite,
            self.wall_list)

    def on_draw(self):
        arcade.start_render()
        # Code to draw the screen goes here
        self.ground_list.draw()
        self.wall_list.draw()
        self.box_list.draw()
        self.target_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        if self.player_sprite.change_y or self.player_sprite.change_x:
            return
        if key == arcade.key.UP:
            end = self.player_sprite.center_y + TILE_SIZE
            if self.wall_map[self.player_sprite.center_x][end]:
                return
            self.player_sprite.movement = {'key': key, 'end': end}
            self.player_sprite.change_y = SPEED
        elif key == arcade.key.DOWN:
            end = self.player_sprite.center_y - TILE_SIZE
            if self.wall_map[self.player_sprite.center_x][end]:
                return
            self.player_sprite.movement = {'key': key, 'end': end}
            self.player_sprite.change_y = -SPEED
        elif key == arcade.key.LEFT:
            end = self.player_sprite.center_x - TILE_SIZE
            if self.wall_map[end][self.player_sprite.center_y]:
                return
            self.player_sprite.movement = {'key': key, 'end': end}
            self.player_sprite.change_x = -SPEED
        elif key == arcade.key.RIGHT:
            end = self.player_sprite.center_x + TILE_SIZE
            if self.wall_map[end][self.player_sprite.center_y]:
                return
            self.player_sprite.movement = {'key': key, 'end': end}
            self.player_sprite.change_x = SPEED

    def update(self, delta_time):
        # Move the player with the physics engine
        self.physics.update()
        key = self.player_sprite.movement['key']
        end = self.player_sprite.movement['end']
        if key == arcade.key.UP and self.player_sprite.center_y >= end:
            self.player_sprite.change_y = 0
            self.player_sprite.center_y = end
        elif key == arcade.key.DOWN and self.player_sprite.center_y <= end:
            self.player_sprite.change_y = 0
            self.player_sprite.center_y = end
        elif key == arcade.key.LEFT and self.player_sprite.center_x <= end:
            self.player_sprite.change_x = 0
            self.player_sprite.center_x = end
        elif key == arcade.key.RIGHT and self.player_sprite.center_x >= end:
            self.player_sprite.change_x = 0
            self.player_sprite.center_x = end


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
