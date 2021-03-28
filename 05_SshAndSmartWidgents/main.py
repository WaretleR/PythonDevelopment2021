import tkinter as tk
import random

class GraphEditCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs, highlightcolor="red")
        self.objInfo = {}
        self.prevCursorPos = (0, 0)
        self.startCursorPos = (0, 0)
        self.isCreating = True
        self.processedFigure = None

    def processClick(self, event):
        figures = event.widget.find_withtag("current")
        if len(figures) > 0:
            self.isCreating = False
            self.processedFigure = figures[0]
        else:
            self.isCreating = True
            color = random.choice(["#000000", "#ffffff", "#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff"])
            outline = "#000000"
            width = 2
            self.processedFigure = self.create_oval(event.x, event.y, event.x, event.y, fill=color, outline = outline, width = width)
            self.objInfo[self.processedFigure] = {"coords" : self.coords(self.processedFigure), "fill" : color, "outline" : outline, "width" : width}

        self.prevCursorPos = (event.x, event.y)
        self.startCursorPos = (event.x, event.y)

    def processMotion(self, event):
        if self.isCreating:
            self.coords(self.processedFigure, min(self.startCursorPos[0], event.x), min(self.startCursorPos[1], event.y), max(self.startCursorPos[0], event.x), max(self.startCursorPos[1], event.y))
        else:
            self.move(self.processedFigure, event.x - self.prevCursorPos[0], event.y - self.prevCursorPos[1])
        self.prevCursorPos = (event.x, event.y)

    def processRelease(self, event):
        if self.processedFigure in self.objInfo:
            self.objInfo[self.processedFigure]["coords"] = self.coords(self.processedFigure)


    def update(self, textInfo):
        self.delete("all")
        self.objInfo = {}
        wrongLines = []
        lines = textInfo.split("\n")[:-1]
        for i, l in enumerate(lines):
            try:
                coords = l.split(";")[0].split('[')[1].split(']')[0].split(',')
                for j, c in enumerate(coords):
                    coords[j] = float(c)
                color = '#' + l.split(";")[1].strip()
                width = int(l.split(";")[2])
                outline = '#' + l.split(";")[3].strip()
                objID = self.create_oval(*coords, fill=color, outline=outline, width=width)
                self.objInfo[objID] = {"coords" : coords, "fill" : color, "width" : width, "outline" : outline}
            except:
                wrongLines.append(i)
        return wrongLines


class GraphEditText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
    
    def update(self, canvasInfo):
        self.delete("1.0", "end")
        for obj in canvasInfo.values():
            strInfo = "%s; %s; %d; %s\n" % (obj["coords"], obj["fill"][1:], obj["width"], obj["outline"][1:])
            self.insert("end", strInfo)


class Application(tk.Frame):

    def __init__(self, master=None, title="Application", **kwargs):
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        pass

class App(Application):
    def create_widgets(self):
        self.T = GraphEditText(self, undo=True, wrap=tk.WORD, font="fixed",
                inactiveselectbackground="MidnightBlue")
        self.T.grid(row=0, column=0, sticky="NEWS")
        self.C = GraphEditCanvas(self)
        self.C.grid(row=0, column=1, sticky="NEWS")

        self.C.bind("<Button-1>", self.C.processClick)
        self.C.bind("<B1-Motion>", self.C.processMotion)
        self.C.bind("<ButtonRelease-1>", self.processRelease)
        self.C.bind("<Enter>", self.processCursorEnter)

    def processRelease(self, event):
        self.C.processRelease(event)
        self.T.update(self.C.objInfo)

    def processCursorEnter(self, event):
        wrongLines = self.C.update(self.T.get("1.0", "end-1c"))
        for tag in self.T.tag_names():
            self.T.tag_delete(tag)
        for l in wrongLines:
            self.T.tag_add("error", str(l + 1) + ".0", str(l + 1) + ".end")
        self.T.tag_config("error", background = "red")



app = App(title="Graph Edit")
app.mainloop()
