# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 09:54:20 2021

@author: lucac
"""

import random, pygame, sys, time, words

pygame.init()

wh = 800
wl = 600
whc = wh/2
wlc = wl/2
windowSurface = pygame.display.set_mode((wh, wl), 0, 32)
pygame.display.set_caption('Hangman')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# 66, 135, 245
BLUE = (0, 0, 255)

windowSurface.fill(WHITE)
#pygame.draw.polygon(windowSurface, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

# Set up the fonts.
basicFont = pygame.font.SysFont(None, 24)
smallFont = pygame.font.SysFont(None, 24)

# Constants
NUMBER_OF_ROUNDS = 3
HELP_KEYWORD = "?"

def getRandomWord(wordList):
    """
    (list) -> str
    
    Given a list as input, return a random entry in the list.
    
    If the input argument is invalid, return None.
    
    >>> getRandomWord(["Hello World", "Python", "Test"])
    "Python"
    >>> getRandomWord(["Hello World", "Python", "Test"])
    "Hello World"
    >>> getRandomWord(["Hello World", "Python", "Test"])
    "Test"
    """
    # This function returns a random string from the passed list of strings.
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]

def spinWheel():
    l=['500','550','600','650','700','750','800','850','900','5000','Bankrupt','Lose a turn','Free Play']
    return random.choice(l)

def displayBoard(missedLetters, correctLetters, secretWord):
    # Method has been heavily edited to return the board and missed letters as strings instead of printing them separately
    # TODO could just print missed letters instead of passing them through this method
    """
    (tuple) -> tuple
    
    Given a 3-entry tuple as input, return a 2-entry tuple.
    This function 
    
    If the input argument is invalid, return None.
    
    >>> displayBoard("mn", "te", "test")
    ("t _ e t ", "m n ")
    >>> displayBoard("mnp", "lheo", "hello_world")
    ("h e l l o   _ o _ l _ ", "m n p ")
    """
    # TODO go back and make sure these are correct (with spacing and stuff)
    blanks = '_' * len(secretWord)
    missed = ''
    board = ''

    for i in range(len(missedLetters)):
        # Add a space in between each missed letter
        # TODO maybe add a comma between each letter
        missed += missedLetters[i]
        if i != len(missedLetters) - 1:
            missed += ", "

    for i in range(len(secretWord)):
        # Replace blanks with correctly guessed letters
        # TODO if guess in secretWord[i]
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for i in range(len(blanks)):
        # Add a space in between each entry on the board
        board += blanks[i]
        if i != len(blanks) - 1:
            board += " "
    return (board, missed)

#def getGuess(alreadyGuessed)
    
def guessedWord(guess, correctLetters, missedLetters):
    
    if guess in secretWord:
        correctLetters += guess

        # Check if the player has won.
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            displayMessage('Yes! The secret word is "' + secretWord + '"! You have won!')
            #TODO instance of sleep
            #TODO not effective until next loop, so this sleep doesn't work
            return True, correctLetters, missedLetters
    else:
        missedLetters += guess
        # Check if player has guessed too many times and lost.
        if len(missedLetters) == 6:
            displayBoard(missedLetters, correctLetters, secretWord)
            displayMessage('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
            #TODO instance of sleep
            time.sleep(1)
            pygame.draw.rect(windowSurface, WHITE, (windowSurface.get_rect().centerx, windowSurface.get_rect().centery + 200, 180, 80))
            return True, correctLetters, missedLetters
        
    return False, correctLetters, missedLetters
    """
    (str) -> str
    
    Given a letter as input, return the same letter.
    This function makes sure the player entered a single letter and not something else.
    If entering an invalid character, the function loops until a valid character is entered
        
    >>> getGuess("a")
    "a"
    >>> getGuess("A")
    "a"
    """

    while True:
        displayMessage('Guess a letter.')
        guess = input()
        guess = guess.lower()
        #if len(guess) != 1:
            #displayMessage('Please enter a single letter.')
        if guess in alreadyGuessed:
            displayMessage('You have already guessed that letter. Choose again.')
            #TODO First instance of sleep
            time.sleep(1)
            pygame.draw.rect(windowSurface, WHITE, (windowSurface.get_rect().centerx, windowSurface.get_rect().centery + 200, 180, 80))
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            displayMessage('Please enter a LETTER.')
            time.sleep(1)
            pygame.draw.rect(windowSurface, WHITE, (windowSurface.get_rect().centerx, windowSurface.get_rect().centery + 200, 180, 80))
        else:
            return guess

def playAgain():
    """
    (None) -> bool
    
    Given no input, returns a boolean value.
    # This function returns True if the player wants to play again when asked; otherwise, it returns False.
    
    >>> playAgain()
        >>> "yes"
    True
    >>> playAgain()
        >>> "Y"
    True
    >>> playAgain()
        >>> "no"
    False
    """

    displayMessage('Do you want to play again? (y or n)')
    if event.key == pygame.K_y:
        return True
    return False
    #TODO return input().lower().startswith('y')

def pygameTextRenderer(renderedtext, offsetH, offsetV):
    text = basicFont.render(renderedtext, True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx + offsetH
    textRect.centery = windowSurface.get_rect().centery + offsetV
    
    # Draw the text's background rectangle onto the surface
    pygame.draw.rect(windowSurface, RED, (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))
    
    # Draw the text onto the surface
    windowSurface.blit(text, textRect)

def displayMessage(renderedtext):
    text = smallFont.render(renderedtext, True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx
    textRect.centery = windowSurface.get_rect().centery + 200
    
    # Draw the text's background rectangle onto the surface
    pygame.draw.rect(windowSurface, RED, (textRect.left - 10, textRect.top - 10, textRect.width + 20, textRect.height + 20))
    
    # Draw the text onto the surface
    windowSurface.blit(text, textRect)

def displayRound(roundnum):
    text = smallFont.render(("Round " + str(roundnum)), True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx - 300
    textRect.centery = windowSurface.get_rect().centery - 250
    
    # Draw the text's background rectangle onto the surface
    pygame.draw.rect(windowSurface, RED, (textRect.left - 10, textRect.top - 10, textRect.width + 20, textRect.height + 20))
    
    # Draw the text onto the surface
    windowSurface.blit(text, textRect)

def displayScore(score):
    
    text = smallFont.render(("Score: " + str(score)), True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx + 300
    textRect.centery = windowSurface.get_rect().centery - 250
    
    # Draw the text's background rectangle onto the surface
    pygame.draw.rect(windowSurface, RED, (textRect.left - 10, textRect.top - 10, textRect.width + 20, textRect.height + 20))
    
    # Draw the text onto the surface
    windowSurface.blit(text, textRect)

def displayNaught():
    pygame.draw.polygon(windowSurface, GREEN, ((whc-100, wlc+75), (whc-50, wlc+50), (whc-50, wlc+50), (whc-50, wlc-150), (whc+50, wlc-150), (whc+50, wlc-125), (whc+40, wlc-125), (whc+40, wlc-140), (whc-10, wlc-140), (whc-30, wlc-120), (whc-30, wlc+50), (whc+25, wlc+75),))

missedLetters = ''
correctLetters = ' '

wordList = words.word_list
secretWord = getRandomWord(wordList)

gameIsDone = False
guessingWord = False
roundNum = 1
score = 0
scoreToBeAdded = 0

message = ""

keys = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_a,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z,pygame.K_QUESTION]


while True:
    windowSurface.fill(WHITE)
    displayRound(roundNum)
    displayScore(score)
    displayNaught()
    displayMessage(message)
    pygameTextRenderer((displayBoard(missedLetters, correctLetters, secretWord)[0]), 200, -100)
    pygameTextRenderer((displayBoard(missedLetters, correctLetters, secretWord)[1]), 200, 0)
    
    # Get a pixel array of the surface.
    pixArray = pygame.PixelArray(windowSurface)
    pixArray[480][380] = BLACK
    del pixArray
    
    # Draw the window onto the screen.
    pygame.display.update()
    
    # Run the game loop.
    # TODO check pygame animated to check how this function works
    # TODO this can't be moved somewhere else. For some reason, moving this past the imput causes an error
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            
            if gameIsDone:

                if playAgain():
                    windowSurface.fill(WHITE)
                    pygame.draw.polygon(windowSurface, GREEN, ((whc-100, wlc+75), (whc-50, wlc+50), (whc-50, wlc+50), (whc-50, wlc-150), (whc+50, wlc-150), (whc+50, wlc-125), (whc+40, wlc-125), (whc+40, wlc-140), (whc-10, wlc-140), (whc-30, wlc-120), (whc-30, wlc+50), (whc+25, wlc+75),))
                    missedLetters = ''
                    correctLetters = ' '
                    gameIsDone = False
                    secretWord = getRandomWord(wordList)
                    roundNum += 1
                    score = 0
                else:
                    break
            
            if guessingWord:
                if event.key in keys and pygame.key.name(event.key) not in correctLetters and pygame.key.name(event.key) not in missedLetters:
                    
                    # TODO print("You have pressed a letter")
                    # TODO print(pygame.key.name(event.key))
                    guess = pygame.key.name(event.key)
                    
                    gameIsDone, correctLetters, missedLetters = guessedWord(guess, correctLetters, missedLetters)
                    guessingWord = False
                    
                    message = "Press any key to Spin Wheel"
                
                    # Ask the player if they want to play again (but only if the game is done).
            
            else:           
                wheelResult = spinWheel()
                
                if wheelResult == 'Bankrupt':
                    
                    score = 0
                elif wheelResult == 'Lose a turn':
                    
                    print("Uhhhh")
                elif wheelResult == 'Free Play':
                    
                    #You will not lose a life if you land here
                    print("Uhhh x2")
                else:
                    scoreToBeAdded = int(wheelResult)
                
                message = "You landed on " + wheelResult
                guessingWord = True