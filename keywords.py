from colored import Fore, Style

#Console Colors
c_red = Fore.red
c_blue = Fore.blue
c_green = Fore.green
c_white = Fore.white
c_yellow = Fore.yellow
c_rst = Style.reset

#Console Debugs
def print_warning(*txt):
    string = ""
    for substr in txt:
        string += str(substr) + " "
    print(f"{c_white}[{c_rst}{c_yellow}warning{c_rst}{c_white}]{c_rst} " + string)

def print_error(*txt):
    string = ""
    for substr in txt:
        string += str(substr) + " "
    print(f"{c_white}[{c_rst}{c_red}error{c_rst}{c_white}]{c_rst} " + string)

def print_debug(*txt):
    string = ""
    for substr in txt:
        string += str(substr) + " "
    print(f"{c_white}[{c_rst}{c_blue}debug{c_rst}{c_white}]{c_rst} " + string)

def print_success(*txt):
    string = ""
    for substr in txt:
        string += str(substr) + " "
    print(f"{c_white}[{c_rst}{c_green}success{c_rst}{c_white}]{c_rst} " + string)
