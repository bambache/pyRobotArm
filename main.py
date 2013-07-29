from tkinter import *

class App(Frame):
  def __init__(self, master=None):
    Frame.__init__(self,master)
    self.pack()
    self.createWidgets()

  def sendValues(self,event):
    val_a = self.a.get()
    val_b = self.b.get()
    val_c = self.c.get()
    val_d = self.d.get()
    val_e = self.e.get()
    val_f = self.f.get()
    status = "Sending ( " 
    status += str (val_a) + ", " + str (val_b) + ", "
    status += str (val_c) + ", " + str (val_d) + ", "
    status += str (val_e) + ", " + str (val_f)
    status += " )"
    self.STATUS.config(text=status)

  def createWidgets(self):
    self.a = Scale(from_=0, to=100, resolution=1)
    self.a.pack(side = "left", expand=1, fill="both")
    self.a.bind("<ButtonRelease-1>", self.sendValues)

    self.b = Scale(from_=0, to=100, resolution=1)
    self.b.pack(side = "left", expand=1, fill="both")
    self.b.bind("<ButtonRelease-1>", self.sendValues)

    self.c = Scale(from_=0, to=100, resolution=1)
    self.c.pack(side = "left", expand=1, fill="both")
    self.c.bind("<ButtonRelease-1>", self.sendValues)

    self.d = Scale(from_=0, to=100, resolution=1)
    self.d.pack(side = "left", expand=1, fill="both")
    self.d.bind("<ButtonRelease-1>", self.sendValues)

    self.e = Scale(from_=0, to=100, resolution=1)
    self.e.pack(side = "left", expand=1, fill="both")
    self.e.bind("<ButtonRelease-1>", self.sendValues)

    self.f = Scale(from_=0, to=100, resolution=1)
    self.f.pack(side = "left", expand=1, fill="both")
    self.f.bind("<ButtonRelease-1>", self.sendValues)

    self.STATUS = Label()
    self.STATUS["text"] = "Status"
    self.STATUS.pack(side="bottom",fill="x", anchor="s")

    self.QUIT = Button()
    self.QUIT["text"] = "Quit"
    self.QUIT["command"] = self.quit
    self.QUIT.pack(side = "left", fill="y", anchor="e")

root = Tk()
app = App(master=root)
app.master.title("pyRobotArm")
app.mainloop()
root.destroy()
