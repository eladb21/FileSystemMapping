import GUI
from multiprocessing import freeze_support

if __name__ == '__main__':
    #freeze support for handle with multiprocessing in fast scanner
    freeze_support()
    #start GUI
    gui = GUI.GUI()
    gui.startGUI()
