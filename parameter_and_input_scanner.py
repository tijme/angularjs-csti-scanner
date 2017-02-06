from bs4 import BeautifulSoup
import urllib
import re
import math
import html5lib
from html5lib import treebuilders
import urlparse

def print_parameter_tabel(parameters):

    def cs(string, length=30):
        return (string[0+i:length+i] for i in range(0, len(string), length))

    def houndred(x):
        return int(math.ceil(x / 100.0)) * 100 


    items = parameters
    for number,item  in enumerate(items, start=1):
        name=item
        name += str(" " * int(29- len(name[0])))+ "|" 
        print("+" + "-"  *  32 + "+"  )
        print(str ("|" + str(number)+  ") " + "".join(name))  )

    print("+" + "-"  *  32 + "+"  )
       

def correct_hypertext_scheme(site):
    if 'https://' in site:
        pass
    elif 'http://' in site:
        pass
    else:
        site = "http://"+site
    return site
        
    finalurl = urlparse.urlparse(site)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=finalurl)
    print(domain)
        

def find_parameters(site): 
    correct_hypertext_scheme(site)
    parameters = []
    url = correct_hypertext_scheme(site)
    mhtml = urllib.urlopen(url)
    soup = BeautifulSoup(mhtml, 'html5lib')
    inputs = soup.findAll("input", {'type':'text'})

    #print("[+] No parameters in your url detected, but here are some input fields the page has")
     
    if len(inputs) > 0:
        for elem in inputs:
            parameter = elem['name']
            parameters.append([parameter])
            
        print("[+] No parameters in your url detected, but here are some input fields the page has")
        print("[+] Please fill in those fields and see if you can get a url with parameters included ")  
        print_parameter_tabel(parameters)
        
    else:
        print("[+] No parameters in your url detected...")
        print("[+] No input entery points found on this page...")

 

def get_parameters(site):
    parsed_url = urlparse.urlparse(site)
    parameters_with_values = urlparse.parse_qs(parsed_url.query, keep_blank_values=True)
    parameters = []
    for parameter in parameters_with_values:
        parameters.append(parameter)
    parameters.sort()
    return parameters


def print_url_parameter_tabel(parameters): #Minimal difference with print_parameter_table fucntion, removed the 0 index in the name variable

    def cs(string, length=30):
        return (string[0+i:length+i] for i in range(0, len(string), length))

    def houndred(x):
        return int(math.ceil(x / 100.0)) * 100 


    items = parameters
    for number,item  in enumerate(items, start=1):
        name=item
        name += str(" " * int(29- len(name)))+ "|" 
        print("+" +           "-"  *  32 +            "+"  )
        print(str (     "|" + str(number)+  ") " + "".join(name))  )

      
    print("+" +           "-"  *  32 +            "+"  )
    


url_choise = raw_input("[+] Please enter a url ")
parameterz = get_parameters(url_choise)  

def determine():
    if len(parameterz) > 0:
        print("[+]Parameters found!")
        print_url_parameter_tabel(parameterz)
    else:
        find_parameters(url_choise)   
    
if __name__ == "__main__":
    determine()
