
import tsapp as ts


def add_all(win, *args):
    """
    Adds all objects in the function to the screen.
    Returns a list of all objects added to screen.
    """
    
    retlist = []
    
    for i in args:
        retlist.append(i)
        win.add_object(i)
        
    return retlist


def setpos(sprite, x, y):
    """Sets the sprite's x and y to the args"""
    sprite.x = x
    sprite.y = y

    
def lock_to_mouse(obj):
    """Centers an object on the mouse"""
    obj.center_x = ts.get_mouse_x()
    obj.center_y = ts.get_mouse_y()

    
def center_on(moveobj, centerobj, offset=0):
    """Centers one object on another"""
    moveobj.x = centerobj.center_x + offset
    moveobj.y = centerobj.center_y + offset

    
def check_edge(obj, window):
    """Checks if the center of an image is out of bounds and returns true if it is"""
    if obj.center_x <= 0 or obj.center_y <= 0:  # If obj is out of bounds
        return True                             # return true
    elif obj.center_x >= window.width or obj.center_y >= window.height:
        return True
    else:
        return False

    
def bounce_edge(obj, window):
    """Checks for edge and reverses the direction from witch it came"""
    if obj.center_x <= 0:
        obj.x_speed *= -1
    elif obj.center_y <= 0:
        obj.y_speed *= -1

    elif obj.center_x >= window.width:
        obj.x_speed *= -1
    elif obj.center_y >= window.height:
        obj.y_speed *= -1

        
class Button:
    def __init__(self, win, img, text, font, posx, posy, command):
        """Create a new button object"""
        self.win = win
        self.img = img
        self.txt = text
        self.font = font
        self.x = posx
        self.y = posy
        self.command = command
        
        
        btn = ts.Sprite(img, posx, posy)  # Create the btn sprite
        self.b = btn
        
        btxt = ts.TextLabel(font, 20, 0, 0,  # Create the text to go on the button
                            btn.width, text, ts.BLACK)
        
        # Set pos and add to window
        btxt.x = posx + 30
        btxt.y = posy + 30
        
        win.add_object(btn)
        win.add_object(btxt)
        
    
    def press(self):
        """Presses the button. NOTE: This only works with no argument functions"""
        self.command()
        

class Infobox:
    def __init__(self, window, boxbg, font, *args):
        """Create a new Infobox object"""
        self.win = window
        self.font = font
        self.bg = ts.Sprite(boxbg, 100, 0)  # Box sprite
        self.bg.center_x = window.width / 2
        self.txtlist = []
        
        for i in range(len(args)):  # Text list
            txt = ts.TextLabel(font, 20, (self.win.width / 2) - 100, (i + 1) * 100,
                               self.bg.width, args[i] ,ts.BLACK)
            
            self.txtlist.append(txt)
        
        # Add and set to not visible
        self.win.add_object(self.bg)
        self.bg.visible = False
        
        # Add and set text to not visible
        for i in self.txtlist:
            i.visible = False
            self.win.add_object(i)
            
            
    def openbox(self):
        """Sets the visiblity to true"""
        self.bg.visible = True
        
        for i in self.txtlist:
            i.visible = True
        
            
    
    def closebox(self):
        """Sets the visibility to false"""
        self.bg.visible = False
        
        for i in self.txtlist:
            i.visible = False
            

class Movement:
    def __init__(self, mspeed):
        """Create a new movement object"""
        self.mspeed = mspeed
        
    
    def move(self, sprite, dkeyup=ts.K_UP,
             dkeydown=ts.K_DOWN, dkeyleft=ts.K_LEFT, 
             dkeyright=ts.K_RIGHT):
        """
        Makes any sprite move with specified keys, all of wich default to the arrows
        """
        
        # Movement key dictionary
        mvdict = {dkeyup: (0, -self.mspeed), dkeydown: (0, self.mspeed), 
                  dkeyleft:(-self.mspeed, 0), dkeyright: (self.mspeed, 0)}
        
        checklist = mvdict.keys()  # List to check for movement
        
        for i in checklist:
            if ts.is_key_down(i):  # Run through the list of keys and add to the x and y if it is pressed down
                sprite.x += mvdict[i][0]
                sprite.y += mvdict[i][1]
                

class Dynamicbg:
    def __init__(self, window, sprite):
        """Create a new Dynamicbg object"""
        self.win = window
        self.spr = sprite
        
    
    def shake(self, duration):
        
        for i in range(duration * 10):  
            # Creates the illusion of a shake by rapidly adding and subtracting from the pos of the background
            self.spr.x += 10
            self.win.finish_frame()
            
            self.spr.y += 10
            self.win.finish_frame()
            
            self.spr.x -= 10
            self.win.finish_frame()
            
            self.spr.y -= 10
            self.win.finish_frame()
            
            
class Animation:
    def __init__(self, window, framerate=30):
        self.fps = framerate
        self.win = window
        
    def animate_seq(self, sprite, duration, *args):
        """Takes the sprite, and a duration with a series of images
            and displays them in a sequence of even intervals"""
        ilist = []  # List for the images 
        
        for i in range(len(args)):
            # Takes all images in *args and sppends them to a list
            # I do this for easier handling and for future compatability
            ilist.append(args[i])
            
        tick = round(duration/len(ilist))  
        # A tick is equal to the duration over the length of the 
        # image list rounded to the nearest whole number.
        
        for x in range(len(ilist)):      # For every image in the list
            for wait in range(tick):     # change the sprites image to
                sprite.image = ilist[x]  # one image in the image list
                self.win.finish_frame()  # then changes to the another 
                                         # after the time of a tick has passed
