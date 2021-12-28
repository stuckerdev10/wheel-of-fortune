#!/usr/bin/env python
# coding: utf-8

# In[286]:


import random #importing packages and initializing values for the game
playerScoreList = [0, 0, 0]
playerScoreDict = {1: 0, 2: 0, 3: 0}
spinValues = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 0, 'Lose a Turn']
finalscoreList = [0, 0, 0]
vowels = {'a', 'e', 'i', 'o', 'u'}


# In[287]:


def has_numbers(string): #this function helps get rid of words with numbers in them
    return any(char.isdigit() for char in string)


# In[288]:


answerFile = open("words-list.txt", 'r')
answerList = answerFile.read().splitlines()#the following lines clean the list of words with symbols in them
answerList[:] = [row for row in answerList if not '.' in row]
answerList[:] = [row for row in answerList if not '-' in row]
answerList[:] = [row for row in answerList if not "'" in row]
answerList[:] = [row for row in answerList if not '&' in row]
answerList[:] = [row for row in answerList if not '/' in row]
answerList[:] = [row for row in answerList if not has_numbers(row)]


for i in range(0, 150):#gets rid of the first initial words with repeating letters
    answerList.remove(answerList[i])
for i in range(0, len(answerList) - 1):#converts everything to lowercase
    answerList[i] = answerList[i].lower()


# In[ ]:


print("-------------------------------------")#begin first round
print("      Wheel of Fortune: Round 1      ")
print("-------------------------------------")
print("Here is your word: ")
chosenAnswer = random.choice(answerList)#choose random word, the break into list
chosenAnswerList = list(chosenAnswer)
playingField = []#set up visable playing field mirroring the chosenAnswerList, filled with  underscores instead of letters
for letter in chosenAnswerList:
    playingField.append('_')
print(playingField)
playersTurn(1)#Game starts with player 1
print("Here are the new standings: ")#displays new standings
print(f"Player 1: {finalscoreList[0]}\n Player 2: {finalscoreList[1]}\n Player 3: {finalscoreList[2]}")

playerScoreDict = {1: 0, 2: 0, 3: 0}

print("-------------------------------------")#begin round 2
print("      Wheel of Fortune: Round 2      ")
print("-------------------------------------")
print("Here is your new word: ")#same answer choosing process as before
chosenAnswer = random.choice(answerList)
chosenAnswerList = list(chosenAnswer)
playingField = []
for letter in chosenAnswerList:
    playingField.append('_')
print(playingField)
lastPlace = min(finalscoreList)#starts with player who is at the lowest value
lastPlaceIndex = finalscoreList.index(lastPlace) + 1
playersTurn(lastPlaceIndex)

firstPlace = max(finalscoreList)#finds the player with the highest final score for the final round
firstPlaceIndex = finalscoreList.index(firstPlace) + 1

print("-------------------------------------")
print("      Wheel of Fortune: Final Round      ")
print("-------------------------------------")
finalRound(firstPlaceIndex)#begin final round


# In[300]:


testList = [2, 4, 6]
print(testList.index(min(testList)))
print(testList)


# In[290]:


def playersTurn(player):#core gameplay of the first to rounds, takes int of player number to start the round
    global playerScoreDict#bring in score an spin values
    global spinValues
    selectedLetters = []#keeps track of letters already selected
    playing = True 
    while playing == True:#loop to keep the round perpetually going
        print(f"Player {player}'s turn: ")
        print(playingField)
        letterCounter = 0#initializes scoring/answer variables before round
        spinScore = random.choice(spinValues)
        totalAttemptScore = 0
        print(f"Your Rolled: {spinScore}")
        if(spinScore) == 0:#if bankrupt
            print("You went Bankrupt! You lost all your money")
            playerScoreDict[player] = 0
            if player + 1 > 3:#moves to next player, resets to player one if already at 3
                player = 1
            else:
                player = player + 1
        elif spinScore == 'Lose a Turn':#if round lost, moves to next player without losing money
            print("You lost this turn!")
            if player + 1 > 3:
                player = 1
            else:
                player = player + 1
        else:
            print(f"Letters already chosen: {selectedLetters}")
            print('Select a letter or answer the puzzle:')
            attempt = input()#player inputs guess or answers puzzle
            if len(attempt) > 1:#if the player chooses to answer
                answerCounter = 0
                attemptWordList = list(attempt)#breaks attempt into list for iteration
                for count, letter in enumerate(attemptWordList):#count if each letter in the attempt matches the answers letter
                    if attemptWordList[count] == chosenAnswerList[count]:
                        answerCounter += 1
                    else:#if there is a mismatch, move to next player
                        print("Incorrect word")
                        if player + 1 > 3:
                            player = 1
                        else:
                            player = player + 1
                if answerCounter == len(chosenAnswerList):#if each letter matches the answer
                    print("Congratulations! You chose the correct word")
                    finalscoreList[player - 1] = playerScoreDict[player]#players score is saved to the final score
                    break
            else:#if they are guessing just a letter
                letterCounter = 0#tracks how many times a letter appears
    
                selecting = True

                while selecting == True:#while loop to let player continue to guess in case of error

                    if attempt in selectedLetters:#if the letter was already chosen, continue to next player
                        print("Letter already chosen")
                        break
                    else:
                        if attempt in vowels:#if letter is in vowels set
                            print('You bought a vowel for $250')
                            if playerScoreDict[player] < 250:#if player can't afford a vowel, cancel and move to next player
                                print("Sorry, you don't have enough money to buy a vowel")
                                if player + 1 > 3:
                                    player = 1
                                else:
                                    player = player + 1
                                break
                            else:#if they can afford, add to selectedLetters and subtrack 250 from their score
                                selectedLetters.append(attempt)
                                playerScoreDict[player] = playerScoreDict[player] - 250
                            if attempt in chosenAnswerList:#if letter exists in the answer
                                print('Correct Choice!')
                            else:
                                print("Incorrect choice")#if its the wrong letter, move on to next player
                                if player + 1 > 3:
                                    player = 1
                                else:
                                    player = player + 1
                                break
                            for count, letter in enumerate(chosenAnswerList):#keeps track of how many times letter appears,
                                if chosenAnswerList[count] == attempt:
                                    letterCounter += 1
                                    playingField[count] = attempt#replaces underscores on playing field with the letter
                            totalAttemptScore = letterCounter * spinScore#calculates total score of attempt
                            playerScoreDict[player] = playerScoreDict[player] + totalAttemptScore
                            print(f"This letter appeared {letterCounter} times for a score of {totalAttemptScore}")
                            print(f"Your new score is {playerScoreDict[player]}")
                            print(playingField)
                        else:#if the guess is a constonant
                            print('this is a constonant')
                            if attempt in chosenAnswerList:#if correct move on
                                selectedLetters.append(attempt)
                                print('Correct Choice!')
                            else:
                                selectedLetters.append(attempt)#if incorrect move to next player
                                print('Incorrect choice')
                                if player + 1 > 3:
                                    player = 1
                                else:
                                    player = player + 1
                                break
                            for count, letter in enumerate(chosenAnswerList):#same scoring scheme as before
                                if chosenAnswerList[count] == attempt:
                                    letterCounter += 1
                                    playingField[count] = attempt
                            totalAttemptScore = letterCounter * spinScore
                            playerScoreDict[player] = playerScoreDict[player] + totalAttemptScore
                            print(f"This letter appeared {letterCounter} times for a score of {totalAttemptScore}")
                            print(playingField)
                    print(f"Scores: {playerScoreDict}")
    


# In[278]:


def attemptWord(player, word, playing):
    global chosenAnswerList
    answerCounter = 0
    attemptWordList = list(word)
    for count, letter in enumerate(attemptWordList):
        if attemptWordList[count] == chosenAnswerList[count]:
            answerCounter += 1
        else:
            print("Incorrect word")
            break
    if answerCounter == len(chosenAnswerList):
        print("Congratulations! You chose the correct word")
    


# In[279]:


def attemptChar(player, attempt, spin):
    global chosenAnswerList
    global playerScoreDict
    global vowels
    global selectedLetters
    
    letterCounter = 0
    
    selecting = True
    
    while selecting == True:
       
        if attempt in selectedLetters:
            print("Letter already chosen")
            break
        else:
            print(f"Chosen letters: {selectedLetters}")
            if attempt in vowels:
                print('You bought a vowel for $250')
                if playerScoreDict[player] < 250:
                    print("Sorry, you don't have enough money to buy a vowel")
                    chosenAnswerList.pop()
                    break
                else:
                    selectedLetters.append(attempt)
                    playerScoreDict[player] = playerScoreDict[player] - 250
                if attempt in chosenAnswerList:
                    print('Correct Choice!')
                else:
                    print("Incorrect choice")
                    break
                for count, letter in enumerate(chosenAnswerList):
                    if chosenAnswerList[count] == attempt:
                        letterCounter += 1
                        playingField[count] = attempt
                totalAttemptScore = letterCounter * spin
                playerScoreDict[player] = playerScoreDict[player] + totalAttemptScore
                print(f"This letter appeared {letterCounter} times for a score of {totalAttemptScore}")
                print(f"Your new score is {playerScoreDict[player]}")
                print(playingField)
            else:
                print('this is a constonant')
                if attempt in chosenAnswerList:
                    print('Correct Choice!')
                else:
                    print('Incorrect choice')
                    break
                for count, letter in enumerate(chosenAnswerList):
                    if chosenAnswerList[count] == attempt:
                        letterCounter += 1
                        playingField[count] = attempt
                totalAttemptScore = letterCounter * spinScore
                playerScoreDict[player] = playerScoreDict[player] + totalAttemptScore
                print(f"This letter appeared {letterCounter} times for a score of {totalAttemptScore}")
                print(playingField)


# In[280]:


def finalRound(player):#final round of the game, player with max score plays
    global vowels
    print(f"Congratulations player {player}! You have made it to the final round")
    print("This next round is worth $1,000,000.")
    print("Here is the word: ")
    chosenAnswer = random.choice(answerList)#choose new word
    chosenAnswerList = list(chosenAnswer)
    playingField = []
    for letter in chosenAnswerList:
        playingField.append('_')
    print(playingField)#display word to player
    print("Here is the word after the default clues (r s t l n e)")
    defaultClues = ['r', 's', 't', 'l', 'n' 'e']
    for count, letter in enumerate(chosenAnswerList):#this loop checks each letter in chosenAnswerList against the default clues
        for letter in defaultClues:
            if letter == chosenAnswerList[count]:
                playingField[count] = letter#replaces the underscore with the letter if they match
                break
    print(playingField)
    guessSelections = []
    for i in range(1, 4):#player chooses 3 constonants, which gets put in guessSelections List
        print(f"Select constonant {i}")
        attempt = input()
        if len(attempt) > 1 or attempt in vowels:#checks to see if constonant in proper format
            while len(attempt) > 1 or attempt in vowels:
                print("invalid format, please enter again")
                attempt = input()
        guessSelections.append(attempt)
    print("Now choose a vowel: ")
    attempt = input()#user must choose a vowel
    if attempt not in vowels:#checks to see if letter is actually a vowel
        while attempt not in vowels:
            print("Not a vowel, please try again: ")
            attempt = input()
    guessSelections.append(attempt)
    print(f"Here are your selections: {guessSelections}")
    print("Here is the new playing field: ")
    for count, letter in enumerate(chosenAnswerList):#runs through letters against chosenAnswerList
        for letter in guessSelections:
            if letter == chosenAnswerList[count]:
                playingField[count] = letter
                break
    print(playingField)
    print("For $1,000,000 dollars, what is the word?")
    attempt = input()#player inputs guess
    answerCounter = 0
    attemptWordList = list(attempt)
    for count, letter in enumerate(attemptWordList):#runs through same word guessing progress as previous rounds
        if attemptWordList[count] == chosenAnswerList[count]:
            answerCounter += 1
        else:
            print("Incorrect word")
            break
    if answerCounter == len(chosenAnswerList):
        print("Congratulations! You chose the correct word")


# In[ ]:





# In[ ]:




