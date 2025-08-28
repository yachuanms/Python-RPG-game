from pytmx.util_pygame import load_pygame
import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        Pic = pygame.image.load("Map/Picture/Saber.png").convert_alpha()
        self.image = pygame.transform.scale(Pic, (64, 80))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.SCREENX = 1000
        self.SCREENY = 800
        self.Flip = False

    

    def LEFT(self):
        if self.rect.left <= 5:
            pass
        else:
            self.rect.left -= 5
            if not self.Flip :
                self.image=pygame.transform.flip(self.image,True,False)
                self.Flip = True
    def RIGHT(self):
        if self.rect.right >= self.SCREENX-5:
            pass
        else:
            self.rect.right += 5
            if  self.Flip :
                self.image=pygame.transform.flip(self.image,True,False)
                self.Flip=False
    def UP(self):
        if self.rect.top <= 5:
            pass
        else:
            self.rect.top -= 5

    def DOWN(self):
        if self.rect.bottom >= self.SCREENY-5:
            pass
        else:
            self.rect.bottom += 5


class HOUSE(pygame.sprite.Sprite):

    def __init__(self, POSITION,PIC):
        img = ["Map/Graphics/Object/HOUSE.png", 
               "Map/Graphics/Object/DEC1.png",
               "Map/Graphics/Object/DEC2.png"]
        
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.image.load(img[PIC])
        self.rect = self.image.get_rect()
        self.rect.center = POSITION
        self.RIGHTpos, self.DOWNpos = self.rect.bottomright

    def DOWN(self):

        self.DOWNpos = self.DOWNpos-5
        #self.rect.topleft=(self.LEFTpos,self.UPpos)
        self.rect.bottomright = (self.RIGHTpos, self.DOWNpos)

    def UP(self):
        self.DOWNpos = self.DOWNpos+5
        self.rect.bottomright = (self.RIGHTpos, self.DOWNpos)

    def LEFT(self):

        self.RIGHTpos = self.RIGHTpos+5

        self.rect.bottomright = (self.RIGHTpos, self.DOWNpos)

    def RIGHT(self):
        self.RIGHTpos = self.RIGHTpos-5

        self.rect.bottomright = (self.RIGHTpos, self.DOWNpos)


class TREE(pygame.sprite.Sprite):

    def __init__(self, POSITION,PIC):
        image = ["Map/Graphics/Object/TREE1.png",
                 "Map/Graphics/Object/TREE2.png",
                 "Map/Graphics/Object/OTHER1.png",
                 "Map/Graphics/Object/HOUSE.png"
                 ]
        
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.image.load(image[PIC])
        self.rect = self.image.get_rect()
        self.rect.center = POSITION
        self.RIGHTpos, self.DOWNpos = self.rect.bottomright

    def DOWN(self):

        self.DOWNpos = self.DOWNpos-5
        #self.rect.topleft=(self.LEFTpos,self.UPpos)
        self.rect.bottomright = (self.RIGHTpos, self.DOWNpos)

    def UP(self):
        self.DOWNpos = self.DOWNpos+5
        self.rect.bottomright = (self.RIGHTpos, self.DOWNpos)

    def LEFT(self):

        self.RIGHTpos = self.RIGHTpos+5

        self.rect.bottomright = (self.RIGHTpos, self.DOWNpos)

    def RIGHT(self):
        self.RIGHTpos = self.RIGHTpos-5

        self.rect.bottomright = (self.RIGHTpos, self.DOWNpos)


class Monster(pygame.sprite.Sprite):

    def __init__(self, POSITION):
        image = ["Map/Picture/magic_1.png", "Map/Picture/magic_2.png", "Map/Picture/magic_3.png", "Map/Picture/magic_4.png"]
        t = random.randint(0, 3)
        pygame.sprite.Sprite.__init__(self)
        Pic = pygame.image.load(image[t]).convert_alpha()
        self.status = t
        self.image = pygame.transform.scale(Pic, (40, 50))
        self.rect = self.image.get_rect()
        self.rect.center = POSITION
        self.RIGHTpos, self.DOWNpos = self.rect.bottomright

    def DOWN(self):

        self.DOWNpos = self.DOWNpos-5
        #self.rect.topleft=(self.LEFTpos,self.UPpos)
        self.rect.bottomright = (self.RIGHTpos, self.DOWNpos)

    def UP(self):
        self.DOWNpos = self.DOWNpos+5
        self.rect.bottomright = (self.RIGHTpos, self.DOWNpos)

    def LEFT(self):

        self.RIGHTpos = self.RIGHTpos+5

        self.rect.bottomright = (self.RIGHTpos, self.DOWNpos)

    def RIGHT(self):
        self.RIGHTpos = self.RIGHTpos-5

        self.rect.bottomright = (self.RIGHTpos, self.DOWNpos)

 

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
       super().__init__(groups)
       self.image =surf
       self.rect=self.image.get_rect(topleft=pos)




 


