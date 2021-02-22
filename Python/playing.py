from textDisplay import textBox
from colors import *
from buttonDisplay import button
import pygame
import time
import random
from random import seed
from random import randint

pygame.init()
display_width = 1000
display_height = 700
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Let's hang!")   #Naming the window

#declaring images outside of loop so they only load once
humanHanging = pygame.image.load('h_hang.png')
humanHanging = pygame.transform.scale(humanHanging, (150,170))
rope = pygame.image.load('rope.png')
rope = pygame.transform.scale(rope, (450,620))
monster = pygame.image.load('monster_hang.png')
monster = pygame.transform.scale(monster,(152, 155))

#variables for monster's movement
deltaX = 0
deltaY = 50
humanX = 620
humanY = 65
monsterPos = []
monsterSpeed = 2

background= pygame.image.load("space.png")
clock = pygame.time.Clock()


class hangman:
    def __init__(self, maxFails, catName, SGame):
        self.CENTERED_XBUTTON = (display_width/2) - 100

        self.maxFails= self.max = maxFails
        self.catN = catName
        if(SGame != 1):
            self.greeting()
            self.createGuess()
        self.tried = False
        self.failedLetters = []
        self.win = True
        self.score = 0
        self.pause = False
        self.mainMenuB = False
        if(SGame == 1):
            self.LoadSave()
        if self.max == 2:
            self.point = 750
        elif self.max == 3:
            self.point = 400
        elif self.max == 5:
            self.point = 200


    def mainMenu(self):
        self.mainMenuB = True
        self.pause = False

    def unpause(self):
        self.pause = False

    def replay(self):
        self.maxFails = self.max
        self.greeting()
        self.createGuess()
        self.tried = False
        self.failedLetters = []
        self.win = True
        if self.max == 2:
            self.point = 750
        elif self.max == 3:
            self.point = 400
        elif self.max == 5:
            self.point = 200
        self.game()

    def greeting(self):                   # this shall be replaced by the categories input and the reading of the file that selects the word
        hint_dictionary = {}
        catF = open(self.catN + ".txt", "r")
        for line in catF:
            separator = line.split(":")
            word = separator[0] 
            hint = separator[1]
            bye = len(hint)-1           # this is the new line we need to get rid of
            hint = hint[0:bye]          # grabs everything but omits last character
            hint_dictionary[word] = hint      #dictionary format
        wordGUI = random.choice(list(hint_dictionary.keys()))
        hintGUI = hint_dictionary[wordGUI]
        print(wordGUI)                  # WORD
        print(hintGUI)                  # HINT
        self.guess = self.word = wordGUI.upper()
        self.print_hint = hintGUI
    
    def createGuess(self):
        for i in self.word:
            if i != ' ':
                self.guess = self.guess.replace(i, '_')

    def correct(self):
        guess2 = "".join(self.guess)
        if guess2 == self.word:
            return True
        else:
            return False

    def hints(self):        #New hint function that runs when the hint button is pressed.
        self.showHints = True       
        #This variable is originally false, making the displayBlit() 
        #not run in the display function, once the button is pressed 
        #the displayBlit() will now run on a loop along with all other display texts
       
    def display(self):
        if self.maxFails < self.max:
            failedLetters2 = "".join(self.failedLetters)
            fld = textBox(text = failedLetters2, ypixel= 100, xpixel = 90, color = RED)
            fld.displayBlit()
        guess2 = ''                                                 #FOR LOOP GUESS INTO GUESS2 AND ADD SPACES IN BETWEEN SO WHEN PASSING ON TO GUESSD THERE WOULD BE SPACES
        for letter in self.guess:
            guess2 += str(letter) + " "
        guessD = textBox(text = guess2, ypixel= 470, color = BLACK, size= 80)
        guessD.fitToScreen()
        guessD.displayBlit()
        tries = "Tries remaining: " + str(self.maxFails)
        triesD = textBox(text = tries, xpixel= 10, ypixel= 00, center = False)
        triesD.displayBlit()
        self.triedD.displayBlit()

        category = "Category: " + str(self.catN.capitalize())
        categoryD = textBox(text = category,xpixel = 660, ypixel = 0, center = False)
        categoryD.displayBlit()

        hints = "Hint: " + str(self.print_hint)
        hintsD = textBox(text = hints, xpixel = 10, ypixel = 200, center = False) # Hint display
        if self.win != True and self.maxFails != 0 and self.showHints == True: # erases the hint off the display for winning || added new condition where if the button is pressed the displayBlit() would be true on a loop
            hintsD.displayBlit()


    def quitGame(self):
        pygame.quit()
        quit()

    def SaveGame(self):
        saveF = open("save.txt", "w")
        saveF.write(str(self.max) + "\n") #write all relevant data to save, to be loaded into same game state as is
        saveF.write(self.catN + "\n")
        saveF.write(str(self.score) + "\n")
        saveF.write(self.word + "\n")
        for i in self.guess:
            saveF.write(i)
        saveF.write("\n")
        for i in self.failedLetters:
            saveF.write(i)
        saveF.write("\n")
        saveF.write(str(self.maxFails) + "\n")
        saveF.write(self.print_hint)
        saveF.close()
        self.quitGame()
     
    def LoadSave(self): #loads the saved file
        saveF = open("save.txt", "r")
        self.max = int(saveF.readline().rstrip('\n')) #rstrip removes endline char
        self.catN = saveF.readline().rstrip('\n')
        self.score = int(saveF.readline().rstrip('\n'))
        self.word = saveF.readline().rstrip('\n')
        self.guess = str(saveF.readline().rstrip('\n'))
        self.failedLetters = str(saveF.readline().rstrip('\n'))
        self.maxFails = int(saveF.readline().rstrip('\n'))
        self.print_hint = saveF.readline().rstrip('\n')

        saveF.close()
        self.SGame = 0
        open("save.txt", "w").close()  #erases save file

    def game(self):
        self.win = False
        self.showHints = False
        mup = False
        finish = False
        cont = False
        self.guess = list(self.guess)
        self.failedLetters = list(self.failedLetters)
        self.guessLetter = ''
        self.triedD = textBox(text = "You've already tried that", xpixel = display_width/3, ypixel = 150, center = True, color = list(WHITE), size = 30)

        while self.win != True and self.maxFails != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mup = True
                else:
                    mup = False
                
                if len(self.guessLetter) != 0 and event.type == pygame.KEYDOWN and event.key == 13:     #Enter key(event.key = 13)
                    cont = True

                if event.type == pygame.KEYDOWN and event.key != 13:                                    #input a letter that is not the enter key
                    self.guessLetter = event.unicode
                    self.guessLetter = self.guessLetter.upper()
                else:
                    pass

                if event.type == pygame.KEYUP:
                    if event.key == 27:
                        self.pause = True
                if self.pause == True:
                    pauseM = textBox( text = 'PAUSE', size = 55, center = True, ypixel = 230, font= 'comicsansms')
                    pygame.draw.rect(gameDisplay, BLACK, [display_width/3,display_height/4,335,428])
                    pygame.draw.rect(gameDisplay, WHITE, [(display_width/3) + 1,(display_height/4) + 1,332,425])
                    pauseM.displayBlit()
                    button(30, "Continue", self.CENTERED_XBUTTON - 25,(display_height/2)-50,250,50,GREEN,BRIGHT_GREEN,self.unpause, mup)
                    button(30, "Main Menu", self.CENTERED_XBUTTON - 25,(display_height/2)+25,250,50,GRAY,BRIGHT_GRAY,self.mainMenu, mup)
                    button(30, "Save and Quit",self.CENTERED_XBUTTON-25,(display_height/2)+100,250,50,YELLOW,BRIGHT_YELLOW,self.SaveGame, mup)
                    button(30, "Quit Game", self.CENTERED_XBUTTON - 25,(display_height/2)+175,250,50,RED,BRIGHT_RED,self.quitGame, mup)
                    pygame.display.flip()
            if self.pause == True:
                continue

            if self.mainMenuB == True:
                return

            global monsterPos, humanX, humanY
            
            for m in monsterPos:
                m[0] = m[0] - monsterSpeed #moves left
                if m[0] < 0:
                    monsterPos = [x for x in monsterPos if not (x[0] == m[0] and x[1] == m[1])]
            if random.randint(0,200) == 0: #frequency between new monster spawnings
                monsterPos.append([random.randint(900, 1000), 0]) #where monster is spawned


            gameDisplay.fill(BRIGHT_GRAY)
            gameDisplay.blit(background, (0,0))
            gameDisplay.blit(rope,(305,0))
            gameDisplay.blit(humanHanging,(humanX, humanY))
            
            for m in monsterPos:
                monsterX, monsterY = m[0], m[1]
                gameDisplay.blit(monster,((monsterX - 10), (monsterY + 560))) #placement of monster

            guessLetterD = textBox(text = self.guessLetter)
            guessLetterD.displayBlit()

            self.failed = True
            self.tried = False

            #if self.triedD.color[1] < 255:   #When guessing a letter that's already guess it makes the message fade from red to white
                #self.triedD.color[1] += 4
                #self.triedD.color[2] += 4
                
            if self.triedD.color == [255,255,255]:
                self.triedD.color = [34,56,74]
        
            if cont == True:
                cont = False
                self.triedD.color = [34,56,74]    #When you guess another word it makes the triedD text space blue

                if self.guessLetter in self.failedLetters + self.guess:   #Check if the letter has already been in use
                    self.tried = True
                    self.guessLetter = ''
                    self.triedD.color = [255, 3, 3]   #Creates a red colored text when you repeat a letter
                    continue
                
                for index in range(len(self.word)):      #Gets the letter input, checks it with the word string, and then shoves it into the guess list checks if letter failed
                    if self.guessLetter == self.word[index]:
                        self.guess[index] = self.guessLetter
                        self.failed = False

                if self.failed == True:      #Put guessed letter in a list of failed letters
                    self.failedLetters.append(self.guessLetter)
                    self.maxFails -= 1
                    humanX += deltaX
                    humanY += deltaY
                    gameDisplay.blit(humanHanging,(humanX, (humanY)))
                    # lower the human
                
                self.guessLetter = ''
                self.win = self.correct()

            if self.showHints == False:      #When the hint button gets pressed the button disappears
                button(35, 
                "Hint",self.CENTERED_XBUTTON+450,(display_height/3)-180,100,70,[
                    13,91,157],BRIGHT_GRAY,self.hints,mup)   
                    #Hint button, the location is not centered at the moment because I was working with old display pixels

            self.display()
            pygame.display.update()
            clock.tick(60)

        if self.win == True:     #Finish texts
            humanX = 620 #resets hanging human position on top of rope
            humanY = 65
            self.failedLetters = [] #erases trace of incorrect letters
            finishD = textBox(text = 'Congratulations you won!', ypixel = 200) 
        else:
            finishD = textBox(text = "You Lose", ypixel = 200)
            humanX = 620 #resets hanging human position on top of rope
            humanY = 65
        continueD = textBox(text = 'Press any key to continue')
        
        while finish != True:   #print the finish message before continuing
            #gameDisplay.fill(WHITE)
            gameDisplay.blit(background, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    finish = True
            
            self.display()
            finishD.displayBlit()
            continueD.displayBlit()
            pygame.display.update()
            clock.tick(60)

        self.score += self.maxFails * self.point


if __name__ == "__main__":
    game = hangman(3, "animals", 0)
    game.game()