from playing import hangman
from textDisplay import textBox
from buttonDisplay import button
from colors import *
import pygame
import time
import random
import json
import os
from collections import Counter
 
background= pygame.image.load('space.png')
rules = pygame.image.load('rules.png')
rules = pygame.transform.scale(rules,(750,491))
humanStanding = pygame.image.load('h_start.png')
humanStanding = pygame.transform.scale(humanStanding,(608, 400))
rope = pygame.image.load('rope.png')
rope = pygame.transform.scale(rope, (450,620))
speechBub = pygame.image.load('bubble_hang.png')
speechBub = pygame.transform.scale(speechBub, (405, 90))
welcomeBub = pygame.image.load ('bubble_welcome.png')
welcomeBub = pygame.transform.scale(welcomeBub, (680, 140))

class hangers:
    def __init__(self):
        pygame.init()                               #Initializing display and creating the pixel size for for the window
        self.display_width = 1000
        self.display_height = 700
        self.CENTERED_XBUTTON = (self.display_width/2) - 100 #only works for button width 100
        self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption("Lets Hang Out!")   #Naming the window
        self.clock = pygame.time.Clock()
        self.menu = True

    def hard(self):                         #OPTIONS FUNCTIONS
        self.tries = 2
        self.category_menu()
    def medium(self):
        self.tries = 3
        self.category_menu()
    def easy(self):
        self.tries = 5
        self.category_menu()   
    def animals(self):
        self.cat = 'animals'
        self.start()
    def sports(self):
        self.cat = 'sports'
        self.start()
    def school(self):
        self.cat = 'school'
        self.start()
    def random(self):                        #END OF OPTIONS FUNCTIONS
        self.cat = 'random'
        self.start()

    def pauseFunction(self, m):
        mup = m
        pauseM = textBox( text = 'PAUSE', size = 55, center = True, ypixel = 230, font= 'comicsansms')
        pygame.draw.rect(self.gameDisplay, BLACK, [self.display_width/3,self.display_height/4,335,380])
        pygame.draw.rect(self.gameDisplay, WHITE, [(self.display_width/3) + 1,(self.display_height/4) + 1,332,377])

        pauseM.displayBlit()
        button(30, "Continue",self.CENTERED_XBUTTON-25,(self.display_height/2)-50,250,50,GREEN,BRIGHT_GREEN,self.unpause, mup)
        button(30, "Main Menu",self.CENTERED_XBUTTON-25,(self.display_height/2)+25,250,50,GRAY,BRIGHT_GRAY,self.game, mup)
        button(30, "Quit Game",self.CENTERED_XBUTTON-25,(self.display_height/2)+100,250,50,RED,BRIGHT_RED,self.quitGame, mup)
        pygame.display.flip()
        mup = False
        return mup

    def quitGame(self):
        pygame.quit()
        quit()

    def unpause(self):
        self.pause = False

    def game_intro(self):                   #First screen that runs/ showing the name of the game and the game presentation
        intro = True
        part1 = True
        part2 = False
        part2a = False
        gameName = textBox(list(BLACK), 'Hangman', 100)
        presentation = textBox(list(WHITE), 'Presented by Element', 58, 'comicsansms')
        #test = textBox(text = 'THIS IS A TEXT TEST', size = 200, center = True , ypixel = 200) #TESTING TEXT TO FIT TO SCREEN

        while intro:
            self.gameDisplay.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if part1:
                #gameName = textBox(gameName.color, 'Hangman', 100)     CHANGED RENDER TO textBox.displayBlit() FUNCTION SO WE DO NOT HAVE TO KEEP REINITIALIZING TEXTBOX ON LOOP
                gameName.displayBlit()
                #test.fitToScreen()                                         #TEXT FIT TO SCREEN
                #test.displayBlit()
                pygame.display.update()
                self.clock.tick(100)
                gameName.color[0] += 1
                gameName.color[1] += 1
                gameName.color[2] += 1

                if gameName.color[0] == WHITE[0]:
                    part1 = False
                    part2 = True

            elif part2:
                #presentation = textBox(presentation.color, 'Presented by group 2', 60, 'comicsansms')
                presentation.displayBlit()
                pygame.display.update()
                self.clock.tick(150)
                if presentation.color[0] > 0 and part2a == False:
                    presentation.color[0] -= 1
                    presentation.color[1] -= 1
                    presentation.color[2] -= 1
                    if presentation.color[0] == 0:
                        part2a = True
                elif part2a:
                    presentation.color[0] += 1
                    presentation.color[1] += 1
                    presentation.color[2] += 1
                    if presentation.color[0] == 255:
                        part2 = False
                        intro = False

    def saveExists(self): #Asks user if they want to load save, or continue a new game
        filesize = os.path.getsize("save.txt")
        if filesize == 0:
            self.difficulty_menu()

        mup = False
        self.menu = True

        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mup = True
                else:
                    mup = False

            pauseM = textBox( text = 'Save File Exists', size = 28, center = True, ypixel = 230, font= 'comicsansms')
            pygame.draw.rect(self.gameDisplay, BLACK, [self.display_width/3,self.display_height/4,335,380])
            pygame.draw.rect(self.gameDisplay, WHITE, [(self.display_width/3) + 1,(self.display_height/4) + 1,332,377])

            pauseM.displayBlit()
            button(30, "Load Save",self.CENTERED_XBUTTON-25,(self.display_height/2)-40,250,50,GREEN,BRIGHT_GREEN,self.SetLoad, mup)
            button(30, "New Game",self.CENTERED_XBUTTON-25,(self.display_height/2)+40,250,50,RED,BRIGHT_RED,self.difficulty_menu, mup)
            button(30, "Back",self.CENTERED_XBUTTON-25,(self.display_height/2)+120,250,50,GRAY,BRIGHT_GRAY,self.game, mup)
            #pygame.display.flip()
            pygame.display.update()
            self.clock.tick(60)

    def SetLoad(self): #Tells playing that save needs to be loaded
        self.SGame = 1
        self.start()
        

    def game(self):                         #This is where the game loop begins
        mup = False
        self.menu = True
        self.pause = False
        title = textBox( WHITE, text = 'Hangman', size = 95, center = True, ypixel = 70, font= 'comicsansms')
        self.SGame = 0
        self.tries = 0
        self.cat   = ""

        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mup = True
                else:
                    mup = False

                if event.type == pygame.KEYUP:
                    if event.key == 27:
                        self.pause = True
                if self.pause == True:
                    mup = self.pauseFunction(mup)
            if self.pause == True:
                continue

            pygame.draw.rect(self.gameDisplay, BLUE, [0,0,self.display_width,150])
            pygame.draw.rect(self.gameDisplay, GRAY, [0,150,self.display_width,self.display_height])
            title.displayBlit()
            button(60, "RULES",(self.display_width/2)-200,(self.display_height/2)+40,400,100,[13,91,157],BRIGHT_YELLOW,self.rules_menu, mup)
            button(60, "QUIT",(self.display_width/2)-200,(self.display_height/2)+190,400,100,[13,91,157],BRIGHT_RED,self.quitGame, mup)
            button(60, "START",(self.display_width/2)-200,(self.display_height/2)-110,400,100,[13,91,157],BRIGHT_GREEN,self.saveExists, mup)
            pygame.display.update()
            self.clock.tick(60)

    def rules_menu(self):
        self.menu = True
        mup = False
        title = textBox(WHITE, text = 'Rules', size = 50, center = True, ypixel = 70, font= 'comicsansms')
        #rules1 = textBox(WHITE, text = 'Welcome to Hangman, by Element! Hangman is a game where you are given tries to guess a secret word!', size = 20, center = True, ypixel = 190, font= 'comicsansms')
        #rules2 = textBox(WHITE, text = 'SETTING UP', size = 30, center = True, ypixel = 225, font= 'comicsansms')
        #rules3 = textBox(WHITE, text = 'In this game, you select from three categories to guess words from, or an optional fourth category that will draw from all of the other three!', size = 14, center = True, ypixel = 250, font= 'comicsansms')
        #rules4 = textBox(WHITE, text = 'Before selecting a category, you will need to select your difficulty. Difficulty will determine both how many tries you have to guess incorrectly on a', size = 14, center = True, ypixel = 275, font= 'comicsansms')
        #rules5 = textBox(WHITE, text = 'letter in the mystery word, and also how many points you will get from the word. You will also get more points the less wrong letters you guess.', size = 14, center = True, ypixel = 300, font= 'comicsansms')
        #rules6 = textBox(WHITE, text = 'PLAYING', size = 28, center = True, ypixel = 325, font= 'comicsansms')
        #rules7 = textBox(WHITE, text = 'If you correctly guess your word, you will be shown your total score, and allowed to either quit now, or continue to guess more words for more points!', size = 14, center = True, ypixel = 350, font= 'comicsansms')
        #rules8 = textBox(WHITE, text = 'You are allowed to continue until you get a word wrong. If you incorrectly guess your word, you will be taken to the highscore screen.', size = 14, center = True, ypixel = 375, font= 'comicsansms')
        #rules9 = textBox(WHITE, text = 'Here you will be shown the previous highscores, and will display your score if it was high enough! Guess lots of words to get a highscores!', size = 14, center = True, ypixel = 400, font= 'comicsansms')
        #rules10 = textBox(WHITE, text = 'Also, at any point in the game, pressing escape will pause, and allow you to quit the game.', size = 14, center = True, ypixel = 425, font= 'comicsansms')
        #rules11 = textBox(WHITE, text = 'Thats Hangman, have fun!', size = 20, center = True, ypixel = 450, font= 'comicsansms')
        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mup = True
                else:
                    mup = False
                if event.type == pygame.KEYUP:
                    if event.key == 27:
                        self.pause = True
                if self.pause == True:
                    pauseM = textBox( text = 'PAUSE', size = 55, center = True, ypixel = 230, font= 'comicsansms')
                    pygame.draw.rect(self.gameDisplay, BLACK, [self.display_width/3,self.display_height/4,335,380])
                    pygame.draw.rect(self.gameDisplay, WHITE, [(self.display_width/3) + 1,(self.display_height/4) + 1,332,377])
                    pauseM.displayBlit()
                    button(60, "Continue",self.CENTERED_XBUTTON-25,(self.display_height/2)-50,250,100,GREEN,BRIGHT_GREEN,self.unpause, mup)
                    button(60, "Quit",self.CENTERED_XBUTTON-25,(self.display_height/2)+100,250,100,RED,BRIGHT_RED,self.quitGame, mup)
                    mup = False
                    pygame.display.flip()
            if self.pause == True:
                continue

            pygame.draw.rect(self.gameDisplay, BLUE, [0,0,800,150])
            pygame.draw.rect(self.gameDisplay, GRAY, [0,150,800,450])
            title.displayBlit()
            #rules1.displayBlit()
            #rules2.displayBlit()
            #rules3.displayBlit()
            #rules4.displayBlit()
            #rules5.displayBlit()
            #rules6.displayBlit()
            #rules7.displayBlit()
            #rules8.displayBlit()
            #rules9.displayBlit()
            #rules10.displayBlit()
            #rules11.displayBlit()
            self.gameDisplay.blit(rules,(30,240))
            self.gameDisplay.blit(welcomeBub,(270,170))
            self.gameDisplay.blit(humanStanding,((self.display_width - 635), (self.display_height/2)-90)) 
            button(35, "back", 2, 2, 100, 50, GRAY,BRIGHT_GRAY,self.game, mup)
            pygame.display.update()
            self.clock.tick(60)
            
    def difficulty_menu(self):
        self.menu = True
        mup = False
        title = textBox(WHITE, text = 'Choose Difficulty Level', size = 50, center = True, ypixel = 70, font= 'comicsansms')

        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mup = True
                else:
                    mup = False

                if event.type == pygame.KEYUP:
                    if event.key == 27:
                        self.pause = True
                if self.pause == True:
                    mup = self.pauseFunction(mup)
            if self.pause == True:
                continue

            pygame.draw.rect(self.gameDisplay, BLUE, [0,0,self.display_width,150])
            pygame.draw.rect(self.gameDisplay, GRAY, [0,150,self.display_width,self.display_height])
            title.displayBlit()
            button(55, "Hard",self.CENTERED_XBUTTON+225,(self.display_height/2)-20,200,200,[13,91,157],BRIGHT_GRAY,self.hard, mup)
            button(50, "Medium",self.CENTERED_XBUTTON,(self.display_height/2)-20,200,200,[13,91,157],BRIGHT_GRAY,self.medium, mup)
            button(55, "Easy",self.CENTERED_XBUTTON-225,(self.display_height/2)-20,200,200,[13,91,157],BRIGHT_GRAY,self.easy, mup)
            button(35, "back", 2, 2, 100, 50, GRAY,BRIGHT_GRAY,self.game, mup)
            pygame.display.update()
            self.clock.tick(60)

    def category_menu(self):
        self.menu = True
        mup = False
        title = textBox(WHITE, text = 'Choose Category', size = 50, center = True, ypixel = 70, font= 'comicsansms')
        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mup = True
                else:
                    mup = False
    
                if event.type == pygame.KEYUP:
                    if event.key == 27:
                        self.pause = True
                if self.pause == True:
                    mup = self.pauseFunction(mup)
            if self.pause == True:
                continue

            pygame.draw.rect(self.gameDisplay, BLUE, [0,0,800,150])
            pygame.draw.rect(self.gameDisplay, GRAY, [0,150,800,450])
            title.displayBlit()
            # these buttons are 30 pixels apart and centered
            button(45, "Animals",(self.display_width/2)-445,(self.display_height/2)-20,200, 200,[13,91,157],BRIGHT_GRAY, self.animals, mup)
            button(45, "Sports",(self.display_width/2)-215, (self.display_height/2)-20,200,200,[13,91,157],BRIGHT_GRAY, self.sports, mup)
            button(45, "School",(self.display_width/2)+15, (self.display_height/2)-20,200,200,[13,91,157],BRIGHT_GRAY, self.school, mup)
            button(45, "Random",(self.display_width/2)+245, (self.display_height/2)-20,200,200,[13,91,157],BRIGHT_GRAY, self.random, mup)
            button(35, "back", 2, 2, 100, 50, GRAY,BRIGHT_GRAY,self.difficulty_menu, mup)
            pygame.display.update()
            self.clock.tick(60)

    def start(self):                        #The actual starts here and it's using the file playing
        #if(self.SGame != 1):
        self.play = hangman(self.tries, self.cat, self.SGame)
        #else:
        #self.play = hangman(self.maxFails, self.catN, self.SGame)
        self.play.game()
        
        if self.play.mainMenuB == True:
            self.game()

        while self.play.win == True:
            mup = False
            self.gameDisplay.fill(WHITE)
            self.gameDisplay.blit(background, (0,0))
            self.gameDisplay.blit(rope,(435,0))
            self.gameDisplay.blit(humanStanding,((self.display_width - 635), (self.display_height/2)-260)) 
            self.gameDisplay.blit(speechBub,(580,60))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mup = True
                else:
                    mup = False

                if event.type == pygame.KEYUP:
                    if event.key == 27:
                        self.pause = True
                if self.pause == True:
                    mup = self.pauseFunction(mup)
            if self.pause == True:
                continue
            
            score = textBox(text = 'Score: ' + str(self.play.score), xpixel=0, ypixel=0, center = False)
            score.displayBlit()
            button(45, "Done", self.CENTERED_XBUTTON, 370, 200, 100, RED, BRIGHT_RED, self.highscore, mup)
            button(45, "Continue", self.CENTERED_XBUTTON, 170, 200, 100, GREEN, BRIGHT_GREEN, self.play.replay, mup)

            if self.play.mainMenuB == True:
                self.game()

            pygame.display.update()
            self.clock.tick(60)

        self.highscore()

    def highscore(self):                    #Always returns back to game function. get someone else to make the highscore screen to work?
        filename = 'highscores.json'
        n = 0               #SOMETHING TO DO WITH THE PIXEL OF THE HIGHSCORE

        def save(filename, dict):
            with open(filename, 'w') as f:
                json.dump(dict, f, indent = 2)
        
        def load(filename):
            with open(filename) as f:
                data = json.load(f)
            return data

        def newScore(num):
            data = load(filename)
            nameList = []
            scoreList = []

            for key, value in data.items():
                nameList.append(value['name'])
                scoreList.append(value['score'])

            for score in scoreList:
                if num > score:
                    name = self.inputName()
                    newIndex = scoreList.index(score)
                    nameList.insert(newIndex, name)
                    scoreList.insert(newIndex, num)
                    nameList.pop()
                    scoreList.pop()

                    for i in range(len(nameList)):
                        data[str(i+1)] = {}
                        data[str(i+1)]['name'] = nameList[i]
                        data[str(i+1)]['score'] = scoreList[i]

                    break


            save(filename, data)
        

        newScore(self.play.score)
        
        self.menu = False
        highscores = load(filename)
        names = []
        scores = []
    
        highscoreD = textBox(text = 'HIGHSCORE', color = WHITE, ypixel = 100, size = 100)

        for i in range(len(highscores)):
            names.append(textBox(text = highscores[str(i+1)]['name'], xpixel = 250, center = False, ypixel = 200 + (n * 75)))
            scores.append(textBox(text = str(highscores[str(i+1)]['score']), xpixel = 650, center = False, ypixel = 200 + (n * 75)))
            n += 1

        while self.menu != True:
            mup = False
            self.gameDisplay.fill(SPACE_BLUE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mup = True
                else:
                    mup = False

            highscoreD.displayBlit()
            for name in names:
                name.displayBlit()
            for score in scores:
                score.displayBlit()
            button(30, 'Return', 898, 648, 100, 50, GRAY, BRIGHT_GRAY, self.game, mup)
            pygame.display.update()
            self.clock.tick(60)
    
    
    def inputName(self):
        self.menu = True
        mup = False
        name = ''
        cont = False
        title = textBox(WHITE, text = 'CONGRATULATIONS NEW HIGH SCORE', size = 40, center = True, ypixel = 70, font= 'comicsansms')
        prompt = textBox(WHITE, text = 'Please enter your name', size = 40, center = True, ypixel = 200, font= 'comicsansms')
        while self.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mup = True
                else:
                    mup = False
                
                if len(name) != 0 and event.type == pygame.KEYDOWN and event.key == 13:     #Enter key(event.key = 13)
                    cont = True
                if len(name) != 0 and event.type == pygame.KEYDOWN and event.key == 8:     #Backspace key
                    name = name[0:len(name)-1]
                elif event.type == pygame.KEYDOWN and event.key != 13:                        #input a letter that is not the enter key
                    name += event.unicode
                    name = name.upper()
                else:
                    pass

                if event.type == pygame.KEYUP:
                    if event.key == 27:
                        self.pause = True
                if self.pause == True:
                    pauseM = textBox( text = 'PAUSE', size = 55, center = True, ypixel = 230, font= 'comicsansms')
                    pygame.draw.rect(self.gameDisplay, BLACK, [self.display_width/3,self.display_height/4,335,380])
                    pygame.draw.rect(self.gameDisplay, WHITE, [(self.display_width/3) + 1,(self.display_height/4) + 1,332,377])
                    pauseM.displayBlit()
                    button(60, "Continue",self.CENTERED_XBUTTON-25,(self.display_height/2)-50,250,100,GREEN,BRIGHT_GREEN,self.unpause, mup)
                    button(80, "Quit",self.CENTERED_XBUTTON-25,(self.display_height/2)+100,250,100,RED,BRIGHT_RED,pygame.quit, mup)
                    mup = False
                    pygame.display.flip()
            if self.pause == True:
                continue
            
            pygame.draw.rect(self.gameDisplay, BLUE, [0,0,self.display_width,self.display_height])
            pygame.draw.rect(self.gameDisplay, GRAY, [0,150,self.display_width,self.display_height])
            title.displayBlit()
            prompt.displayBlit()
            nameD = textBox(text = name)
            nameD.displayBlit()
            pygame.display.update()
            self.clock.tick(60)

            if cont == True:
                return name

meh = hangers()
meh.game_intro()
meh.game()
pygame.quit()
quit()