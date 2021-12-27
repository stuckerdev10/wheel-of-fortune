#!/usr/bin/env python
# coding: utf-8

# In[261]:


import random #importing packages and initializing values for the game
playerScoreList = [0, 0, 0]
playerScoreDict = {1: 0, 2: 0, 3: 0}
spinValues = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 0, 'Lose a Turn']
finalscoreList = [0, 0, 0]
vowels = {'a', 'e', 'i', 'o', 'u'}


# In[262]:


def has_numbers(string): #this function helps get rid of words with numbers in them
    return any(char.isdigit() for char in string)


# In[263]:


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


# In[276]:


print("-------------------------------------")
print("      Wheel of Fortune: Round 1      ")
print("-------------------------------------")
print("Here is your word: ")
chosenAnswer = random.choice(answerList)
chosenAnswerList = list(chosenAnswer)
playingField = []
for letter in chosenAnswerList:
    playingField.append('_')
print(playingField)
playersTurn(1)
print("Here are the new standings: ")
print(f"Player 1: {finalscoreList[0]}\n Player 2: {finalscoreList[1]}\n Player 3: {finalscoreList[2]}")

print("-------------------------------------")
print("      Wheel of Fortune: Round 2      ")
print("-------------------------------------")
print("Here is your new word: ")
chosenAnswer = random.choice(answerList)
chosenAnswerList = list(chosenAnswer)
playingField = []
for letter in chosenAnswerList:
    playingField.append('_')
print(playingField)
lastPlace = min(finalscoreList)
lastPlaceIndex = finalscoreList.index(lastPlace)
playersTurn(lastPlaceIndex)

firstPlace = max(finalScoreList)
firstPlaceIndex = finalScoreList.index()

print("-------------------------------------")
print("      Wheel of Fortune: Final Round      ")
print("-------------------------------------")
finalRound(firstPlaceIndex)


# In[275]:


def playersTurn(player):
    global playerScoreDict
    global spinValues
    selectedLetters = []
    playing = True
    while playing == True:
        print(f"Player {player}'s turn: ")
        letterCounter = 0
        spinScore = random.choice(spinValues)
        totalAttemptScore = 0
        print(f"Your Rolled: {spinScore}")
        if(spinScore) == 0:
            print("You went Bankrupt! You lost all your money")
            playerScoreDict[player] = 0
            if player + 1 > 3:
                player = 1
            else:
                player = player + 1
        elif spinScore == 'Lose a Turn':
            print("You lost this turn!")
            if player + 1 > 3:
                player = 1
            else:
                player = player + 1
        else:
            print('Select a letter or answer the puzzle:')
            attempt = input()
            if len(attempt) > 1:
                answerCounter = 0
                attemptWordList = list(attempt)
                for count, letter in enumerate(attemptWordList):
                    if attemptWordList[count] == chosenAnswerList[count]:
                        answerCounter += 1
                    else:
                        print("Incorrect word")
                        if player + 1 > 3:
                            player = 1
                        else:
                            player = player + 1
                        break
                if answerCounter == len(chosenAnswerList):
                    print("Congratulations! You chose the correct word")
                    finalscoreList[player - 1] = playerScoreDict[player]
                    break
            else:
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
                                if player + 1 > 3:
                                    player = 1
                                else:
                                    player = player + 1
                                break
                            else:
                                selectedLetters.append(attempt)
                                playerScoreDict[player] = playerScoreDict[player] - 250
                            if attempt in chosenAnswerList:
                                print('Correct Choice!')
                            else:
                                print("Incorrect choice")
                                if player + 1 > 3:
                                    player = 1
                                else:
                                    player = player + 1
                                break
                            for count, letter in enumerate(chosenAnswerList):
                                if chosenAnswerList[count] == attempt:
                                    letterCounter += 1
                                    playingField[count] = attempt
                            totalAttemptScore = letterCounter * spinScore
                            playerScoreDict[player] = playerScoreDict[player] + totalAttemptScore
                            print(f"This letter appeared {letterCounter} times for a score of {totalAttemptScore}")
                            print(f"Your new score is {playerScoreDict[player]}")
                            print(playingField)
                        else:
                            print('this is a constonant')
                            if attempt in chosenAnswerList:
                                selectedLetters.append(attempt)
                                print('Correct Choice!')
                            else:
                                selectedLetters.append(attempt)
                                print('Incorrect choice')
                                if player + 1 > 3:
                                    player = 1
                                else:
                                    player = player + 1
                                break
                            for count, letter in enumerate(chosenAnswerList):
                                if chosenAnswerList[count] == attempt:
                                    letterCounter += 1
                                    playingField[count] = attempt
                            totalAttemptScore = letterCounter * spinScore
                            playerScoreDict[player] = playerScoreDict[player] + totalAttemptScore
                            print(f"This letter appeared {letterCounter} times for a score of {totalAttemptScore}")
                            print(playingField)
                    print(f"Scores: {playerScoreDict}")
    


# In[265]:


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
    


# In[266]:


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


# In[267]:


def finalRound(player):
    global vowels
    print(f"Congratulations player {player}! You have made it to the final round")
    print("This next round is worth $1,000,000.")
    print("Here is the word: ")
    chosenAnswer = random.choice(answerList)
    chosenAnswerList = list(chosenAnswer)
    playingField = []
    for letter in chosenAnswerList:
        playingField.append('_')
    print(playingField)
    print("Here is the word after the default clues (r s t l n e)")
    defaultClues = ['r', 's', 't', 'l', 'n' 'e']
    for count, letter in enumerate(chosenAnswerList):
        for letter in defaultClues:
            if letter == chosenAnswerList[count]:
                playingField[count] = letter
                break
    print(playingField)
    guessSelections = []
    for i in range(1, 4):
        print(f"Select constonant {i}")
        attempt = input()
        if len(attempt) > 1 or attempt in vowels:
            while len(attempt) > 1 or attempt in vowels:
                print("invalid format, please enter again")
                attempt = input()
        guessSelections.append(attempt)
    print("Now choose a vowel: ")
    attempt = input()
    if attempt not in vowels:
        while attempt not in vowels:
            print("Not a vowel, please try again: ")
            attempt = input()
    guessSelections.append(attempt)
    print(f"Here are your selections: {guessSelections}")
    print("Here is the new playing field: ")
    for count, letter in enumerate(chosenAnswerList):
        for letter in guessSelections:
            if letter == chosenAnswerList[count]:
                playingField[count] = letter
                break
    print(playingField)
    print("For $1,000,000 dollars, what is the word?")
    attempt = input()
    answerCounter = 0
    attemptWordList = list(attempt)
    for count, letter in enumerate(attemptWordList):
        if attemptWordList[count] == chosenAnswerList[count]:
            answerCounter += 1
        else:
            print("Incorrect word")
            break
    if answerCounter == len(chosenAnswerList):
        print("Congratulations! You chose the correct word")


# In[ ]:





# In[ ]:




