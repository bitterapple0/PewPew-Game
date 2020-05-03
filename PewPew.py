import kivy
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
import random

class InstructionWindow(Screen):
    txt="Welcome to PewPew, the simple tapping game to test your focus and tapping speed!\n\n    Goal: Hit as many boxes, each are worth 10 points. \n    How: When box above it is green, tap the 'SHOOT' button or press\n              W = Right Button \n              E or O = Middle Button \n              P = Left Button. \n    Time Limit: 30 seconds \n    Bonus: The higher the score, the cooler the message at the end. \n \n*Note: Game is best played with a touchscreen device.*"

class StartWindow(Screen):    
    def quit_app(self):
        App.get_running_app().stop()
        Window.close()
        
class GameWindow(Screen):   
######### Functions to initialise the screen #########  
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self.matrix=[]
        self.row=[]
        self.score=0
        self.time=30
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        Clock.schedule_once(self.make_matrix,0)   
        Clock.schedule_once(self.set_color,0)
        
        
    def make_matrix(self, dt=0):  # make matrix of the ids of colored boxes
        for i in self.ids.keys():  
            if i[0]=='a':
                if len(self.row)<3:
                    self.row.append(i)
                else:
                    self.matrix.append(self.row)
                    self.row=[]
                    self.row.append(i)
        self.matrix.append(self.row)
        
    def set_color(self,dt=0): # randomises the starting colors shown on screen 
        
        for i in self.matrix:
            for x in i:
                self.ids[x].color=[0,0,0,1]
            green=random.randint(0,2)
            self.ids[i[green]].color=[0,1,0,.7]
######### Function to bind keys #########
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        if key == 'w':
            self.color_check('a41')
        if key =='e' or key =='o':
            self.color_check('a42')
        if key =='p':
            self.color_check('a43')
            
######### Function for button #########                            
    def color_check(self, box_id): #box_id is id of box directly above the button as a string
        if self.ids[box_id].color==[0,1,0,.7]:
            self.color_change()
            self.add_score()
            self.start_timer()
            
######### Function to change color #########              
    def color_change(self):     
        for i in range(1,4):       # downward motion of the boxes
            col1=self.matrix[-i][0]
            col2=self.matrix[-i][1]
            col3=self.matrix[-i][2]
            prev_col1=self.matrix[-i-1][0]
            prev_col2=self.matrix[-i-1][1]
            prev_col3=self.matrix[-i-1][2]
            self.ids[col1].color=self.ids[prev_col1].color
            self.ids[col2].color=self.ids[prev_col2].color
            self.ids[col3].color=self.ids[prev_col3].color
        
        for i in self.matrix[0]:       # resets all the 1st row to blank
            self.ids[i].color=[0,0,0,1] 
            
        new_green= random.randint(0,2) # new green box (only 1)
        key=self.matrix[0][new_green]
        self.ids[key].color=[0,1,0,.7]  

######### Functions to add/reset scores #########  
    def add_score(self):  # changes the score label
        self.score +=10
        self.ids.score.text='Score:{:5d}'.format(self.score)
    
    def reset_score(self): # resets the score value to 0 and makes label blank
        self.score=0
        self.ids.score.text=''
        
######### Functions to start/reset timer #########
    def start_timer(self): # starts the timer when player makes first successful hit
        if self.score == 10:
            Clock.schedule_once(self.timer,0)
            Clock.schedule_interval(self.timer,1)
    def timer(self,dt=0): # displays the time on the label
        if self.time >= 0: 
            self.ids.timer.text='Time:{:3d}'.format(self.time)
            self.time -= 1            
        else:
            Clock.unschedule(self.timer)
            self._keyboard_closed()
            self.end_popup()
            
    def reset_timer(self): # resets time value to 30 and makes timer label blank
        self.time=30
        self.ids.timer.text=''
        Clock.unschedule(self.timer)
        
######### Functions for total reset #########    
    def reset(self,event): #runs the function in order(for the button in popup)
        self.reset_score()
        self.reset_timer()
        self.set_color()
        self._keyboard.bind(on_key_down=self._on_keyboard_down)        
        self.manager.transition.direction = 'right'
        self.manager.current = "start"
        
######### Popup function when game ends #########          
    def end_popup(self): # pop up when time value reaches 0 or when player leaves
        show=End_Popup_Content() 
        show.ids.score_final.text='Final Score:{:5d}'.format(self.score) 
        if self.score==0:
            txt=show.comments[0]
        elif self.score<=400:
            txt=show.comments[1]
        elif self.score<=900:
            txt=show.comments[2]
        elif self.score<=1500:
            txt=show.comments[3]
        elif self.score<=2000:
            txt=show.comments[4]
        elif self.score<=2200:
            txt=show.comments[5]
        elif self.score>2200:
            txt=show.comments[6]       
        show.ids.comment.text=txt
        popup_window = Popup(title='', 
                             content=show, 
                             auto_dismiss=False, 
                             size_hint=(None,None),
                             size=(400,400))
        show.ids.btn.bind(on_press=self.reset)
        show.ids.btn.bind(on_release=lambda *args: popup_window.dismiss())
        popup_window.open()
        

class GameApp(App):
     def build(self):
        return Builder.load_file('UI_PewPew.kv')

######### Additional classes #########

class New_Tap(Label):
    color = ListProperty([0,0,0,1])

class Tap(Label):
    color = ListProperty([0,0,0,1])
    
class End_Popup_Content(FloatLayout):
    comments=['Looks like we have a quitter....',
             'Would you like the code to edit your score?',
             'Hellooo are you even trying?',
             'Hmmm, decent score...',
             'Oh, looks like we got a Speedy Mcgee here',
             "Wow you're good, but is this the last level?",
             'LEGENDARY, are you Prof Oka?']
GameApp().run()


