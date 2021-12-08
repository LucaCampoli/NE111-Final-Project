# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 21:03:48 2021

@author:  LucaC, EthanC, RianE, LinuxH
Initials: LC,    EC,     RE,    LH
"""

import random, pygame, sys, words

# Setting up the pygame window size -LC
pygame.init()
wl = 600
wh = 1000
wlc = wh/2
whc = wl/2
windowSurface = pygame.display.set_mode((wh, wl), 0, 32)
pygame.display.set_caption('Hangman')
# Setting up the pygame colors -LC
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
windowSurface.fill(WHITE)
# Setting up the font -LC
basicFont = pygame.font.SysFont(None, 24)

def getRandomWord(wordList):
    """
    (list) -> str
   
    Given a list as input, return a random entry in the list.
   
    >>> getRandomWord(["Hello World", "Python", "Test"])
    "Python"
    >>> getRandomWord(["Hello World", "Python", "Test"])
    "Hello World"
    >>> getRandomWord(["Hello World", "Python", "Test"])
    "Test"
    -EC
    """
    wordIndex = random.randint(0, len(wordList) - 1)
    return list(wordList)[wordIndex]

def spinWheel():
    """
    (None) -> str
   
    Given no input, returns a random string from the list.
   
    >>> spinWheel()
    "750"
    >>> spinWheel()
    "Bankrupt"
    >>> spinWheel()
    "900"
    -RE
    """
    l=['500','550','600','650','700','750','800','850','900','5000','Bankrupt']
    return random.choice(l)

def displayBoard(missedLetters, correctLetters, secretWord):
    """
    (str, str, str) -> tuple
   
    Given a 3-entry tuple as input, return a 2-entry tuple.
    This function
   
    If the input argument is invalid, return None.
   
    >>> displayBoard("mn", "te", "test")
    ("t _ e t", "m, n")
    >>> displayBoard("mnp", "lheo", "hello_world")
    ("h e l l o   _ o _ l _", "m, n, p")
    -LC
    """
    blanks = '_' * len(secretWord)
    missed = ''
    board = ''
    for i in range(len(missedLetters)):
        # Add a space in between each missed letter -LC
        missed += missedLetters[i]
        if i != len(missedLetters) - 1:
            missed += ", "
    for i in range(len(secretWord)):
        # Replace blanks with correctly guessed letters -LC
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
    for i in range(len(blanks)):
        # Add a space in between each entry on the board -LC
        board += blanks[i]
        if i != len(blanks) - 1:
            board += " "
    return (board, missed)
   
def guessedWord(guess, correctLetters, missedLetters, stage, message, message2, scoreToBeAdded, score):
    if guess in secretWord:
       
        for i in secretWord:
           
            if i == guess:
               
                score += scoreToBeAdded
       
        correctLetters += guess
        # Check if the player has won -LH
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            message = 'Yes! The secret word is "' + secretWord + '"! You have won!'
            message2 = "Press 'Y' to Play Again"
            return True, correctLetters, missedLetters, stage, message, message2, score, False
    else:
        missedLetters += guess
        # Check if player has guessed too many times and lost -LH
        if len(missedLetters) == 6:
            displayBoard(missedLetters, correctLetters, secretWord)
            message = 'You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"'
            message2 = "Press 'Y' to Play Again"
            return True, correctLetters, missedLetters, stage + 1, message, message2, score, True
        # If the player guessed incorrectly but hasn't lost -LH
        message = "That is incorrect"
        message2 = "Press any key to Spin the Wheel"
        return False, correctLetters, missedLetters, stage + 1, message, message2, score, False
    
    # If the player guessed correctly but hasn't won -LH
    message = "Good Job!"
    message2 = "Press any key to Spin the Wheel"
    return False, correctLetters, missedLetters, stage, message, message2, score, False
    """
    (str) -> str
   
    Given a letter as input, return the same letter.
    This function makes sure the player entered a single letter and not something else.
    If entering an invalid character, the function loops until a valid character is entered
       
    >>> getGuess("a")
    "a"
    >>> getGuess("A")
    "a"
    -LH
    """

def playAgain():
    """
    (None) -> bool
   
    Given no input, returns a boolean value.
    # This function returns True if the player wants to play again when asked; otherwise, it returns False.
   
    >>> playAgain()
        >>> "y"
    True
    >>> playAgain()
        >>> "Y"
    True
    >>> playAgain()
        >>> "n"
    False
    -RE
    """
    displayMessage('Do you want to play again? (y or n)')
    if event.key == pygame.K_y:
        return True
    return False

def pygameTextRenderer(renderedtext, offsetH, offsetV):
    """
    (str, int, int) -> None
   
    Given a 3-entry tuple, prints text to the window.
    This function will print the first parameter, and will offset the text horizontally by offsetH units, and vertically by offsetV units
    -LC
    """
    text = basicFont.render(renderedtext, True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx + offsetH
    textRect.centery = windowSurface.get_rect().centery + offsetV
   
    # Drawing the text's background rectangle onto the surface -LC
    pygame.draw.rect(windowSurface, RED, (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))
   
    # Drawing the text onto the surface -LC
    windowSurface.blit(text, textRect)

def displayMessage(renderedtext):
    """
    (str) -> None
   
    Given a string, prints text to the window with a set offset.
    This function will print the given message, which will be centered and near the bottom of the screen
    -LC
    """
    text = basicFont.render(renderedtext, True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery + 150
   
    # Drawing the text's background rectangle onto the surface -LC
    pygame.draw.rect(windowSurface, RED, (textRect.left - 10, textRect.top - 10, textRect.width + 20, textRect.height + 20))
   
    # Drawing the text onto the surface -LC
    windowSurface.blit(text, textRect)

def displayLowerMessage(renderedtext):
    """
    (str) -> None
   
    Given a string, prints text to the window with a set offset.
    This function will print the given message, which will be centered and below the first message
    This function is called so two messages can appear simultaneously
    -LC
    """
    text = basicFont.render(renderedtext, True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery + 250
   
    # Drawing the text's background rectangle onto the surface -LC
    pygame.draw.rect(windowSurface, RED, (textRect.left - 10, textRect.top - 10, textRect.width + 20, textRect.height + 20))
   
    # Drawing the text onto the surface -LC
    windowSurface.blit(text, textRect)

def displayRound(roundnum):
    """
    (int) -> None
   
    Given an integer, prints text to the window with a set offset.
    This function will print: "Round" + the given round number, which will located at the top-left of the screen
    -LC
    """
    text = basicFont.render(("Round " + str(roundnum)), True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx - 300
    textRect.centery = windowSurface.get_rect().centery - 250
   
    # Drawing the text's background rectangle onto the surface -LC
    pygame.draw.rect(windowSurface, RED, (textRect.left - 10, textRect.top - 10, textRect.width + 20, textRect.height + 20))
   
    # Drawing the text onto the surface -LC
    windowSurface.blit(text, textRect)

def displayScore(score):
    """
    (int) -> None
   
    Given an integer, prints text to the window with a set offset.
    This function will print: "Score:" + the current score, which will located at the top-right of the screen
    -LC
    """
    text = basicFont.render(("Score: " + str(score)), True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx + 300
    textRect.centery = windowSurface.get_rect().centery - 250
   
    # Drawing the text's background rectangle onto the surface -LC
    pygame.draw.rect(windowSurface, RED, (textRect.left - 10, textRect.top - 10, textRect.width + 20, textRect.height + 20))
   
    # Drawing the text onto the surface -LC
    windowSurface.blit(text, textRect)

def displayNaught(stage=0):
    """
    (int) -> None
   
    Given an integer, prints the hangman visual to the window with a set offset.
    This function will print different stages of the hangman visual depending on the number of incorrect guesses
    -LC
    """
    pygame.draw.polygon(windowSurface, GREEN, ((wlc-250, whc+75), (wlc-200, whc+50), (wlc-200, whc+50), (wlc-200, whc-150), (wlc-100, whc-150), (wlc-100, whc-125), (wlc-110, whc-125), (wlc-110, whc-140), (wlc-160, whc-140), (wlc-180, whc-120), (wlc-180, whc+50), (wlc-125, whc+75)))
    if stage >= 1:
        pygame.draw.circle(windowSurface, GREEN, (wlc-105, whc-100), 25)        
    if stage >= 2:
        pygame.draw.polygon(windowSurface, GREEN, ((wlc-110, whc-100), (wlc-100, whc-100), (wlc-100, whc), (wlc-110, whc)))
    if stage >= 3:
        pygame.draw.polygon(windowSurface, GREEN, ((wlc-110, whc-15), (wlc-135, whc+10), (wlc-125, whc+20), (wlc-105, whc)))
    if stage >= 4:
        pygame.draw.polygon(windowSurface, GREEN, ((wlc-100, whc-15), (wlc-75, whc+10), (wlc-85, whc+20), (wlc-105, whc)))
    if stage >= 5:
        pygame.draw.polygon(windowSurface, GREEN, ((wlc-110, whc-65), (wlc-135, whc-40), (wlc-125, whc-30), (wlc-105, whc-50)))
    if stage >= 6:
        pygame.draw.polygon(windowSurface, GREEN, ((wlc-100, whc-65), (wlc-75, whc-40), (wlc-85, whc-30), (wlc-105, whc-50)))

# Setting all the game constants -LH
missedLetters = ''
correctLetters = ' '
wordList = words.word_list
secretWord = getRandomWord(wordList)
gameIsDone = False
guessingWord = False
stage = 0
roundNum = 1
score = 0
scoreToBeAdded = 0

message = "Welcome To Wheel Of Fortune!"
message2 = "Press any key to Spin the Wheel"

# Outlining every possible key that could be pressed -LH
keys = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_a,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z,pygame.K_QUESTION]

#Gameplay loop -LH
while True:
    #Printing the round number, score, hangman visual, both messages, the board state, and the missed letters -LC
    windowSurface.fill(WHITE)
    displayRound(roundNum)
    displayScore(score)
    displayNaught(stage)
    displayMessage(message)
    displayLowerMessage(message2)
    pygameTextRenderer((displayBoard(missedLetters, correctLetters, secretWord)[0]), 200, -100)
    pygameTextRenderer((displayBoard(missedLetters, correctLetters, secretWord)[1]), 200, 0)

    # Getting a pixel array of the surface -LC
    pixArray = pygame.PixelArray(windowSurface)
    pixArray[480][380] = BLACK
    del pixArray
   
    # Drawing the window onto the screen -LC
    pygame.display.update()
   
    # Run the game loop -LH
    for event in pygame.event.get():
        # If the player pressed the "X" button of the window -LH
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # If a key was pressed -LH
        if event.type == pygame.KEYDOWN:
           
            if gameIsDone:
                if playAgain():
                    # Incrementing the round number while setting all other variables to their default values -LH
                    roundNum += 1
                    stage = 0
                    windowSurface.fill(WHITE)
                    displayNaught(stage)
                    missedLetters = ''
                    correctLetters = ' '
                   
                    gameIsDone = False
                    guessingWord = False
                    secretWord = getRandomWord(wordList)
                   
                    scoreToBeAdded = 0
                   
                    message = "Welcome to round " + str(roundNum)
                    message2 = "Press any key to Spin the Wheel"
                   
                    break
                # If the player wants to exit the game: -LH
                else:
                    # Break the game loop -LH
                    break
            # If guessing a letter: -LH
            if guessingWord:
                # If the key pressed is a valid key and has not been guessed before -LH
                if event.key in keys and pygame.key.name(event.key) not in correctLetters and pygame.key.name(event.key) not in missedLetters:
                    guess = pygame.key.name(event.key)
                    
                    gameIsDone, correctLetters, missedLetters, stage, message, message2, score, restart = guessedWord(guess, correctLetters, missedLetters, stage, message, message2, scoreToBeAdded, score)
                    
                    if restart:
                        roundNum = 0
                        score = 0
                        scoreToBeAdded = 0
                    
                    guessingWord = False
            # If not guessing a letter: -LH
            else:
                wheelResult = spinWheel()
               
                if wheelResult == 'Bankrupt':
                   
                    score = 0
                    message = "You went Bankrupt"
                   
                else:
                    scoreToBeAdded = int(wheelResult)

                    message = "You landed on " + wheelResult
                    message2 = "Guess a letter!"
                guessingWord = True