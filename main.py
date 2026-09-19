import random

import pygame as pyg

from button import Button

pyg.init()

fps = 60
clock = pyg.time.Clock()

# game Window
bot_panel = 150
WIDTH = 800
HEIGHT = 600 + bot_panel

window = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("PY-FANTASY")

font = pyg.font.SysFont("Times New Roman", 26)


# color: r g b
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# assets
bg_img = pyg.image.load("img/Background/background.png").convert_alpha()
panel_img = pyg.image.load("img/Icons/panel.png").convert_alpha()
sword_img = pyg.image.load("img/Icons/sword.png").convert_alpha()
potion_img = pyg.image.load("img/Icons/potion.png").convert_alpha()


# helper for drawing background
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))


# helper for drawing background
def draw_bg():
    window.blit(bg_img, (0, 0))


# helper for drawing panel
def draw_panel():
    window.blit(panel_img, (0, HEIGHT - bot_panel))
    # draw stats
    draw_text(
        f"{fighter.name} HP: {fighter.hp}", font, red, 100, HEIGHT - bot_panel + 10
    )
    for count, i in enumerate(bandit_list):
        draw_text(
            f"{i.name} HP: {i.hp}",
            font,
            red,
            550,
            (HEIGHT - bot_panel + 10) + count * 60,
        )


# fighter class
class Fighter:
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions = potions
        self.start_potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # Idle: 0, Attack: 1, Damage: 2, Death: 3
        self.update_time = pyg.time.get_ticks()

        # Idle animation: 0
        temp_list = []
        for i in range(8):
            img = pyg.image.load(f"img/{self.name}/Idle/{i}.png")
            self.img = pyg.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            temp_list.append(self.img)
        self.animation_list.append(temp_list)

        # Attack animation: 1
        temp_list = []
        for i in range(8):
            img = pyg.image.load(f"img/{self.name}/Attack/{i}.png")
            self.img = pyg.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            temp_list.append(self.img)
        self.animation_list.append(temp_list)

        # Damage animation: 2
        temp_list = []
        for i in range(3):
            img = pyg.image.load(f"img/{self.name}/Hurt/{i}.png")
            self.img = pyg.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            temp_list.append(self.img)
        self.animation_list.append(temp_list)

        # Death animation: 3
        temp_list = []
        for i in range(10):
            img = pyg.image.load(f"img/{self.name}/Death/{i}.png")
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

    def attack(self, target):
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage

        target.damage()

        # check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()

        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_group.add(damage_text)

        self.action = 1
        self.frame_index = 0
        self.update_time = pyg.time.get_ticks()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pyg.time.get_ticks()

    def damage(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pyg.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pyg.time.get_ticks()

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
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()


# health bar class
class HealthBar:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp
        # calculate ratio
        ratio = self.hp / self.max_hp

        pyg.draw.rect(window, red, (self.x, self.y, 150, 20))
        pyg.draw.rect(window, green, (self.x, self.y, 150 * ratio, 20))


class DamageText(pyg.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pyg.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # float damage text up
        # delete text
        self.rect.y -= 1
        self.counter += 1

        if self.counter > 20:
            self.kill()


damage_group = pyg.sprite.Group()


fighter = Fighter(200, 260, "Knight", 30, 10, 3)
bandit1 = Fighter(550, 270, "Bandit", 20, 6, 1)
bandit2 = Fighter(700, 270, "Bandit", 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

fighter_health_bar = HealthBar(100, HEIGHT - bot_panel + 40, fighter.hp, fighter.max_hp)
bandit1_health_bar = HealthBar(550, HEIGHT - bot_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(
    550, HEIGHT - bot_panel + 40 + 60, bandit2.hp, bandit2.max_hp
)

potion_button = Button(window, 100, HEIGHT - bot_panel + 70, potion_img, 64, 64)

# game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
potion_effect = 15
attack = False
potions = False
clicked = False


def main():
    run = True

    current_fighter = 1
    action_cooldown = 0
    while run:
        clock.tick(fps)

        # draw game
        draw_bg()
        draw_panel()
        fighter_health_bar.draw(fighter.hp)
        bandit1_health_bar.draw(bandit1.hp)
        bandit2_health_bar.draw(bandit2.hp)

        # draw characters
        fighter.update()
        fighter.draw()
        for bandit in bandit_list:
            bandit.update()
            bandit.draw()

        # draw damage text
        damage_group.update()
        damage_group.draw(window)

        # reset variables
        attack = False
        potions = False
        target = None
        pos = pyg.mouse.get_pos()
        pyg.mouse.set_visible(True)  # visible mouse

        for count, bandit in enumerate(bandit_list):
            if bandit.rect.collidepoint(pos):
                pyg.mouse.set_visible(False)  # hide
                window.blit(sword_img, pos)
                if clicked is True and bandit.alive is True:
                    attack = True
                    target = bandit_list[count]
        if potion_button.draw():
            potions = True

        draw_text(str(fighter.potions), font, red, 150, HEIGHT - bot_panel + 70)

        # player action
        if fighter.alive is True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    # attack
                    if attack == True and target != None:
                        fighter.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                    # potion
                    elif potions == True:
                        if fighter.potions > 0:
                            if fighter.max_hp - fighter.hp > potion_effect:
                                healing = potion_effect
                            else:
                                healing = fighter.max_hp - fighter.hp
                            fighter.hp += healing
                            damage_text = DamageText(
                                fighter.rect.centerx,
                                fighter.rect.y,
                                str(healing),
                                green,
                            )
                            damage_group.add(damage_text)
                            fighter.potions -= 1
                            action_cooldown = 0

        # enemy action
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive is True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        # healing
                        if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                            if bandit.max_hp - bandit.hp > potion_effect:
                                healing = potion_effect
                            else:
                                healing = bandit.max_hp - bandit.hp
                            bandit.hp += healing
                            damage_text = DamageText(
                                bandit.rect.centerx,
                                bandit.rect.y,
                                str(healing),
                                green,
                            )
                            damage_group.add(damage_text)
                            bandit.potions -= 1
                            action_cooldown = 0
                            current_fighter += 1

                        # attack
                        else:
                            bandit.attack(fighter)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1
        # reset
        if current_fighter > total_fighters:
            current_fighter = 1

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                run = False
            if event.type == pyg.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
        pyg.display.update()

    pyg.quit()


if __name__ == "__main__":
    main()
