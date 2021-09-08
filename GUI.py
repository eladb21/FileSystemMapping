import PySimpleGUI as sg
import mongoDbConnection as mdc
import slowScanning as ss
import fastScanning as fs

class GUI():
    def __init__(self):
        self.mongoClient = mdc.mongoModule()
        self.slowScanner = ss.slowScannerModule()
        self.fastScanner = fs.fastScannerModule()

    def startGUI(self):
        sg.theme('Topanga')
        # Add some color to the window

        def slowScanner():
            self.slowScanner.scanToDb()
            sg.popup_ok('Done slow scanning')

        def fastScanner():
            self.fastScanner.start()
            sg.popup_ok('Done fast scanning')

        def dbCleaner():
            self.mongoClient.cleanCol()
            sg.popup_ok('Done cleaning database')

        dispatch_dictionary = {'slow': slowScanner, 'fast': fastScanner, 'del': dbCleaner}

        layout = [
            [sg.Text("That program can scan your filesystem into DB in two ways:", size=(50, 2))],
            [sg.Text("Slow scanning - regular scanning, scanning the files one by one in hierarchical order.")],
            [sg.Text("Fast scanning - multiprocess scanning, scanning the files in parallel, optimal for multi-core"
                     " computers.", size=(80, 3))],
            [sg.Button(key='slow', button_text='Slow scanning'), sg.Button(key='fast', button_text='Fast scanning'),
            sg.Button(key='del', button_text='Clean database')],
            [sg.Quit()]
        ]

        window = sg.Window('FilesystemScanner - by Elad Ben-Avraham', layout)
        while True:
            # Read the Window
            event, value = window.read()
            if event in ('Quit', sg.WIN_CLOSED):
                break
            # Lookup event in function dictionary
            if event in dispatch_dictionary:
                func_to_call = dispatch_dictionary[event]   # get function from dispatch dictionary
                func_to_call()
            else:
                print('Event {} not in dispatch dictionary'.format(event))

        window.close()

