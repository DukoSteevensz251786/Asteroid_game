import arcade
import random
import math


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Astroid Shooter"
PLAYER_MOVEMENT_SPEED = 5
BULLET_SPEED = 10



class GameView(arcade.Window):
   
    def add_score(self, points=1):
        self.score += points
        
    def __init__(self):

      
        
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.asteroids = None
        self.bullet_list = None
        self.gui_camera = None
        self.score = 0
        
        self.player_sprite = arcade.Sprite("Player_icon.png", 1.0)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_sprite.scale = 0.2

        self.backgrounds = [
            arcade.load_texture("Back1.png"),
            arcade.load_texture("Back2.png")
        ]
        self.current_background_index = 0
        self.background = self.backgrounds[self.current_background_index]

        self.time_since_last_switch = 0


        self.game_over = False
        self.game_over_text_timer = 0


    def on_mouse_press(self, x, y, button, modifiers):
        bullet = arcade.Sprite("Bullet.png",0.04)
 
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y
 
        dest_x = x
        dest_y = y
 
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)
 
        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")
 
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED
 
        self.bullet_list.append(bullet)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.setup()
        elif key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
 
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    
    def create_asteroid(self):
        asteroid = arcade.Sprite("asstroid.png", random.uniform(0.2,0.4))


      

        asteroid.center_x = WINDOW_WIDTH + 100
        asteroid.center_y = random.randint(0, WINDOW_HEIGHT)
        asteroid.change_x = random.uniform(-6, -1)
        asteroid.change_y = random.uniform(-1, 1)

        self.asteroids.append(asteroid)

       
       


    def on_update(self, delta_time):
        if self.game_over:
            self.game_over_text_timer += delta_time
            return

        self.time_since_last_switch += delta_time
        if self.time_since_last_switch >= 0.5:
            self.time_since_last_switch = 0
            self.current_background_index = (self.current_background_index + 1) % len(self.backgrounds)
            self.background = self.backgrounds[self.current_background_index]

        self.asteroids.update()
        self.player_sprite.update()
        self.bullet_list.update()

        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.asteroids)
            for asteroid in hit_list:
                asteroid.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()
                self.add_score()
            if (bullet.bottom > self.height or bullet.top < 0 or 
                bullet.right < 0 or bullet.left > self.width):
                bullet.remove_from_sprite_lists()

        hit_player = arcade.check_for_collision_with_list(self.player_sprite, self.asteroids)

        if hit_player:
            self.game_over = True  
            return

        if random.random() < 0.05:
            self.create_asteroid()


            
            
        

    def setup(self):
        self.asteroids = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()  

        self.player_list = arcade.SpriteList()  
        self.player_list.append(self.player_sprite) 


        for i in range(1):
            self.create_asteroid()

        self.gui_camera = arcade.Camera2D()
        self.score = 0
        

    def on_draw(self):
        
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.player_list.draw()
        self.asteroids.draw()
        self.bullet_list.draw()
        

        # Draw score
        self.gui_camera.use()
        arcade.draw_text(
            f"Score: {self.score}",
            10,
            WINDOW_HEIGHT - 30,
            arcade.color.WHITE,
            20
        )

        # Game Over overlay
        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                WINDOW_WIDTH / 2,
                WINDOW_HEIGHT / 2 + 20,
                arcade.color.RED,
                60,
                anchor_x="center"
            )
            arcade.draw_text(
                f"Final Score: {self.score}",
                WINDOW_WIDTH / 2,
                WINDOW_HEIGHT / 2 - 40,
                arcade.color.WHITE,
                30,
                anchor_x="center"
            )

def main():

    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()