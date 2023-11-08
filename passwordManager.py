import csv
import keyboard
import subprocess
from pywinauto import Application
import time
import psutil

username,password = None, None

allLines = []

# opening the CSV file
with open('passwords.txt', mode ='r')as file:

    csvFile = csv.reader(file)
        
    for lines in csvFile:
        allLines.append(lines)


def grab(url):
    print('Searching passwords for url:')

    headers = allLines[0]

    urls = []
    for line in allLines:
        urls.append(line[3][:len('fs.azauth.net/adfs/ls/?SAMLRequest=')])

    siteReq = url[:len('fs.azauth.net/adfs/ls/?SAMLRequest=')]
    
    try:
        print(allLines[urls.index(siteReq)])
        return allLines[urls.index(siteReq)]
    except ValueError as err:
        print('Failed due to: '+ str(err))
        return 
    
def getChromeURL():
    app = Application(backend='uia')
    app.connect(title_re=".*Chrome.*")
    dlg = app.top_window()
    url = dlg.child_window(title="Address and search bar", control_type="Edit").get_value()
    return url

def waitForPaste():
    print('Waiting for "Ctrl+V"')
    keyboard.wait('ctrl+v')

def copy(txt):
    print('Copying text:', txt.strip())
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def doSomething(site):
    print('...........Starting password retrieval process...........')
    print('Site:', site)
    info = site
    username, password = info[1], info[2]

    copy(username)
    print('...........Username copied to clipboard...........')
    waitForPaste()
    print('...........Username pasted...........')

    copy(password)
    print('...........Password copied to clipboard...........')
    waitForPaste()
    print('...........Password pasted...........')
    
    copy('not the password')
    print('...........Fake password copied to clipboard...........')
    print('...........Fake password pasted...........')

    
    print('Password retrieval process complete')

currentURL = None

def process_is_running(exename):
        # check if chrome is open
        if exename in (i.name() for i in psutil.process_iter()):
                return True
        return False

while True:
    if keyboard.is_pressed("ctrl+alt+e"):
        break

    if process_is_running('chrome.exe'):
        print("######## RUNNING #########")
        
        try:
            if getChromeURL() != currentURL:
                currentURL = getChromeURL()
                site = grab(getChromeURL())
                if site is not None:
                    doSomething(site)
        except:
            pass
    else:
        print("######## Chrome Not Open #########")
