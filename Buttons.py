import pygame as PG

class Button():

    def __init__(self, x, y, Image, SingleClick):
        self.image = Image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = SingleClick
    def draw(self, surface):
        Action = False
        #Gather Mouse Information
        POS = PG.mouse.get_pos()

        #Conditions
        if self.rect.collidepoint(POS):
            if PG.mouse.get_pressed()[0] == 1 and self.clicked == False:
                Action = True
                if self.single_click:
                    self.clicked = True

        if PG.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #Draw Buttons onto the Screen
        surface.blit(self.image, self.rect)
        return Action