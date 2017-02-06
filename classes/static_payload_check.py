import urllib
import re

def haz_ran(payload,url):# Static check if payload got executed...
        page = urllib.urlopen(url)
        sourcecode = page.read()
        if payload in sourcecode:       
                print("[+] Payload found in source code, please confirm if really vuln in chrome")
                launch_chrome = True
                return launch_chrome
        else:
                print("[+] Payload not found in source however you can always manually confirm it in chrome")
                manually = raw_input("[+] Do you wnat to open chrome and confirm if payload has yet been running [Yes/no] ")
                if manually == "yes" or manually == "y" or manually == "Yes" or manually == "Y":
                        launch_chrome = True
                        return launch_chrome

                elif manually == "no" or manually == "n" or manually == "No" or manually == "N":
                        launch_chrome = False
                        return launch_chrome
                                 


