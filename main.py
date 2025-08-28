from pytmx.util_pygame import load_pygame
import pygame
import random
import sys


from Fight_Scene.Character.Enemy_02 import Hooded
from Fight_Scene.Character.Fight_01 import Saber
from Fight_Scene.Character.Enemy_03 import WizardQ
from Fight_Scene.Character.Enemy_01 import WIZARD
from Map.Code.Map import Player
from Map.Code.Map import HOUSE
from Map.Code.Map import TREE
from Map.Code.Map import Monster
from Map.Code.Map import Tile


# chuan
pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# define color
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# define game variables
last_count_update = pygame.time.get_ticks()


WARRIOR_SIZE = 162
WARRIOR_SCALE = 3
WARRIOR_OFFSET = [65, 40]  # 72 56
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

WIZARD_SIZE = 66.8
WIZARD_SCALE = 7
WIZARD_OFFSET = [27, 20]  # 112 107
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

HOODED_SIZE = 32
HOODED_SCALE = 4
HOODED_OFFSSET = [27, -15]
HOODED_DATA = [HOODED_SIZE, HOODED_SCALE, HOODED_OFFSSET]

WIZZARDQ_SIZE = 32
WIZZARDQ_SCALE = 4
WIZZARDQ_OFFSSET = [27, -17]
WIZZARDQ_DATA = [WIZZARDQ_SIZE, WIZZARDQ_SCALE, WIZZARDQ_OFFSSET]

count_font = pygame.font.Font("Fight_Scene/Turok.ttf", 80)
score_font = pygame.font.Font("Fight_Scene/Turok.ttf", 60)
text_font = pygame.font.Font("Fight_Scene/Turok.ttf", 30)

screen2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighting!")


# load bg image
bg_image_0 = pygame.image.load(
    "Fight_Scene/Picture/Fight_background_5.jpg"
).convert_alpha()
bg_image = pygame.transform.scale(bg_image_0, (SCREEN_WIDTH, SCREEN_HEIGHT))

warrior_sheet = pygame.image.load("Fight_Scene/Picture/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("Fight_Scene/Picture/wizard.png").convert_alpha()
hooded_sheet = pygame.image.load("Fight_Scene/Picture/Hooded.png").convert_alpha()
wizardq_sheet = pygame.image.load("Fight_Scene/Picture/Wizard_Q.png").convert_alpha()

WARRIOR_ANIMATTION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATTION_STEPS = [8, 8, 1, 8, 8, 3, 7]
HOODED_ANIMATTION_STEPS = [2, 2, 4, 8, 6, 8, 3, 8, 8]
WIZARDQ_ANIMATTION_STEPS = [2, 4, 6, 8, 10, 8, 10, 8]

Enemy_x = 700
Enemy_y = 310
Player_x = 210
Player_y = 310


def draw_fightbg():
    screen2.blit(bg_image, (0, 0))


# draw blood line
def draw_blood_line(blood, x, y, cnt=4):
    ratio = blood / (80 + cnt * 20)
    pygame.draw.rect(screen2, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen2, RED, (x, y, 400, 30))
    pygame.draw.rect(screen2, GREEN, (x, y, 400 * ratio, 30))


# chuan


# wen
MOSPOS = []
TREE1 = []
TREE2 = []
TREE3 = []
HOUSE1 = []
DEC = []
DEC1 = []

SCROLL_LEFT = False
SCROLL_RIGHT = False
SCROLL_UP = False
SCROLL_DOWN = False
scrollrl = 0
scrollud = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen2.blit(img, (x, y))


TMX = load_pygame("Map/Data/tmx/Map.tmx")
clock = pygame.time.Clock()
FPS = 30

# BACKGROUDND LAYER
SEA = pygame.sprite.Group()
BACKGROUND = pygame.sprite.Group()
BACKGROUNDOBJ = pygame.sprite.Group()

# GET LAYER OF TILES
for layer in TMX.visible_layers:
    if layer.name == "SEA":
        print(layer.tiles())
        for x, y, surf in layer.tiles():
            pos = (x * 32, y * 32)
            T = Tile(pos, surf, SEA)

    if layer.name == "GROUND":
        for x, y, surf in layer.tiles():
            pos = (x * 32, y * 32)
            Tile(pos, surf, BACKGROUND)

    if layer.name == "BRIDGE":
        for x, y, surf in layer.tiles():
            pos = (x * 32, y * 32)
            Tile(pos, surf, BACKGROUND)

for i in SEA:
    if pygame.sprite.spritecollide(i, BACKGROUND, False):
        SEA.remove(i)

for object in TMX.objects:
    if object.name == "MONSTER":
        MOSPOS.append((object.x, object.y))
        # Monster((object.x, object.y))
    if object.name == "TREE1":
        TREE1.append((object.x, object.y))
    if object.name == "TREE2":
        TREE2.append((object.x, object.y))
    if object.name == "TREE3":
        TREE3.append((object.x, object.y))
    if object.name == "HOUSE":
        HOUSE1.append((object.x, object.y))
    if object.name == "DEC":
        DEC.append((object.x, object.y))
    if object.name == "DEC1":
        DEC1.append((object.x, object.y))
    if object.name == "PLAYER":
        P = Player((object.x, object.y))

MG = pygame.sprite.Group()
TREEG = pygame.sprite.Group()

for i in MOSPOS:
    M = Monster(i)
    MG.add(M)
for i in TREE1:
    T = TREE(i, 0)
    TREEG.add(T)

for i in TREE2:
    T = TREE(i, 1)
    TREEG.add(T)

for i in TREE3:
    T = TREE(i, 2)
    TREEG.add(T)

for i in HOUSE1:
    H = HOUSE(i, 0)
    TREEG.add(H)

for i in DEC:
    D = HOUSE(i, 1)
    TREEG.add(D)

for i in DEC1:
    D = HOUSE(i, 2)
    TREEG.add(D)

count = 0

RUN = True
Fight = False
while RUN:
    clock.tick(FPS)
    round_over = False
    round_over_cooldown = 100
    # QUIT THE LOOP
    # COLLIDE = pygame.sprite.spritecollide(P, BACKGROUND, False)
    screen.fill((32, 214, 199))
    SEA.draw(screen)
    BACKGROUND.draw(screen)
    TREEG.draw(screen)
    MG.draw(screen)
    # HOUSEG.draw(screen)
    screen.blit(P.image, P.rect)
    # for M in MG:
    #     screen.blit(M.image,M.rect)
    pygame.display.update()
    if SCROLL_UP:  # and scrollud<=800:
        # P.UP()

        P.UP()
        if scrollud >= 5:
            for M in MG:
                M.UP()
            for T in TREEG:
                T.UP()
            for i in BACKGROUND:
                i.rect.top += 5

            for i in SEA:
                i.rect.top += 5
            scrollud -= 5
    if SCROLL_DOWN:  # and scrollud>=1:
        P.DOWN()
        if scrollud <= 480:
            for T in TREEG:
                T.DOWN()
            for M in MG:
                M.DOWN()
            for i in BACKGROUND:
                i.rect.top -= 5

            for i in SEA:
                i.rect.top -= 5
            scrollud += 5
    if SCROLL_LEFT:  # and scrollrl<=599:
        P.LEFT()

        if scrollrl >= 5:
            for M in MG:
                M.LEFT()
            for T in TREEG:
                T.LEFT()
            for i in BACKGROUND:
                i.rect.left += 5

            for i in SEA:
                i.rect.left += 5
            scrollrl -= 5
    if SCROLL_RIGHT:  # and scrollrl>=1:
        P.RIGHT()
        if scrollrl <= 575:
            for T in TREEG:
                T.RIGHT()
            for M in MG:
                M.RIGHT()
            for i in BACKGROUND:
                i.rect.left -= 5

            for i in SEA:
                i.rect.left -= 5
            scrollrl += 5

    if pygame.sprite.spritecollide(P, MG, True):
        SCROLL_DOWN = False
        SCROLL_LEFT = False
        SCROLL_RIGHT = False
        SCROLL_UP = False

        # 進入打鬥畫面
        r = random.randint(2, 4)
        count += 1
        Player = Saber(Player_x, Player_y, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATTION_STEPS, count)
        if r == 2:
            Enemy = WIZARD(Enemy_x, Enemy_y, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATTION_STEPS, count)
        elif r == 3:
            Enemy = Hooded(Enemy_x, Enemy_y, True, HOODED_DATA, hooded_sheet, HOODED_ANIMATTION_STEPS, count)
        else:
            Enemy = WizardQ(Enemy_x, Enemy_y, True, WIZZARDQ_DATA, wizardq_sheet, WIZARDQ_ANIMATTION_STEPS, count)

        intro_count = 3
        Fight = True

        while Fight:
            clock.tick(60)

            draw_fightbg()
            draw_text(str("Player blood   " + str(Player.blood)), text_font, BLACK, 40, 50)
            draw_text(str("Attack:    " + str(20 + Player.count *5)), text_font, BLACK, 40, 75)
            draw_text(str("Enmey blood   " + str(Enemy.blood)), text_font, BLACK, 610, 50)
            draw_text(str("Attack:    " + str(10 + 3 * Enemy.count)), text_font, BLACK, 610, 75)
            sum = 0
            # 開局倒數3秒
            if intro_count <= 0:
                Player.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, Enemy)
                Enemy.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, Player)
            else:
                draw_text(str(intro_count), count_font, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                # display count timer(白色)
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

            Enemy.update(Player)
            Player.update(Enemy)

            Enemy.draw(screen)
            Player.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if round_over == False:
                draw_blood_line(Player.blood, 20, 20)
                draw_blood_line(Enemy.blood, 580, 20, count)
                pygame.display.update()
                # pygame.time.delay(1000)

                # 平手則再來一局
                if Player.alive == False and Enemy.alive == False:
                    round_over_time = pygame.time.get_ticks()
                    while (pygame.time.get_ticks() - round_over_time < round_over_cooldown):
                        print("tttt")
                        continue
                    if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
                        draw_text("Tie...", count_font, BLACK, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3)
                        pygame.display.update()
                        round_over = True
                        count -= 1
                    continue
                    # Fight = False
                # 獲勝回到遊戲地圖
                elif Enemy.alive == False and Player.alive == True:
                    round_over_time = pygame.time.get_ticks()
                    while (pygame.time.get_ticks() - round_over_time < round_over_cooldown):
                        print("aaa")
                        continue
                    if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
                        draw_text("You Win!!!!!", count_font, BLACK, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3)
                        draw_text("      Attack +5", text_font, BLACK, SCREEN_WIDTH / 3+45, SCREEN_HEIGHT / 3+75)
                        pygame.display.update()
                        pygame.time.delay(3000)
                        round_over = True
                    # pygame.time.delay(600)
                    if count == 10:
                        #pygame.time.delay(1000)
                        Victory = pygame.image.load("Fight_Scene/Picture/Victory.jpg").convert_alpha()
                        Victory_ = pygame.transform.scale(Victory, (SCREEN_WIDTH, SCREEN_HEIGHT))
                        screen2.blit(Victory_, (0, 0))
                        pygame.display.update()
                        pygame.time.delay(3000)
                        pygame.quit()
                        sys.exit()
                # 失敗 結束遊戲
                elif Player.alive == False and Enemy.alive == True:
                    round_over_time = pygame.time.get_ticks()
                    while (pygame.time.get_ticks() - round_over_time < round_over_cooldown):
                        print("aaa")
                        pass
                    if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
                        print("bbbb")
                        draw_text("You Lose...", count_font, BLACK, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3)
                        pygame.display.update()
                        pygame.time.delay(3000)
                        round_over = True
                        # cooldown  = 20000
                        # while(cooldown != 0):
                        #      cooldown-= 1
                        # pygame.time.delay(3000)
                        Over = pygame.image.load("Fight_Scene/Picture/GameOver.png").convert_alpha()
                        Over_ = pygame.transform.scale(Over, (SCREEN_WIDTH, SCREEN_HEIGHT))

                        screen2.blit(Over_, (0, 0))
                        pygame.display.update()
                        pygame.time.delay(3000)
                        round_over = True
                        pygame.quit()
                        sys.exit()
            else:
                del Enemy
                del Player
                pygame.time.delay(1000)
                Fight = False

                # pygame.time.delay(400)

        # continue
    if pygame.sprite.spritecollide(P, TREEG, False) or pygame.sprite.spritecollide(P, SEA, False):
        if SCROLL_UP:
            P.DOWN()
            for M in MG:
                M.DOWN()
            for T in TREEG:
                T.DOWN()
            for i in BACKGROUND:
                i.rect.top -= 5

            for i in SEA:
                i.rect.top -= 5
            scrollud += 5
        if SCROLL_DOWN:
            P.UP()
            for T in TREEG:
                T.UP()
            for M in MG:
                M.UP()
            for i in BACKGROUND:
                i.rect.top += 5

            for i in SEA:
                i.rect.top += 5
            scrollud -= 5
        if SCROLL_LEFT:
            P.RIGHT()
            for T in TREEG:
                T.RIGHT()
            for M in MG:
                M.RIGHT()
            for i in BACKGROUND:
                i.rect.left -= 5

            for i in SEA:
                i.rect.left -= 5
            scrollrl += 5

        if SCROLL_RIGHT:
            P.LEFT()
            for T in TREEG:
                T.LEFT()
            for M in MG:
                M.LEFT()
            for i in BACKGROUND:
                i.rect.left += 5

            for i in SEA:
                i.rect.left += 5
            scrollrl -= 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # P.UP()
                SCROLL_UP = True
            if event.key == pygame.K_DOWN:
                # P.DOWN()
                SCROLL_DOWN = True
            if event.key == pygame.K_LEFT:
                # P.LEFT()
                SCROLL_LEFT = True
            if event.key == pygame.K_RIGHT:
                # P.RIGHT()
                SCROLL_RIGHT = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                SCROLL_UP = False
            if event.key == pygame.K_DOWN:
                SCROLL_DOWN = False
            if event.key == pygame.K_LEFT:
                SCROLL_LEFT = False
            if event.key == pygame.K_RIGHT:
                SCROLL_RIGHT = False

    pygame.display.update()


pygame.quit()
sys.exit()


# 多增加的東西
# 1.把hooded 跟wizardQ teleport功能加好了  可以調大或小移動幅度  看起來有點強
#    目前是用 10*(random.randint(12, 16))
# 2.把主角攻擊力設定為每回合+5  血量一開始就比較高一點(160)  enemy是(100+20*count)
# 3.enemy攻擊力每回合上升3
# 4.被攻擊會往符合物理的方向後退
