import pygame
import time
from pygame.locals import *
import random

hero_nums = 0
enermy_nums = 0


class BasePlane(object):
    def __init__(self, screen, x, y, image):
        self.x = x
        self.y = y
        self.screen = screen
        self.image = pygame.image.load(image)
        self.is_hit = False  # 此标志用来表示飞机是否被击中了
        self.bullets = []

    def test(self, bullets):
        for bullet in bullets:
            if self.x < bullet.x < self.x + self.image.get_width() and \
                                    self.y < bullet.y < self.y + self.image.get_height():
                self.is_hit = True

                #  检测子弹碰撞
        for item in self.bullets:
            for bullet in bullets:
                if item.x < bullet.x < item.x + item.image.get_width() and \
                                        item.y < bullet.y < item.y + item.image.get_height():
                    item.is_hit = True
                    bullet.is_hit = True


class HeroPlane(BasePlane):
    def __init__(self, screen, image="./feiji/hero1.png"):
        super().__init__(screen, 210, 700, image)

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            if bullet.is_hit:
                self.bullets.remove(bullet)
            else:
                bullet.display()
                bullet.move()
            if bullet.y <= 0:
                self.bullets.remove(bullet)

    def move_left(self):
        if not (self.x < 0):
            self.x -= 5

    def move_right(self):
        if (self.x + self.image.get_width()) < self.screen.get_width():
            self.x += 5

    def fire(self):
        self.bullets.append(Bullet(self.screen, self.x + 40, self.y - 20))


class EnermyPlane(BasePlane):
    def __init__(self, screen):
        self.direciton = "right"
        self.bullets = []
        super().__init__(screen, 215, 0, "./feiji/enemy0.png")

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        for item in self.bullets:
            if item.is_hit:
                self.bullets.remove(item)
            else:
                item.display()
                item.move()
            if item.y > 852:
                self.bullets.remove(item)

    def move(self):
        if self.direciton == "right":
            self.x += 3
        elif self.direciton == "left":
            self.x -= 3
        if self.x > 430:
            self.direciton = "left"
        elif self.x <= 0:
            self.direciton = "right"

    def fire(self):
        num = random.randint(0, 100)
        if num == 50 or num == 25:
            self.bullets.append(EnermyBullet(self.screen, self.x + 25, self.y + 20))


class BaseBullet(object):
    def __init__(self, screen, x, y, image):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.is_hit = False

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def test(self, bullets):
        for bullet in bullets:
            if bullet.x > self.x and bullet.x < self.x + 100 and bullet.y > self.y and bullet.y < self.y + 124:
                self.is_hit = True


class Bullet(BaseBullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, "./feiji/bullet.png")

    def move(self):
        self.y -= 5


class EnermyBullet(BaseBullet):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y, "./feiji/bullet1.png")

    def move(self):
        self.y += 3

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


# 键盘控制飞机的坐标
def key_control(hero):
    for event in pygame.event.get():
        if event.type == QUIT:
            print("exit")
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                hero.move_left()
                print("left")
            elif event.key == K_d or event.key == K_RIGHT:
                hero.move_right()
                print("right")
            elif event.key == K_SPACE:
                hero.fire()
                print("space")


def main():
    global is_hit
    global nums
    screen = pygame.display.set_mode((480, 852), 0, 32)
    background = pygame.image.load("./feiji/background.png")
    # 创建飞机
    hero = HeroPlane(screen)
    enermy_plane = EnermyPlane(screen)
    while True:
        global hero_nums
        global enermy_nums
        # 显示背景
        screen.blit(background, (0, 0))
        # 显示我方飞机
        hero.display()
        # 测试是否被子弹击中
        hero.test(enermy_plane.bullets)
        if hero.is_hit:
            hero_nums += 1
            if hero_nums == 10:
                hero.image = pygame.image.load("./feiji/hero_blowup_n1.png")
            elif hero_nums == 20:
                hero.image = pygame.image.load("./feiji/hero_blowup_n2.png")
            elif hero_nums == 30:
                hero.image = pygame.image.load("./feiji/hero_blowup_n3.png")
            elif hero_nums == 40:
                hero.image = pygame.image.load("./feiji/hero_blowup_n4.png")
            elif hero_nums > 50:
                break
        # 显示敌飞机
        enermy_plane.display()
        enermy_plane.test(hero.bullets)
        if enermy_plane.is_hit:
            enermy_nums += 1
            if enermy_nums == 10:
                enermy_plane.image = pygame.image.load("./feiji/enemy0_down1.png")
            elif enermy_nums == 20:
                enermy_plane.image = pygame.image.load("./feiji/enemy0_down2.png")
            elif enermy_nums == 30:
                enermy_plane.image = pygame.image.load("./feiji/enemy0_down3.png")
            elif enermy_nums == 40:
                enermy_plane.image = pygame.image.load("./feiji/enemy0_down4.png")
            elif enermy_nums > 50:
                enermy_plane = EnermyPlane(screen)
                enermy_nums = 0
        else:
            enermy_plane.move()
            enermy_plane.fire()

        # 控制飞机左右
        key_control(hero)
        # 刷新屏幕
        pygame.display.update()
        # 程序休眠0.01秒
        time.sleep(0.01)


if __name__ == "__main__":
    main()
