import pygame as pyg

pyg.init()

fps = 60
clock = pyg.time.Clock()

# game Window
bot_panel = 150
WIDTH = 800
HEIGHT = 600 + bot_panel

window = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("PY-FANTASY")

# assets
bg_img = pyg.image.load("img/Background/background.png").convert_alpha()
panel_img = pyg.image.load("img/Icons/panel.png").convert_alpha()


# helper for drawing background
def draw_bg():
    window.blit(bg_img, (0, 0))


# helper for drawing panel
def draw_panel():
    window.blit(panel_img, (0, HEIGHT - bot_panel))


# fighter class
class Fighter:
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.strength = strength
        self.potions = potions
        self.start_potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 1
        self.update_time = pyg.time.get_ticks()

        temp_list = []

        for i in range(8):
            img = pyg.image.load(f"img/{self.name}/Idle/{i}.png")
            self.img = pyg.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            temp_list.append(self.img)

        self.animation_list.append(temp_list)

        temp_list = []

        for i in range(8):
            img = pyg.image.load(f"img/{self.name}/Attack/{i}.png")
            self.img = pyg.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            temp_list.append(self.img)

        self.animation_list.append(temp_list)
        self.img = self.animation_list[self.action][self.frame_index]
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        window.blit(self.img, self.rect)

    def update(self):
        animation_cooldown = 100
        # handle animation
        # load images
        self.img = self.animation_list[self.action][self.frame_index]
        # check time
        if pyg.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pyg.time.get_ticks()
            self.frame_index += 1
        # reset animation
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0


fighter = Fighter(200, 260, "Knight", 30, 10, 3)


def main():
    run = True
    while run:
        clock.tick(fps)

        # draw
        draw_bg()
        draw_panel()
        fighter.update()
        fighter.draw()

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                run = False
        pyg.display.update()
    pyg.quit()


if __name__ == "__main__":
    main()
