import PySimpleGUI as sg
import mongoDbConnection as mdc
import slowScanning as ss
import fastScanning as fs

class GUI():
    '''
    The program GUI, manage all of the options for the client
    '''
    def __init__(self):
        #init agents
        self.mongoClient = mdc.mongoModule()
        self.slowScanner = ss.slowScannerModule()
        self.fastScanner = fs.fastScannerModule()

    def startGUI(self):
        # symbols for query section
        SYMBOL_UP = '▲'
        SYMBOL_DOWN = '▼'

        def collapse(layout, key):
            return sg.pin(sg.Column(layout, key=key))

        def slowScanner():
            # starting slow scanner
            self.slowScanner.scanToDb()
            sg.popup_ok('Done slow scanning')

        def fastScanner():
            # starting fast scanner
            self.fastScanner.start()
            sg.popup_ok('Done fast scanning')

        def dbCleaner():
            # clean DB collection
            self.mongoClient.cleanCol()
            sg.popup_ok('Done cleaning database')

        def queriesFunc(event, dict):
            # search by file extension
            if event == 'ext':
                ans = self.mongoClient.searchByExtension(dict['-EXT-'])
                if ans.count() != 0:
                    for inst in ans:
                        print(inst)
                else:
                    print("Empty results")

            # search by file name
            elif event == 'fn':
                ans = self.mongoClient.searchByFilename(dict['-F_N-'])
                if ans.count() != 0:
                    for inst in ans:
                        print(inst)
                else:
                    print("Empty results")

            # search from last modify date
            elif event == 'lmd':
                ans = self.mongoClient.searchFromModifyDate(dict['-LMD-'])
                if ans.count() != 0:
                    for inst in ans:
                        print(inst)
                else:
                    print("Empty results")

            # search by file attributes
            elif event == 'attr':
                ans = self.mongoClient.searchByAttribute(dict['-ATTR-'])
                if ans.count() != 0:
                    for inst in ans:
                        print(inst)
                else:
                    print("Empty results")

        sg.theme('Topanga')
        # add some color to the window

        # option functions
        dispatch_dictionary = {'slow': slowScanner, 'fast': fastScanner, 'del': dbCleaner}
        queries = ['ext', 'fn', 'lmd', 'attr']

        # queries section
        section1 = [[sg.Text("Search by files extension - (.txt, .exe, etc.)")],
                    [sg.Input(key='-EXT-')],
                    [sg.Button('By extension', key='ext')],
                    [sg.Text("Search by file name")],
                    [sg.Input(key='-F_N-')],
                    [sg.Button('By file name', key='fn')],
                    [sg.Text("Search from last modified date - (format: YYYY-MM-DD)")],
                    [sg.Input(key='-LMD-')],
                    [sg.Button('From modified date', key='lmd')],
                    [sg.Text("Search by attribute - (hidden, system, etc.)")],
                    [sg.Input(key='-ATTR-')],
                    [sg.Button('By attribute', key='attr')]]

        # scanning section
        layout = [
            [sg.Text("That program can scan your filesystem into DB in two ways:", size=(50, 2))],
            [sg.Text("Slow scanning - regular scanning, scanning the files one by one in hierarchical order.")],
            [sg.Text("Fast scanning - multiprocess scanning, scanning the files in parallel, optimal for multi-core"
                     " computers.", size=(80, 3))],
            [sg.Button(key='slow', button_text='Slow scanning'), sg.Button(key='fast', button_text='Fast scanning'),
            sg.Button(key='del', button_text='Clean database')],

                        #### query section settings ####
            [sg.T(SYMBOL_DOWN, enable_events=True, k='-OPEN SEC1-', text_color='yellow'),
             sg.T('Queries', enable_events=True, text_color='yellow', k='-OPEN SEC1-TEXT')],
            [collapse(section1, '-SEC1-')],
            [sg.Quit()]
        ]

        # window title
        window = sg.Window('FilesystemScanner - by Elad Ben-Avraham', layout)

        opened1 = True

        while True:
            # read the Window
            event, value = window.read()
            if event in ('Quit', sg.WIN_CLOSED):
                break
            # lookup event in function dictionary
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

