import tkinter
import random
from tkinter import messagebox

def onWindowResize(*args, **kwargs):
    maxWidth = 0
    for b in buttonsGame:
        maxWidth = max(maxWidth, b.winfo_reqwidth())
    for i in range(4):
        F.columnconfigure(i, weight=1, minsize = maxWidth)

def onButtonPressed(buttonLabel):
    buttonMatrix = [[0 for j in range(4)] for i in range(4)]
    for k in range(15):
        buttonMatrix[buttonsGame[k].grid_info()['row'] - 1][buttonsGame[k].grid_info()['column']] = k + 1

    i = -1
    j = -1
    for m, row in enumerate(buttonMatrix):
        if buttonLabel in row:
            i = m
            j = row.index(buttonLabel)
            break
            
    for m, n in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if m >= 0 and m < 4 and n >= 0 and n < 4 and buttonMatrix[m][n] == 0:
                buttonMatrix[m][n] = buttonMatrix[i][j]
                buttonMatrix[i][j] = 0
                buttonsGame[buttonLabel - 1].grid(row = m + 1, column = n)
                
                for x in range(4):
                    for y in range(4):
                        if buttonMatrix[x][y] != (4 * x + y + 1) % 16:
                            return
                
                M = tkinter.messagebox.showinfo(title="15", message="You win!")
                shuffleGrid()
                return

def checkShuffle(labels):
    n = 0
    nextLabels = []
    for i, l in enumerate(labels[::-1]):
        for t in nextLabels:
            if t < l:
                n += 1
        nextLabels.append(l)

    return n % 2 == 0


def shuffleGrid():
    buttonLabels = [i for i in range(1, 16)]
    random.shuffle(buttonLabels)
    while not checkShuffle(buttonLabels):
        random.shuffle(buttonLabels)
    buttonLabels.append(0)
    buttonMatrix = [[buttonLabels[4 * i + j] for j in range(4)] for i in range(4)]
    for k, l in enumerate(buttonLabels[:-1]):
        buttonsGame[l - 1].grid(row = k // 4 + 1, column = k % 4, sticky = "NEWS")
    

R = tkinter.Tk()
R.title("15")
R.minsize(180, 180)
F = tkinter.Frame(R)
F.grid(sticky="NEWS")
R.rowconfigure(0, weight=1)
R.columnconfigure(0, weight=1)

for i in range(1, 5):
    F.rowconfigure(i, weight = 1)

buttonNew = tkinter.Button(F, text = "New", command = shuffleGrid)
buttonEsc = tkinter.Button(F, text = "Exit", command = R.quit)
buttonNew.grid(row=0, columnspan=2)
buttonEsc.grid(row=0, column=2, columnspan=2)

buttonsGame = []
for i in range(15):
    buttonsGame.append(tkinter.Button(F, text = i + 1, command = lambda t = i: onButtonPressed(t + 1)))
    
onWindowResize()
R.bind("<Configure>", onWindowResize)

shuffleGrid()
R.mainloop()