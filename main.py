import serial
import time
import threading
import sys

NMB_OF_SLIDERS = 6
PORT = "loop://logging=debug"

if sys.version_info >= (3, 0):
    from tkinter import *
    def data(string):
        return bytes(string, 'latin1')
else:
    from Tkinter import *
    def data(string): return string


class App(Frame):
  def __init__(self, master=None):
    Frame.__init__(self,master)
    master.protocol("WM_DELETE_WINDOW", self.stop)
    self.pack()
    self.createWidgets()
    self.serial = serial.serial_for_url(PORT, timeout=0.1)
    self.alive = True
    self.thread_read = threading.Thread(target=self.reader)
    self.thread_read.setDaemon(True)
    self.thread_read.setName('read serial')
    self.thread_read.start()

  def reader(self):
    """loop forever """
    while self.alive:
      try:
        data = self.serial.read(1)              # read one, blocking
        n = self.serial.inWaiting()             # look if there is more
        if n:
          data = data + self.serial.read(n)   # and get as much as possible
        if data:
	  #here some parsing is to be done, to get the real positions for the sliders, as feedback from arduino
          values = data.decode().split(',')
          assert (len(values) == NMB_OF_SLIDERS)
          for i in range(NMB_OF_SLIDERS):
            self.sliders[i].set(int(values[i]))
      except:
        sys.stderr.write('ERROR: %s\n' % sys.exc_info()[0] )
        raise
    self.alive = False

  def sendValues(self,event):
    status = ""
    for i in range(NMB_OF_SLIDERS):
      val = self.sliders[i].get()
      status += str (val)
      if (i != NMB_OF_SLIDERS - 1):
        status += ", "
    self.serial.write(data(status))
    self.STATUS.config(text="Sent: <" + status + ">")

  def addSlider(self):
    slider = Scale(from_=0, to=100, resolution=1)
    slider.pack(side = "left", expand=1, fill="both")
    slider.bind("<ButtonRelease-1>", self.sendValues)
    self.sliders.append(slider)

  def stop(self):
    if self.alive:
      self.alive = False
      self.thread_read.join()
      self.quit();

  def createWidgets(self):
    self.STATUS = Label()
    self.STATUS["text"] = "Status"
    self.STATUS.pack(side="bottom",fill="x", anchor="w")

    self.sliders = []
    for i in range(NMB_OF_SLIDERS):
      self.addSlider()

    self.QUIT = Button()
    self.QUIT["text"] = "Quit"
    self.QUIT["command"] = self.stop
    self.QUIT.pack(side = "right", fill="y", anchor="e")

root = Tk()
root.geometry("480x320")
app = App(master=root)
app.master.title("pyRobotArm")
app.mainloop()
root.destroy()
