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


def main():
    run = True
    while run:
        clock.tick(fps)

        # draw background
        draw_bg()

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                run = False
        pyg.display.update()
    pyg.quit()


if __name__ == "__main__":
    main()
