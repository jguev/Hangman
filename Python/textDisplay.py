import pygame
import time
import random

#pygame.init()
display_width = 1000
display_height = 700
gameDisplay = pygame.display.set_mode((display_width,display_height))

class textBox:
    def __init__(self, color = [0,0,0], text = '', size = 40, font = 'arial', center = True, xpixel = display_width/2, ypixel = display_height/2):
        self.color = color
        self.text = text
        self.font = font
        self.size = size
        self.center = center
        #self.display_width = 800
        self.xpixel = xpixel # self.xpixel = self displaywidth
        self.ypixel = ypixel
        self.fit = False
        self.fonts = pygame.font.SysFont(font, size)
        self.textSurface = self.fonts.render(text, True, color)
        self.textRect = self.textSurface.get_rect()
        
        if self.center == True:
            self.textRect.center = (xpixel, ypixel)
        else:
            self.textRect = (xpixel, ypixel)

    def displayBlit(self):
        self.textSurface = self.fonts.render(self.text, True, self.color)
        if self.center == True:
            self.textRect.center = (self.xpixel,self.ypixel)
        else:
            self.textRect = (self.xpixel, self.ypixel)
        gameDisplay.blit(self.textSurface, self.textRect)

    def fitToScreen(self): #Only use when not center = True
        if self.fonts.size(self.text)[0] > display_width and self.fit == False:
            self.xpixel = self.xpixel + self.fonts.size(self.text)[0]/2
            self.ypixel = self.ypixel + self.fonts.size(self.text)[1]/2
        if self.fonts.size(self.text)[0] > display_width:
            self.size -= 1
            self.fonts = pygame.font.SysFont(self.font, self.size)
            self.fit = True
            self.fitToScreen()
        else:
            if self.fit == True:
                self.xpixel -= self.fonts.size(self.text)[0]/2
                self.ypixel -= self.fonts.size(self.text)[1]/2
                self.fit = False
            return