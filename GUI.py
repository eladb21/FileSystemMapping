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

        SYMBOL_UP = '▲'
        SYMBOL_DOWN = '▼'

        def collapse(layout, key):
            return sg.pin(sg.Column(layout, key=key))

        def slowScanner():
            self.slowScanner.scanToDb()
            sg.popup_ok('Done slow scanning')

        def fastScanner():
            self.fastScanner.start()
            sg.popup_ok('Done fast scanning')

        def dbCleaner():
            self.mongoClient.cleanCol()
            sg.popup_ok('Done cleaning database')

        def queriesFunc(event, dict):
            if event == 'ext':
                ans=8
            elif event == 'fn':
                ans=8
            elif event == 'lmd':
                ans=8
            elif event == 'attr':
                ans=8

        sg.theme('Topanga')
        # Add some color to the window

        dispatch_dictionary = {'slow': slowScanner, 'fast': fastScanner, 'del': dbCleaner}
        queries = ['ext', 'fn', 'lmd', 'attr']

        section1 = [[sg.Text("Search by files extension - (.txt, .exe, etc.)")],
                    [sg.Input(key='-EXT-')],
                    [sg.Button('By extension', key='ext')],
                    [sg.Text("Search by file name")],
                    [sg.Input(key='-F_N-')],
                    [sg.Button('By file name', key='fn')],
                    [sg.Text("Search from last modified date - (YYYY/MM/DD)")],
                    [sg.Input(key='-LMD-')],
                    [sg.Button('From modified date', key='lmd')],
                    [sg.Text("Search by attribute - (hidden, system, etc.)")],
                    [sg.Input(key='-ATTR-')],
                    [sg.Button('By attribute', key='attr')]]

        layout = [
            [sg.Text("That program can scan your filesystem into DB in two ways:", size=(50, 2))],
            [sg.Text("Slow scanning - regular scanning, scanning the files one by one in hierarchical order.")],
            [sg.Text("Fast scanning - multiprocess scanning, scanning the files in parallel, optimal for multi-core"
                     " computers.", size=(80, 3))],
            [sg.Button(key='slow', button_text='Slow scanning'), sg.Button(key='fast', button_text='Fast scanning'),
            sg.Button(key='del', button_text='Clean database')],

                        #### Query section ####
            [sg.T(SYMBOL_DOWN, enable_events=True, k='-OPEN SEC1-', text_color='yellow'),
             sg.T('Queries', enable_events=True, text_color='yellow', k='-OPEN SEC1-TEXT')],
            [collapse(section1, '-SEC1-')],
            [sg.Quit()]
        ]

        window = sg.Window('FilesystemScanner - by Elad Ben-Avraham', layout)

        opened1 = True

        while True:
            # Read the Window
            event, value = window.read()
            if event in ('Quit', sg.WIN_CLOSED):
                break
            # Lookup event in function dictionary
            if event in dispatch_dictionary:
                func_to_call = dispatch_dictionary[event]   # get function from dispatch dictionary
                func_to_call()
            if event in queries:
                queriesFunc(event, value)
            if event.startswith('-OPEN SEC1-'):
                opened1 = not opened1
                window['-OPEN SEC1-'].update(SYMBOL_DOWN if opened1 else SYMBOL_UP)
                window['-SEC1-'].update(visible=opened1)


        window.close()

