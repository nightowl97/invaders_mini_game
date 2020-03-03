import pyglet
import random, math
from pyglet import window
from pyglet import clock
from pyglet import font
from pyglet.window import key


def distance(a, b):
    """
    returns the euclidean distance
    """
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


class SpaceGame(window.Window):

    def __init__(self, *args, **kwargs):
        # All arguments go to superclass
        self.win = window.Window.__init__(self, *args, **kwargs)

        clock.schedule_interval(self.update, 1.0 / 30)  # update at 30 Hz
        clock.schedule_interval(self.create_alien, 1.0 / 5)  # update at 5 Hz

        self.score = pyglet.text.Label('Score: 0', font_name="Tahoma",
                                       font_size=14, x=self.width / 2, y=10)

        self.fpstext = pyglet.text.Label('', font_name="Tahoma",
                                         font_size=14, y=10)  # object to display the FPS

        # loading image
        self.spaceship_image = pyglet.image.load('images/ship3.png')
        self.spaceship_image.anchor_x = self.spaceship_image.width // 2
        self.spaceship_image.anchor_y = self.spaceship_image.height // 2
        self.spaceship = Spaceship(self.spaceship_image, x=200, y=50)

        self.alien_image = pyglet.image.load('images/invader.png')
        self.alien_image.anchor_x = self.spaceship_image.width // 2
        self.alien_image.anchor_y = self.spaceship_image.height // 2

        self.bullet_image = pyglet.image.load('images/bullet_white_16.png')
        self.bullet_image.anchor_x = self.bullet_image.width // 2
        self.bullet_image.anchor_y = self.bullet_image.height // 2

        self.aliens = []
        self.bullets = []

    def create_alien(self, dt):
        self.aliens.append(Alien(self.alien_image, x=random.randint(0, self.width), y=self.height))

    def update(self, dt):
        for alien in self.aliens:
            alien.update()
            if alien.dead:
                self.aliens.remove(alien)

        for bullet in self.bullets:
            bullet.update()
            if bullet.dead:
                self.bullets.remove(bullet)

    def on_draw(self):
        self.clear()
        clock.tick()

        self.fpstext.text = "fps: %d" % clock.get_fps()
        self.fpstext.draw()

        self.score.text = "Score: %d" % self.spaceship.kills
        self.score.draw()

        self.spaceship.draw()
        for alien in self.aliens:
            alien.draw()

        for bullet in self.bullets:
            bullet.draw()

        # Collisions
        for alien in self.aliens:
            for bullet in self.bullets:
                if distance(bullet, alien) < (bullet.width / 2 + alien.width / 2):
                    bullet.dead = True
                    alien.dead = True
                    self.spaceship.kills += 1
            if distance(alien, self.spaceship) < (alien.height / 2 + self.spaceship.height / 2):
                print("Your score is: {} kills".format(self.spaceship.kills))
                pyglet.app.exit()

    # Event handlers
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')
        if symbol == key.MOTION_LEFT:
            print("left")
        if symbol == key.MOTION_RIGHT:
            print("right")

    def on_mouse_motion(self, x, y, dx, dy):
        self.spaceship.x = x

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        self.bullets.append(Bullet(self.bullet_image, self.height,
                                   x=self.spaceship.x,
                                   y=self.spaceship.y))


####################################################################
class Spaceship(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        pyglet.sprite.Sprite.__init__(self, *args, **kwargs)
        self.kills = 0


####################################################################
class Alien(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        pyglet.sprite.Sprite.__init__(self, *args, **kwargs)
        self.x_velocity = random.randint(-3, 3)
        self.y_velocity = 5
        self.dead = False

    def update(self):
        self.x -= self.x_velocity
        self.y -= self.y_velocity
        if self.y < 0:
            self.dead = True


####################################################################
class Bullet(pyglet.sprite.Sprite):

    def __init__(self, imagedata, top, **kwargs):
        pyglet.sprite.Sprite.__init__(self, imagedata, **kwargs)
        self.y_velocity = 20
        self.top = top
        self.dead = False

    def update(self):
        self.y += self.y_velocity
        if self.y > self.top:
            self.dead = True


if __name__ == "__main__":
    win = SpaceGame(caption="aliens!", height=600, width=800)
    pyglet.app.run()
