import PySimpleGUI as sg

sg.theme('Topanga')
# Add some color to the window

def slowScanner():
    a=8

def fastScanner():
    a=8

def dbCleaner():
    a=8

dispatch_dictionary = {'slow':slowScanner, 'fast':fastScanner, 'del':dbCleaner}

layout = [
    [sg.Text("That program can scan your filesystem into DB in two ways:", size=(50, 2))],
    [sg.Text("Slow scanning - regular scanning, scanning the files one by one in hierarchical order.")],
    [sg.Text("Fast scanning - multiprocess scanning, scanning the files in parallel, optimal for multi-core computers.",
             size=(80, 3))],
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

    # All done!
sg.popup_ok('Done')