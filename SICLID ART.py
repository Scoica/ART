from tkinter import *   
import siclidrobo

def create():
    win = Toplevel(root)
    win.destroy()
    win.update()
    root.destroy()
    root.update()
    siclidrobo.main()


root = Tk()
root.title('SICLID Automatic Regression Tool')
root.geometry('200x100')  
btn = Button(root, text="Start SICLID ART", command = create)
btn.pack(pady = 10) 
root.mainloop()

