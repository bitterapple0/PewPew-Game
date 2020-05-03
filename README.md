# PewPew-Game
Digital World Final Assignment
## Game Summary
This is a simple tapping game where the player aims to hit as many green blocks as they can within a time limit. The more successful hits, the higher their score.

Being able to see the incoming blocks, players can know which button to hit ahead of time. The game challenges the player's focus, hand-eye coordination and reaction time.   

Addtitonally, various comments are displayed based on the obtained score which encourages them to play more.    

## How to Play
### Main 
1. Tap on the **'Start'** button to transition to gameplay     screen 

 
2. To successfully shoot a green box, tap on the shoot button when there is a green box in the row directly above it.<br>Alternatively, you can use your keyboard as well:
    - W = Left Button
    - E or O = Middle Button
    - P = Right Button   

 *Each row will always have only 1 green box* and you can see 4 rows of incoming green to tap.


3. Once you make the first successful shot, the Timer would start and is displayed on the top left and Score in the center. 


4. Hit as many as you can within 30 seconds and your final score would appear once the timer ends. There is a bonus comment based on what you scored. 


5. Tap on the **'Close'** button to return to the start screen. 

### Additional
- To prematurely end the game, tap on the **'Leave'** button in the top right of the game screen. 


- Instructions can be found by tapping **'Instructions'** button in the start screen.


- To close the application, tap the **'Quit'** button in the start screen. 

## Code
By using Kivy, the game feels more authentic as user only needs to interact with the UI while code runs in background. Kivy keeps the code 'clean' as a majority of the UI code and some functions can be written neatly in the `.kv` file. Code in `python` file reserved for creating functions of the `widgets` in UI.  
### Imports
Not all kivy classes had to be imported as a majority could be accessed via the `.kv` file. Only import ones we have to access directly in the python code.

### To initialise App
```python
class GameApp(App):
    def build(self):
        return Builder.load_file('game.kv')
...
GameApp().run() 
```
- created an instance of `App` class and defined `build` to return `game.kv` file.
- `game.kv` file must be saved in same location as `PewPew` file.
- `GameApp().run()` must be at the very end of your code to run the app.

### To quit the App
```python
    def quit_app(self):
        App.get_running_app().stop()
        Window.close()
```
-  Binded to 'Quit' button in `game.kv` file  
- `App.get_running_app().stop()` stops the running app
- `Window.close()` closes the kivy window

### Sceens and Transitioning
```python
class InstructionWindow(Screen):
class StartWindow(Screen):
class GameWindow(Screen):```

```
ScreenManager:
   StartWindow:
   GameWindow:
   InstructionWindow:
``` 

- `ScreenManger:` in `.kv` file is the root widget of the app.
- The lines indented below it are the `Screen` it manages
- In each `Screen` we have to define a `name: "name"` in `.kv` file which allows us to transition between screens:

 Python:<br>`self.manager.transition.direction = 'right'
 self.manager.current = "start"`
 
 Kivy:<br>`app.root.current= "start" 
 root.manager.transition.direction="right"` 
 

### Game Functionality
#### UI 
##### Main body
```  
<GameWindow>:
    name: "game"
          
    GridLayout:
        cols:3
        spacing:20
        Label:
            id: timer
            font_size: 20    
        Label:
            id: score
            font_size: 20
        Button:
            id: leave
            text: 'Leave Game'
            font_size:20
            on_press: 
                app.root.current= "start" 
                root.manager.transition.direction="left"
                root.end_popup()
                root.reset_score()
                root.reset_timer()
                root.set_color()               
        New_Tap:
            id:a11
        New_Tap:
            id:a12
        New_Tap:
            id:a13
        Tap:
            id:a21
        Tap:
            id:a22
        Tap:
            id:a23
        Tap:
            id:a31
        Tap:
            id:a32
        Tap:
            id:a33
        Tap:
            id:a41
        Tap:
            id:a42
        Tap:
            id:a43
        Shoot_btn:                  
            
            on_press: root.color_check('a41')
        Shoot_btn:
            
            on_press: root.color_check('a42')
        Shoot_btn:
            
            on_press: root.color_check3('a43')
```

- Uses a `GridLayout` with 3 columns and a `spacing` which creates spaces between child widgets in layout.
- Child widgets fill each column from left to right in order you add them. Creates new row when no more columns to fill
- Widgets with `id="id"` allow python code to reference kivy widgets via `self.ids["id"]`. 
- To bind function to button, simply indent after `event:` and reference the fucntions defined in the root class (in this case it is `GameWindow(Screen)`) with `root.function_name()`. Functions will be called in order when event occurs. 


##### Green boxes and Shoot button
```
<New_Tap>:
    text:''
    font_size: 35
    canvas:
        Color:
            rgba: self.color
        Rectangle:
            size: self.size
            pos: self.pos  
<Tap>:
    text:''
    font_size: 35
    canvas:
        Color:
            rgba: self.color
        Rectangle:
            size: self.size
            pos: self.pos

<Shoot_btn@Button>:
    text:'SHOOT'
    font_size: 35
```
- Instead of repeatedly listing the same property for labels or buttons, I created a custom class and set its attributes such as `text:`, which all instances would have. `.kv` file is thus much neater.
- If i need to access the attributes in python, I would create the class in python as well:

```python
class New_Tap(Label):
    color = ListProperty([0,0,0,1])

class Tap(Label):
    color = ListProperty([0,0,0,1])
```
    
- If not I would use dynamic class creation in kivy: eg. `<Shoot_btn@Button>:` creates a subclass `Shoot_button` of `Button` class
- `Canvas` in the `Tap` and `New_Tap` classes give the `Label` class a back ground color, which forms the green squares of the game. The size and position follows the size of the label via `self.size` and `self.pos`. Color is set by passing in a list attribute defined in the python file and accessed via `self.color`  


#### Attributes and The matrix
```python
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
        
    def make_matrix(self, dt=0):  # make matrix of the coloured boxes
        for i in self.ids.keys():  
            if i[0]=='a':
                if len(self.row)<3:
                    self.row.append(i)
                else:
                    self.matrix.append(self.row)
                    self.row=[]
                    self.row.append(i)
        self.matrix.append(self.row)
```
- In `__init__` , we have to use **super()** to inherit the `__init__` of the parent class and build on it. We have to define it here as we wish to add attributes and make it call new functions upon initialisation of the class.
- Added attributes the `GameWindow` class are `self.socre` to track score and `self.time` to track time left
- The `Clock` is a kivy object that schedules running a function during the `__init__`. 
- `make_matrix()` function creates a matrix of consisting only the `"id"` of all the green buttons. This allows easier access to their attributes for subsequent functions within the class by calling the attribute:<br>`self.matrix=[['a11','a12','a13],['a21','a22','a23],['a31','a32','a33],['a41','a42','a43']]`
- `self._keyboard` is an instance of `kivy.event.EventDispatcher` and allows us to bind fuctions to be called when keys are pressed(event) which is defined in the `_on_keyboard_down` function defined later in the class.

#### Transitioning of boxes
```python
    def set_color(self,dt=0): # randomises the starting colors
        
        for i in self.matrix:
            for x in i:
                self.ids[x].color=[0,0,0,1]
            green=random.randint(0,2)
            self.ids[i[green]].color=[0,1,0,.4]
    
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
        self.ids[key].color=[0,1,0,.4]  
```
- `set_color()` makes 1 box of each row green. It makes use of `self.matrix` attribute and the `.color` attribute of `Tap` and `New_Tap` class.
- `color_change()` makes the boxes appear as though they are 'moving' downward. This is done by first making each box follow the color of the box above it in the first `for loop`. The following `for loop` resets the first row all to blanks before randomising only 1 of them to be green.
- The following code must run in this order so box color will be consistent as it moves downward.  


#### Shooting buttons
```python
    def color_check1(self,box_id):        # Check button color when player "shoots"
        if self.ids[box_id].color==[0,1,0,.4]:
            self.color_change()
            self.add_score()
            self.start_timer()
```
- Function takes in a string of the id of the box **directly above** it and checks if box is green when pressed. If `True`, 3 functions will be called: `color_change()` , `add_score()` and `start_timer()`.

#### Key Binding to Shoot 
```python
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

```
- ` _keyboard_closed()` when called would unbind keys and prevent unncessary functions from running when keys are pressed. 
- ` _on_keyboard_down()` allows us to define the functions to call when a specific key is pressed. When a key is pressed, `keycode` arguement returns a tuple of the integer value and string value associated with the key. Since it is more readable to see the string value of key pressed, we use `keycode[1]` to check which key has been pressed. 

#### Dynamic Score Display and Reset
```python
    def add_score(self):  # changes the score label
        self.score +=10
        self.ids.score.text='Score:{:5d}'.format(self.score)
    
    def reset_score(self): # resets the score value to 0 and makes label blank
        self.score=0
        self.ids.score.text=''
```
- When `add_score()` is called, it changes the `self.score` attribute of `GameWindow` class by 10 followed by changeing the text of the score label in the `.kv` file by referring to it through its `id:score`.
- When `reset_score()` is called, it will change `self.score` attribute to 0 and cause score label to display nothing.


#### Dynamic Timer Display and Reset
```python
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
```
- Calling `start_timer()` starts the timer only when the successfully hits a box. This is done by checking if `self.score == 10`. it then proceeds to run the `timer` function once via `Clock.schedule_once` so the time label appears instantly. `Clock.schedule_interval` will keep calling `timer` in 1 second interval subsequently.
- `timer` function changes the display of the timer label via `self.ids.timer.text` before decreasing the `self.time` value by 1. Once `self.time==0`, we will stop calling `timer` via `Clock.unschedule(self.timer)` ,unbind the keyboard via `self._keyboard_closed` and call the `self.end_popup()` function defined within the `GameWindow` class. 
- When `reset_timer()` is called, it will change `self.time` attribute to 30 and cause timer label to display nothing while also stopping the calling of `timer` function. 
### PopUp

#### UI 
```
<End_Popup_Content>:
    Label:
        text:'Game Over'
        font_size: 40
        size_hint: 0.5, 0.3
        pos_hint: {'x':0.25,'top':1}
        
    Label:
        id:score_final
        text:''
        font_size:30
        size_hint: 0.5,0.3
        pos_hint:{'x':0.25,'y':0.6}
        
            
    Label:
        id:comment
        font_size: 30
        text_size: self.size
        size_hint: 1, 0.3
        pos_hint:{'x':0,'y':0.3}
        valign: 'center'
        halign: 'center'
        
    Button:
        id:btn
        text:'Close'
        font_size: 20
        size_hint: 0.3,0.2
        pos_hint: {'x':0.35,'top':0.3}
```
```python
class End_Popup_Content(FloatLayout):
    comments=['Looks like we have a quitter....',
             'Would you like the code to edit your score?',
             'Hellooo are you even trying?',
             'Hmmm, decent score...',
             'Oh, looks like we got a Speedy Mcgee here',
             "Wow you're good, but is this the last level?",
             'LEGENDARY, are you Prof Oka?']
```
- We create a subclass of a `FloatLayout` in kivy and in python called `End_Popup_Content` where we design the layout of what to show in the popup window. In the python code, we gave this subclass an attribute `comments` which is a list of stored stirngs.  
#### Dynamic Popup Content
```python
def end_popup(self): # pop up when time value reaches 0 or when player leaves
        show=End_Popup_Content() 
        show.ids.score_final.text='Final Score:{:5d}'.format(self.score) 
        if self.score==0:
            txt=show.comments[0]
        elif self.score<=400 and self.score>0:
            txt=show.comments[1]
        elif self.score<=900 and self.score>400:
            txt=show.comments[2]
        elif self.score<=1500 and self.score>900:
            txt=show.comments[3]
        elif self.score<=2000 and self.score>1500:
            txt=show.comments[4]
        elif self.score<=2200 and self.score>2000:
            txt=show.comments[5]
        else:
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
```
- Instead of adding a `Popup` widget into our main class, we define it as a function that will display a popup when called.
- The first part of the function creates an instance of our `End_Popup_Content` class called `show`.
- We then change the labels of this instance accordingly: `show.ids.score_final.text` calls the text attribute of the label in `show` and we assign it the `self.score` value.
- Following this, the `if-else` helps us determine the comment to display based on the score the player achieves.The comments are called by indexing the list referenced via `comments` attribute of `show`. It is then assigned to the `comment` label via `show.ids.comment.text=txt`
- Button in `show` is assigned functions for 2 different events:<br>`on_release` which closes the popup window.<br>`on_press` that calls `self.reset` which re-binds the keyboard, resets the time, score and color for the next game while transitioning back to start screen. 
```python
    def reset(self,event): #runs the function in order(for the button in popup)
        self.reset_score()
        self.reset_timer()
        self.set_color()
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.manager.transition.direction = 'right'
        self.manager.current = "start"
```
- We then create an instance of `Popup` widget class called `popup_window` and defined its attributes. `content` attribute is assigned our instance `show`. 
- Finally, we open the popup when the function is called via `popup_window.open()`.

### Start and Instruction Screen
#### UI
- Layout for both use a Floatlayout which can be seen in the `.kv` file. 
- To wrap the text inside the size of the label, we use `text_size: self.size` 
- Size and position of the various widgets are defined by `size_hint` and `pos_hint`. Values are defined as a ratio to the entire screen. `pos_hint` sets position from bottom left of widget.  
- Text for instructions can be found in the `txt` attribute defined in `InstructionWindow` class. 
