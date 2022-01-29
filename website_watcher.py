
'''
Run this from windows
'''
if os.name != 'nt':
    print('Please run from Windows.')
    exit(420)

from connectX_util import WIDTH, HEIGHT
from pynput.mouse import Button, Controller
from PIL import ImageGrab

TOP_LEFT = (661, 272)
BOT_RIGHT = (1259, 779)

mouse = Controller()

def website_watcher_interactive_setup():
    global TOP_LEFT
    global BOT_RIGHT
    input("Hover mouse over top-left circle, then press enter..")
    TOP_LEFT = mouse.position
    input("Hover mouse over bottom-right circle, then press enter..")
    BOT_RIGHT = mouse.position

def get_pixels():
    img = ImageGrab.grab()
    print(img.getpixel(TOP_LEFT))
    print(img.getpixel(BOT_RIGHT))

website_watcher_interactive_setup()
print(TOP_LEFT, BOT_RIGHT)
get_pixels()

# mouse.position = TOP_LEFT
# mouse.press(Button.left)
# mouse.release(Button.left)