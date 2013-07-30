from tkinter import *

NMB_OF_SLIDERS = 6

class App(Frame):
  def __init__(self, master=None):
    Frame.__init__(self,master)
    self.pack()
    self.createWidgets()

  def sendValues(self,event):
    status = "Sending ( " 
    for i in range(NMB_OF_SLIDERS):
      val = self.sliders[i].get()
      status += str (val)
      if (i != NMB_OF_SLIDERS - 1):
        status += ", "
    status += " )"
    self.STATUS.config(text=status)

  def addSlider(self):
    slider = Scale(from_=0, to=100, resolution=1)
    slider.pack(side = "left", expand=1, fill="both")
    slider.bind("<ButtonRelease-1>", self.sendValues)
    self.sliders.append(slider)

  def createWidgets(self):
    self.STATUS = Label()
    self.STATUS["text"] = "Status"
    self.STATUS.pack(side="bottom",fill="x", anchor="w")

    self.sliders = []
    for i in range(NMB_OF_SLIDERS):
      self.addSlider()

    self.QUIT = Button()
    self.QUIT["text"] = "Quit"
    self.QUIT["command"] = self.quit
    self.QUIT.pack(side = "right", fill="y", anchor="e")

root = Tk()
root.geometry("480x320")
app = App(master=root)
app.master.title("pyRobotArm")
app.mainloop()
root.destroy()
