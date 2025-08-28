import pygame
import random


class Hooded:
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps, count):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip  # 在右邊的腳色一開始就是反的要先翻過來
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = (
            0  # 0:idle 1:blink 2:hop 3:run 4:duck 5:jump 6:teleport 7:die 8:attack
        )
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attack_type = 0
        self.attack_cooldown = 0  # 攻擊冷卻時間
        self.attacking = False
        self.hit = False
        self.count = count
        self.blood = 80 + count * 20
        self.alive = True

    def draw(self, surface):
        # 讓人物翻轉
        img = pygame.transform.flip(self.image, self.flip, False)  # (x, y)方向 後兩個參數
        # pygame.draw.rect(surface, (255, 255, 255), self.rect)
        # 用offset調整位置
        surface.blit(
            img,
            (
                self.rect.x - (self.offset[0] * self.image_scale),
                self.rect.y - (self.offset[1] * self.image_scale),
            ),
        )

    # load 整張的圖片 切割他
    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(
                    x * self.size, y * self.size, self.size, self.size
                )
                temp_img = pygame.transform.scale(
                    temp_img,
                    ((self.size * self.image_scale, self.size * self.image_scale)),
                )
                # temp_img.set_colorkey((0,0,0)) #去背
                temp_img_list.append(temp_img)
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, surface, target):
        SPEED = 15
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        cooldown = 60
        if (
            self.attacking == False
            and self.attack_cooldown == 0
            and self.running == False
            and target.alive == True
        ):
            self.action = random.randint(3, 8)
            while cooldown > 0:
                cooldown -= 1
            if self.action == 3:
                self.running == True
                dx = -SPEED
            elif self.action == 5 or self.action == 4:
                self.jump == True
                self.vel_y = -25
            elif self.action == 6:
                self.attack_type = 1
                self.attack(surface, target)
                self.attacking = True
                if self.rect.x > target.rect.x:
                    self.rect.x -= 10 * (random.randint(10, 15))
                else:
                    self.rect.x += 10 * (random.randint(10, 15))
            elif self.action == 8:
                self.attack_type = 2
                self.attack(surface, target)
                self.attacking = True
        elif self.hit == True:
            self.rect.x += 5

        if self.rect.x == target.rect.x:
            self.rect.x += 5

        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        if self.rect.bottom + dy > SCREEN_HEIGHT - 110:
            self.vel_y = 0
            self.jump = False
            dy = SCREEN_HEIGHT - 110 - self.rect.bottom

        # ensure players face each other
        if target.alive == True:
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

        # apply atack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.rect.x += dx
        self.rect.y += dy

    def update(self, target):
        if self.blood <= 0:
            self.blood = 0
            self.update_action(7)  # death
            self.alive = False
            self.rect.y = 500
        elif self.hit == True:
            self.update_action(1)  # hit
            if self.rect.x > target.rect.x:
                self.rect.x += 6
            else:
                self.rect.x -= 6
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(6)  # attack1
            elif self.attack_type == 2:
                self.update_action(8)  # attack2
        elif self.jump == True:
            self.update_action(5)  # jump
        # check what action the player is performing
        elif self.running == True:
            self.update_action(3)  # run
        else:
            self.update_action(0)  # idle

        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed to update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1  # 換動作
            self.update_time = pygame.time.get_ticks()
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # check if the player is dead the end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[7]) - 1  # 死了就停在最後一個畫面
            else:
                self.frame_index = 0
                # check if an attack was executed
                if self.action == 6 or self.action == 8:
                    self.attacking = False
                    self.attack_cooldown = 20
                # check if damage was taken
                if self.action == 1:
                    self.hit = False
                    # check if the player was in the middle of the attack, the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attack_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y,
                2 * self.rect.width,
                self.rect.height,
            )
            if attack_rect.colliderect(target.rect):
                target.blood -= 10 + 3 * self.count
                target.hit = True
            # pygame.draw.rect(surface, (0, 255, 0), attack_rect)
        # self.attacking = False
