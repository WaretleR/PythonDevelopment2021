import tkinter as tk
import string
from tkinter import font

class InputLabel(tk.Label):
    def __init__(self, master = None):
        super().__init__(master, anchor = "w")
        self.cursor = tk.Frame(self, width = 2, bg = 'black', height = 20)
        self.cursorPos = 0
        textFont = font.Font(family = "Consolas", size = 10, weight = "normal")
        self.charWidth = textFont.measure("a")
        self.config(font = textFont)
        self.labelText = ""
        self.bind("<BackSpace>", self.onBackspacePressed)
        self.bind("<KP_Home>", self.onHomePressed)
        self.bind("<KP_End>", self.onEndPressed)
        self.bind("<Left>", self.onLeftPressed)
        self.bind("<Right>", self.onRightPressed)
        self.bind("<Key>", self.onKeyPressed)
        self.bind("<Button-1>", self.onMouseButtonPressed)
        
    def onKeyPressed(self, event):
        if str(event.char).isalnum() or event.char == ' ':
            self.labelText = self.labelText[:self.cursorPos] + event.char + self.labelText[self.cursorPos:]
            self.cursorPos += 1
            self.updateText()
            self.updateCursorPosition()

    def onBackspacePressed(self, event):
        if self.cursorPos > 0:
            self.labelText = self.labelText[:self.cursorPos-1] + self.labelText[self.cursorPos:]
            self.cursorPos -= 1
            self.updateText()
            self.updateCursorPosition()

    def onHomePressed(self, event):
        self.cursorPos = 0
        self.updateCursorPosition()

    def onEndPressed(self, event):
        self.cursorPos = len(self.labelText)
        self.updateCursorPosition()

    def onLeftPressed(self, event):
        self.cursorPos = max(0, self.cursorPos - 1)
        self.updateCursorPosition()

    def onRightPressed(self, event):
        self.cursorPos = min(len(self.labelText), self.cursorPos + 1)
        self.updateCursorPosition()

    def onMouseButtonPressed(self, event):
        self.focus()
        self.config(borderwidth="1", relief = "groove")
        self.cursorPos = min(event.x // self.charWidth, len(self.labelText))
        self.updateCursorPosition()

    def updateCursorPosition(self):
        self.cursor.place(x = self.charWidth * self.cursorPos)

    def updateText(self):
        self.config(text = self.labelText)

if __name__ == "__main__":
    R = tk.Tk()
    F = tk.Frame(R)
    F.grid(sticky="NEWS")
    R.rowconfigure(0, weight=1)
    R.columnconfigure(0, weight=1)
    I = InputLabel(F)
    I.grid(row = 0, sticky = "WE")
    buttonEsc = tk.Button(F, text = "Quit", command = R.quit)
    buttonEsc.grid(row=1, sticky = "NES")
    F.rowconfigure(0, weight = 1)
    F.rowconfigure(1, weight = 1)
    F.columnconfigure(0, weight = 1)
    R.mainloop()