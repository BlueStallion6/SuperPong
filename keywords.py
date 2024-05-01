from colored import Fore, Style

#Console Colors
c_red = Fore.red
c_blue = Fore.blue
c_green = Fore.green
c_white = Fore.white
c_yellow = Fore.yellow
c_rst = Style.reset

#Colors
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (190, 190, 190)
    LIGHT_GRAY = (215, 215, 215)
    LIGHTER_GRAY = (245, 245, 245)
    DARK_GRAY = (80, 80, 80)
    VERY_DARK_GRAY = (50, 50, 50)
    WAY_TOO_DARK_GRAY = (38, 38, 38)
    MEGA_LIGHT_BLUE = (200, 200, 255)
    MEGA_LIGHT_RED = (255, 200, 200)

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
