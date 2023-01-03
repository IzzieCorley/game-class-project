#Copy & continuation from game4, has NOT YET had ellie and robbies shit put in
#Added Robbie's credits screen,
#12/16


import pgzrun
import math


#Defining properties of canvas
TITLE = "Wizard's Quest"
WIDTH = 1105
HEIGHT = 800



### CREATING THE ACTORS ###

#"Game": Holds the background, and holds an attribute saying what room we're in
game = Actor('title_screen')
#Frame setup has a 20px wide frame to the top, left & right of the game screen, so the actor game sits at 20,20
#(The actual width of the BG part of the screen is 1065 x 630. So the frame is from (20,20) to (1085, 650))
game.topleft = (20,20)
#Defining the list of possible rooms, and an attribute saying what room we're at. Starts at room1
#(We don't ever access from game.rooms_list, it's just here to remind us the names of each room)
###game.rooms_list = ['title', 'room1', 'room2', 'room3']
game.room = 'title'

#We're also storing some attributes in "game" that record whether certain game progression points have happened
#room3_over asks whether the minion encounter has already happened ("False") or has already happened ("True").
game.room3_over = False
#Room3_happening asks whether the encounter is CURRENTLY HAPPENING
game.room3_happening = False
#The game records a part-by-part progression of the room3 encounter in a series of tags (think of it like an index)
#  (It's primarily used to determine what dialogue should be showing up right now.)
#Tag 1 records progression during the first part of the encounter, before any choice is made
game.room3_tag1 = 0
#Tag 2 records progression through the scene after choice 1, if you chose to fight him
game.room3_tag2 = 0
#Tag 3 records progression through the scene after choice 2, if you chose to spare him
game.room3_tag3 = 0
#Tag 4 records progression through the scene after choice 2, if you chose to kill him
game.room3_tag4 = 0
#Tag 5 records progression through the scene after choice 1, if you chose to talk it out with him
game.room3_tag5 = 0
#We also record a string of the outcome of events.
#  Possible values: 'talk', 'fight'(this one will be in-progress but not final), 'spare', 'kill'
game.room3_outcome = ''

#These game tags are for the cutscene that occurs when you interact w the orb in room 4D
#Is the cutscene currently happening? T/F
game.room5_happening = False
#First tag recording what happens in the encounter
game.room5_tag1 = 0
#This tag becomes 1 after the Good Ending encounter is complete
game.room5_tag2 = 0

#These are for the cutscenes in Room 6
game.room6_happening = False
#The tag for the good ending
game.room6_tag1 = 0
#For the bad ending
game.room6_tag2 = 0

#"Border": The black border that goes over everything else
border = Actor('black border')


#ACTORS FOR THE TITLE SCREEN:
#"game_title" is an image with the game's title name
game_title = Actor('title_title')
game_title.midtop = (552, 200)

#"title_enter" is an image saying "press enter"
title_enter = Actor('title_enter')
title_enter.midtop = (552, 350)


#ACTOR FOR THE CREDITS SEQUENCE:
credit_text = Actor('credits', anchor=('center', 'top'))
#Position starts below the top of the screen
credit_text.pos = (552, (HEIGHT+10))
#Stores a boolean to note whether or not it's on the screen
credit_text.onscreen = False


#"Player": Represents the player character
#Anchor means that when we animate the player, the coordinates they move to will correspond to that anchor
player = Actor('player01', anchor=('center', 'bottom'))
#Holds an attribute with all its possible frames
# (0 = forward, 1 = face right, 2 = face left)
player.frames = ['player01', 'player02', 'player03']
#Initial position of player:
player.midbottom = (160,540)
#This boolean lets us know whether the player is allowed to move or not:
player.movement_allowed = False
#This boolean lets us know if the player is moving. Certain interactions cannot be performed mid-motion.
player.moving = False

#"Text Box": The dialogue box
textbox = Actor('textbox_player')
textbox.bottomleft = (71, 798)
#This string stores who the current speaker is. No speaker is represented by 'none'
#(Possible speakers: 'none', 'player', 'minion', 'wizard', 'dragon')
textbox.speaker = 'none'
#This string stores the text that should currently be displaying. Other actors store their own text and will supply it to the
#  text box actor in relevant functions.
#(This list is a 2D list. The outer layer of lists contains all text to be shown at once. The inner layer has an item for each line on the dialogue box.
textbox.text = []
#This number stores the index within textbox.text[i] you're on. It's referenced in draw(), when deciding what text
#  needs to be drawn onto the screen.
textbox.index = 0
#This boolean stores whether the current dialogue being shown can be closed by hitting enter when it's
#  on the last index.
textbox.skippable = True


#Additional textbox actors: The choice boxes
#Drawn when a one-or-the-other choice is being made. Two identical boxes who can be clicked on
choice1 = Actor('choice_box')
choice1.bottomright = (1014, 770)
#The choice boxes store their own text
# (These lists are NOT 2D. They do not index through themselves.)
choice1.text = []
#I'm storing a value for both choice boxes here in C1: Which choice you're on
# It's basically an index letting me know what part of the game you're in
choice1.tag = 0

choice2 = Actor('choice_box')
choice2.bottomright = (706, 770)
choice2.text = []

### ACTORS SPECIFICALLY IN ROOM 0: ###
room0_door = Actor('room0_door')
room0_door.bottomleft = (707, 650)


### ACTORS SPECIFICALLY IN ROOM 1: ###

#The door that connects to Room 0
room1_door1 = Actor('room1_door1')
room1_door1.topleft = (20, 197)

#Door that, when open, can be clicked to move to the next room
room1_door2 = Actor('room1_door_closed')
room1_door2.topleft = (914, 153)
#Boolean asks if the door is open or closed (open = can progress)
room1_door2.closed = True
#Storing its frames
room1_door2.images = ["room1_door_closed", "room1_door_open"]
#Room 1 door 2 has text associated with it, that displays when you click it while it's closed.
# This list here is stored to be passed to textbox.text when you click on the door.
room1_door2.text = [["The door is closed shut...", "Maybe this is a puzzle?", ""]]

#Now, the 3 dragon panels on the wall
#All of the attributes that involve all three are stored in dragon1
room1_dragon1 = Actor('room1_dragon1')
room1_dragon1.topleft = (171, 196)
#Storing the two images for dragon1
room1_dragon1.images = ['room1_dragon1', 'room1_dragon1_2']
#Storing which dragons have been clicked last
room1_dragon1.clicked = []
#Storing whether the puzzle is clickable (it will be clickable only when it is not flashing and not already solved)
room1_dragon1.clickable = False
#Storing whether the puzzle has been solved yet
# (If it has, you can't click the dragons anymore, they stay in place)
room1_dragon1.solved = False

room1_dragon2 = Actor('room1_dragon2')
room1_dragon2.topleft = (330, 160)
room1_dragon2.images = ['room1_dragon2', 'room1_dragon2_2']

room1_dragon3 = Actor('room1_dragon3')
room1_dragon3.topleft = (482, 199)
room1_dragon3.images = ['room1_dragon3', 'room1_dragon3_2']


### ACTORS SPECIFICALLY IN ROOM 2: ###

#The door that takes you back to room 1
room2_door1 = Actor("room2_door1")
room2_door1.topright = (177, 200)

#The door that takes you to room 3
room2_door2 = Actor("room2_door2")
room2_door2.bottomright = (1042, 550)

#Tablet
room2_tablet = Actor("room2_tablet")
room2_tablet.bottomleft = (596, 355)
#The text it displays
room2_tablet.text = [["It's a mural...","That must be the evil dragon who lives","in this dungeon."],
                     ["The way she's depicted, it almost looks like she's","protecting those structures.","..."],
                     ["It's kind of sad, actually. I guess the dragon","has been fooling her minions into thinking she's good","using propaganda."]]


### ACTORS SPECIFICALLY IN ROOM 3: ###

#The door connecting Room 3 to Room 2
room3_door = Actor('room3_door')
room3_door.bottomright = (206, 259)

room3_bridge = Actor('room3_bridge')
room3_bridge.topright= (1085, 459)

#The minion sprite
#Anchor means that when he's moved around, the destination x,y will be the bottom left corner of his image.
minion = Actor('minion1',  anchor=('left', 'bottom'))
#His initial position is slightly offscreen, on the bridge
minion.bottomleft = (1106, 520)


### ACTORS SPECIFICALLY IN ROOM 4: ###

#The bridge that moves from room 3 to room 4
room4_bridge = Actor('room4_bridge')
room4_bridge.bottomleft = (20, 550)

#The fountain that has the key and stuff
room4_fountain = Actor('room4_fountain')
room4_fountain.midbottom = (432, 429)
#We're going to store whether or not the player has brought the Obsidian Key to the fountain here.
room4_fountain.keyget = False

#The door moving from room 4 to room 5
room4_door = Actor('room4_door')
room4_door.bottomleft = (759, 293)


### ACTORS SPECIFICALLY IN ROOM 5: ###

#The door connecting to the Boss Room
room5_door = Actor('room5_door_closed')
room5_door.midtop = (534, 33)

#The pathway connecting to Room 4
room5_pathway = Actor('room5_pathway')
room5_pathway.bottomleft = (419, 650)

#The tunnels connecting to the Room 5 Side Rooms:
room5_tunnel1 = Actor('room5_tunnel')
room5_tunnel1.bottomleft = (79, 293)
#In room5_tunnel1, we're going to store a specific boolean that lets the game know which tunnel you went into.
#  This will be recalled when you exit room5A-C and come back to room 5, so that you're in the right place.
room5_tunnel1.coords = (0,0)
#For the same reason, we store the letter of what room you've last entered.
room5_tunnel1.letter = 'a'

room5_tunnel2 = Actor('room5_tunnel')
room5_tunnel2.bottomleft = (235, 292)

room5_tunnel3 = Actor('room5_tunnel')
room5_tunnel3.bottomleft = (734, 287)

#Tunnel 4 leads to the Secret Room that's only accessible if you solve the Secret Puzzle
#It won't automatically appear, you have to place the Stone Key into the Room 4 Fountain to do so
room5_tunnel4 = Actor('room5_tunnel')
room5_tunnel4.bottomright = (1011, 283)

#The tablet that can be interacted with to display the text explaining the puzzle
#  that opens the Room 5 Door
room5_tablet = Actor('room5_tablet')
room5_tablet.bottomleft = (93, 573)

### ACTORS SPECIFICALLY IN ROOMS 5A-C: ###

#These three actors are the same actors in every room.
#The room transition functions tell them what images to take on,
#  and on_mouse_down will call different interaction functions depending on
#  what the value of game.room is.

#The tablet depicting a specific piece of art.
#Clicking it is part of the secret puzzle.
r5a_tablet = Actor('5a_tablet')
r5a_tablet.topleft = (373, 33)
#We'll store the list of tablets clicked in the order they were clicked in here:
r5a_tablet.clicked = []
#We'll also store a boolean saying whether or not the secret puzzle has been solved.
r5a_tablet.solved = False

#The button clickable as part of the boss room puzzle
r5a_button = Actor('5a_button')
r5a_button.topleft = (454, 292)
#Storing the list of buttons that have been clicked, in the order they were clicked in:
r5a_button.clicked = []
#Storing a boolean of whether the puzzle involving buttons (the boss room door puzzle) has been solved
r5a_button.solved = False

#The pathway that takes you back to room 5
r5a_pathway = Actor('5a_pathway')
r5a_pathway.bottomleft = (442, 650)



### ACTORS SPECIFICALLY IN ROOM 5D: ###

#The orb that you destroy 
r5d_orb = Actor('5d_orb')
r5d_orb.topleft = (471, 213)
#A boolean asking if the orb has been broken
r5d_orb.destroyed = False

#The pathway that leads back to Room 5
r5d_pathway = Actor('5d_pathway')
r5d_pathway.bottomleft = (439, 650)

#The Wizard!
wizard = Actor('wizard1', anchor=('center', 'bottom'))
wizard.pos = (411, 296)
wizard.appear = False

### ACTORS SPECIFICALLY IN ROOM 6: ###

room6_dragon = Actor('room6_dragon_sick')
room6_dragon.bottomleft = (70, 628)


########################################################################
### DRAWING ON THE SCREEN ###

def draw():
    #The bg ("game") always gets drawn, and it's always the lowest thing, so it can be put outside the if loops.
    game.draw()
    #HERE, we're deciding what objects within the gameplay screen to draw.
    if game.room == 'title':
        game_title.draw()
        title_enter.draw()
        
    elif game.room == 'room0':
        room0_door.draw()
        
        player.draw()
    
    elif game.room == 'room1':
        room1_dragon1.draw()
        room1_dragon2.draw()
        room1_dragon3.draw()
        room1_door2.draw()
        
        player.draw()
        
    elif game.room == 'room2':
        room2_door1.draw()
        room2_door2.draw()
        room2_tablet.draw()
        
        player.draw()
        
    elif game.room == 'room3':
        room3_door.draw()
        room3_bridge.draw()
        
        player.draw()
        
        #The minion is drawn if game.room3_happening = True, AKA, if the room 3 minion encounter is currently happening
        if game.room3_happening or game.room3_outcome == 'spare':
            minion.draw()

        
    elif game.room == 'room4':
        room4_bridge.draw()
        room4_fountain.draw()
        room4_door.draw()
        
        player.draw()
        
    elif game.room == 'room5':
        room5_door.draw()
        room5_tunnel1.draw()
        room5_tunnel2.draw()
        room5_tunnel3.draw()
        room5_tablet.draw()
        room5_pathway.draw()
        
        #Tunnel4 gets drawn IF certain conditions are met
        if room4_fountain.keyget:
            room5_tunnel4.draw()
        
        player.draw()
      
    #Rooms 5A-C have the same actors
    elif game.room == 'room5a' or game.room == 'room5b' or game.room == 'room5c':
        r5a_tablet.draw()
        r5a_button.draw()
        r5a_pathway.draw()
        player.draw()
        
    elif game.room == 'room5d':
        r5d_orb.draw()
        r5d_pathway.draw()
        player.draw()
        
        if wizard.appear == True:
            wizard.draw()
        
    elif game.room == 'room6':
        room6_dragon.draw()
        player.draw()
        
        if wizard.appear == True:
            wizard.draw()
        
    #Now we draw the border over everything else
    #(There's no border in the boss room so we check to ensure it's not boss room)
    if not game.room == 'room6':
        border.draw()
    
    #We check if the game is credits here, so that it gets drawn over the border.
    if game.room == 'credits':
        credit_text.draw()
    
    #NOW, HERE, we decide whether the textbox should be drawn, and draw the text.
    if not textbox.speaker == 'none':
        #The exact text box functionality will depend on whether we're using a text box that has a speaker icon on it.
        #We'll check to see if it's a icon-having textbox:
        if textbox.speaker == 'player' or textbox.speaker == 'minion' or textbox.speaker == 'wizard' or textbox.speaker == 'dragon':
            #First we make sure it's the right image for the speaker
            if textbox.speaker == 'player':
                textbox.image = 'textbox_player'
            elif textbox.speaker == 'minion':
                textbox.image = 'textbox_minion'
            elif textbox.speaker == 'wizard':
                textbox.image = 'textbox_wizard'
            elif textbox.speaker == 'dragon':
                textbox.image = 'textbox_dragon'
                
            #Now we draw the stuff
            textbox.draw()
            
            #Now we draw the text itself (in the right position)
            screen.draw.text(textbox.text[textbox.index][0], topleft=(248, 649), color="black", fontsize = 40)
            screen.draw.text(textbox.text[textbox.index][1], topleft=(248, 694), color="black", fontsize = 40)
            screen.draw.text(textbox.text[textbox.index][2], topleft=(248, 739), color="black", fontsize = 40)
        
        #This is what happens if the textbox is displaying a choice right now
        elif textbox.speaker == 'choice':
            #Make the right image
            textbox.image = 'textbox1_blank'
            
            #Draw the text box
            textbox.draw()
            #Now we draw the text itself
            #NOTE that for a choice, textbox.text is a ONE DIMENSIONAL LIST not a 2D list.
            screen.draw.text(textbox.text[0], topleft=(111, 649), color="black", fontsize = 40)
            screen.draw.text(textbox.text[1], topleft=(111, 694), color="black", fontsize = 40)
            screen.draw.text(textbox.text[2], topleft=(111, 739), color="black", fontsize = 40)
            
            #NOW we draw the two Y/N choice windows.
            choice1.draw()
            choice2.draw()
            
            #And now we draw the text on those two windows
            #Text for choice1:
            screen.draw.text(choice1.text[0], topleft=(746, 670), color='black', fontsize = 40)
            
            #Text for choice2:
            screen.draw.text(choice2.text[0], topleft=(438, 670), color='black', fontsize = 40)
            
        
        
        #This happens if the textbox does NOT have a icon on the right, and isn't a choice branch (This will run if speaker == 'other')
        else:
            textbox.image = 'textbox_other'
                
            #Now we draw things
            textbox.draw()
            
            screen.draw.text(textbox.text[textbox.index][0], topleft=(111, 649), color="black", fontsize = 40)
            screen.draw.text(textbox.text[textbox.index][1], topleft=(111, 694), color="black", fontsize = 40)
            screen.draw.text(textbox.text[textbox.index][2], topleft=(111, 739), color="black", fontsize = 40)
    
########################################################################
### UPDATE FUNCTION ###
            
#Called 60 times every second. Specifically utilized during the credits sequence to make the credits text move.
#DT is the amount of miliseconds since the function was last called.
def update(dt):
    if game.room == 'credits':
        #Move the text's Y
        credit_text.y -= dt * 60
        
        #Check if the text has moved offscreen
        if check_credits():
            #Call the function that resets you back to the menu
            initialize_everything()
    

########################################################################
### MOVEMENT FUNCTIONS ###
#Contains the room-ubiquitous move_player function as well as its helper functions.

#Helper function to calculate how long it will take the player to move to a certain point from their point, based on movement speed
def calc_time(x1, y1, x2, y2):
    distance = int(math.sqrt(((x1 - x2)**2)+((y1 - y2)**2)))
    time_sec = distance/350
    return time_sec

#Helper function that just calculates distance between two points
#Function that calculates distance between two X,Y points, takes x1, y1, x2, y2, returns an int
def calc_distance(x1, y1, x2, y2):
    distance = int(math.sqrt(((x1 - x2)**2)+((y1 - y2)**2)))
    return distance

#Called after player moves, returns them to front-facing frame
def stop_player_move():
    player.image = player.frames[0]
    player.moving = False

#Takes a tuple representing the (x,y) of where the player will end up. (Has already been processed to avoid going out of range)        
def move_player(destination):
    #Pull out each value in destination:
    x_val = destination[0]
    y_val = destination[1]
    
    #First, let's figure out how long the animation will take,
    #  depending on the distance traveled.
    #First, calculating the distance between current position & destination:
    distance = calc_distance(x_val, y_val, player.midbottom[0], player.midbottom[1])
    #Next, calculating the amount of seconds I'd like that to take, using an arbitrary formula
    time_sec = distance/350
    
    #Before we animate the player, we should check to make sure we aren't about
    #  to move the player to the same place. If distance=0, an error will occur.
    if not distance==0:
        #NOW we animate the player.
        #First let's make the player point left or right for their movement
        if player.midbottom[0] > x_val:
            player.image = player.frames[2]
        else:
            player.image = player.frames[1]
        
        #We let the game know the player is moving
        player.moving = True
        
        #Finally, animating the movement:
        animate(player, duration=time_sec, pos=(x_val, y_val))
        #And schedule to make the player face forward when time is up.
        #Schedule_unique avoids possibility of player facing forward during a second
        #  consecutive animation.
        clock.schedule_unique(stop_player_move, time_sec)


#This function is LIKE move_player, except it moves the minion.
def move_minion(destination):
    #Pull out each value in destination:
    x_val = destination[0]
    y_val = destination[1]
    
    #First, let's figure out how long the animation will take,
    #  depending on the distance traveled.
    #First, calculating the distance between current position & destination:
    distance = calc_distance(x_val, y_val, minion.pos[0], minion.pos[1])
    #Next, calculating the amount of seconds I'd like that to take, using an arbitrary formula
    time_sec = distance/300
    #NOTE!!!! The minion walks slower. His speed is distance/325 instead of distance/350.
    
    if not distance == 0:
        #Finally, animating the movement:
        animate(minion, duration=time_sec, pos=(x_val, y_val))

########################################################################
### INTRO CUTSCENE FUNCTIONS ###

#Called when the player hits enter at title. Begins the cutscene sequence
def intro_cutscene1():
    #Tell the game what it is right now
    game.room = 'intro_cutscene'
    game.image = 'intro_cutscene'
    #Load up all the text
    textbox.text = [["Your beloved pet, Scruffy, is terminally ill and you have","Exhausted all possible options, but you've heard that","there is a wizard who can heal him."],
                    ["The Wizard agrees to heal your pet, but he cannot do it", "without an important reagent. He needs", "the SOUL of an evil dragon that lives in a dungeon nearby."],
                    ["The dungeon is perilous, full of puzzle traps, and the", "dragon's dangerous minions. The wizard has granted you", "magical armor suited to protect you against them."],
                    ["You must enter the dungeon, slay the dragon, and", "take her soul.", ""],
                    ["If you complete these tasks, the Wizard", "will be able to heal your pet, and promises you", "happiness for the rest of your days."]]

    textbox.index = 0
    player.movement_allowed = False
    textbox.skippable = True
    textbox.speaker = 'intro_cutscene'



########################################################################
### ROOM 0 INTERACTION FUNCTIONS ###

#This function is called in game.room=='title', and will switch everything to room 0
def game_start():
    #Editing all the game state's files 
    game.room = 'room0'
    game.image = 'room0'
    #Move the player so they're in the beginning of the room
    player.midbottom = (153, 604)
    

    #Now we're gonna open the dialogue for the beginning of the game.
    #Movement allowed is false, and skippable is true, which means you can close this dialogue by pressing enter after the
    #  last index, but can't close it by moving around/interacting with things.
    textbox.text = [["All right... Here we go.","",""],["I'm gonna do whatever it takes to get you better, Scruffy.","",""]]
    textbox.index = 0
    player.movement_allowed = False
    textbox.skippable = True
    textbox.speaker = 'player'
    
    #(After the dialogue is cycled through, player.movement_allowed will be set to True)

    
#This function is called when the player clicks room0_door
def r0_door_interact():
    move_player((930, 560))
    clock.schedule_unique(r0_to_r1, calc_time(player.pos[0], player.pos[1], 930, 560))
    
#Called by the function for clicking r0_door1, switches everything to room 1
def r0_to_r1():
    #Tell the game it's in room 1
    game.room = 'room1'
    #Make the room 1 image appear
    game.image = "room1"
    #Move player to correct location for r1
    player.midbottom = (102, 537)
    #If the dragon puzzle hasn't been solved, we'll schedule the dragon puzzle to flash again
    # when the player re-enters room 1
    if not room1_dragon1.solved:
        player.movement_allowed = False
        clock.schedule_unique(dragons_animate, 0.3)
        
def move_room0(pos):
    #Unschedule this in case it's supposed to have been happening
    clock.unschedule(r0_to_r1)
    
    x = pos[0]
    y = pos[1]
    
    #Range: (89, 576) to (939, 646)
    #Check things out of range
    if x < 89:
        x = 89
    elif x > 939:
        x = 939
        
    if y < 576:
        y = 576
    elif y > 646:
        y = 646
    
    #Now we move
    destination = (x, y)
    move_player(destination)

########################################################################
### ROOM 1 INTERACTION FUNCTIONS ###

#This function is called when the player clicks room1_door1. Moves you back to room 0
def r1_door1_interact():
    move_player((71, 509))
    clock.schedule_unique(r1_to_r0, calc_time(player.pos[0], player.pos[1], 71, 509))

#This is called by r1_door1_interact to switch the game's state
def r1_to_r0():
    #Tell the game it's in room 0
    game.room = 'room0'
    #Make the room 0 image appear
    game.image = "room0"
    #Move player to correct location for r0
    player.midbottom = (930, 560)

#This function is called when the player clicks room1_door2
def r1_door2_interact():
    #If the door is closed we're gonna call up some dialogue about it. This will only happen if the player is not moving. 
    if room1_door2.closed and not player.moving:
        #We fill the textbox with relevant data.
        #Put the right text into the attribute that displays it 
        textbox.text = room1_door2.text
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'player'
        #We do NOT disable player.movement_allowed for this dialogue
        textbox.skippable = True
        
    #This will only happen if door 2 is open
    elif not room1_door2.closed:
        #If the door is open we'll go to room 2
        #We'll call move_player so they move to the door, then schedule the r1-r2 transition
        #  for the time it takes to get there.
        move_player((968, 480))
        #(968, 480) is the bottom center of the doorway
        clock.schedule_unique(r1_to_r2, calc_time(player.pos[0], player.pos[1], 968, 480))

#This function will initiate the transition to room 2, by altering necessary variables.
#It's called when you click on door2 when it's open, after the player has moved to the door.
def r1_to_r2():
    #Tell the game it's in room 2
    game.room = 'room2'
    #Make the room 2 image appear
    game.image = "room2"
    #Move player to correct location for r2
    player.midbottom = (172, 492)
        

### DRAGON ANIMATION FUNCTIONS. ###
#This chain reaction starts with room1_dragons_animate, called by room1_dragon_clicked

#This is the final call in the dragon_animation. It will set things back to normal
def dragon_animation_4():
    room1_dragon1.image = room1_dragon1.images[0]
    
    #These two lines set things back to normal
    room1_dragon1.clickable = True
    player.movement_allowed = True
    
def dragon_animation_3():
    room1_dragon2.image = room1_dragon2.images[0]
    room1_dragon1.image = room1_dragon1.images[1]
    # sounds.half_sec_silence.play()
    #Now for the next part
    clock.schedule_unique(dragon_animation_4, 0.5)


def dragon_animation_2():
    room1_dragon3.image = room1_dragon3.images[0]
    room1_dragon2.image = room1_dragon2.images[1]
    # sounds.half_sec_silence.play()
    #Now for the next part
    clock.schedule_unique(dragon_animation_3, 0.5)


#This is called within dragons_animate(), and is the first of these to be called
def dragon_animation_1():
    room1_dragon1.image = room1_dragon1.images[0]
    room1_dragon3.image = room1_dragon3.images[1]
    # sounds.half_sec_silence.play()
    #Now for the next part
    clock.schedule_unique(dragon_animation_2, 0.5)
    
#This is the first in the chain, and is called first.
def dragons_animate():
    #First let's set some important booleans that will avoid bugs/gameplay issues
    room1_dragon1.clickable = False
    player.movement_allowed = False
    #Now let's go in order. We'll start the chain within this function
    room1_dragon1.image = room1_dragon1.images[1]
    # sounds.half_sec_silence.play()
    #Now we call the next function to do this
    #The delay is set to 0.5 because the sound effect will last that long
    clock.schedule_unique(dragon_animation_1, 0.5)
    
### END OF DRAGON ANIMATION SECTION ###

    
#Room 1 interaction functions, continued:

#This function is called when the player clicks any of the dragon panels, if the puzzle is clickable.
#It takes the tuple of the player's click location, so it can tell which tile was clicked.
def room1_dragon_clicked(pos):
    #First we're gonna add to the "clicked" list included in the dragon 1 actor, so we can store what order we clicked the dragons
    if room1_dragon1.collidepoint(pos):
        room1_dragon1.clicked.append("1")
        
    elif room1_dragon2.collidepoint(pos):
        room1_dragon1.clicked.append("2")
        
    elif room1_dragon3.collidepoint(pos):
        room1_dragon1.clicked.append("3")
        
    #Now let's check to see if the player has clicked four dragons
    #If so, we need to decide whether it's the right order.
    if len(room1_dragon1.clicked) == 4:
        #Is it the right order?
        if room1_dragon1.clicked == ["1", "3", "2", "1"]:
            print("yay")
            #sounds.puzzle.play()
            #To-do: Make all 3 tiles light up at once, maybe even a "ding" kinda sound effect?
            #  Something that is recognizably a sign of "you win" 
            room1_dragon1.clicked = []
            room1_dragon1.clickable = False
            #We also open up Door 2
            room1_door2.closed = False
            room1_door2.image = room1_door2.images[1]
            
        #If it wasn't the right order let's clear the list so the player can try again
        else:
            print("try again")
            #To-do: Replace this print statement with something like a 'wuh-woh' sound effect, maybe the 4 tiles flash red or smth
            room1_dragon1.clicked = []
            room1_dragon1.clickable = False
            player.movement_allowed = False
            #Call dragons_animate to give the player a refresher on the correct pattern
            clock.schedule_unique(dragons_animate, 0.3)
           

#This function is called by on_mouse_down when the click isn't interacting with an actor.
#It determines what coordinates the player should move to, and calls the move_player with those coords.
def move_room1(pos):
    #Before we do anything else, we're going to unschedule room-transitions, to avoid a bug
    #  where you schedule moving to room 2, but move away halfway through, but still switch to room 2 (without ever reaching the door)
    clock.unschedule(r1_to_r2)
    clock.unschedule(r1_to_r0)
    
    #There's two possible ranges of x,y where the player can move to.
    #  The big rectangular space of the floor, (90, 450) to (1000, 650); and the little bit at the top, (660, 405) to (915, 450)
    #Let's see if pos is within those ranges.
    #We'll pull out the x and y of pos for easy usage
    x = pos[0]
    y = pos[1]
    
    #To determine what the acceptable movement range is, we need to see where the player is at.
    
    #If the player is on the main part of the floor, not the upper niche:
    if player.pos[1] >= 450:
        #Now let's see if the user clicked to move to the niche area.
        if y < 450 and 660 <= x <= 915:
            #You can't move to the upper niche if you're near it in Y but far from it in X, it'll cause a wall-clipping,
                #so we need to check their X too.
            #This means you're UNABLE to move to the niche:
            if player.pos[0] < 450 and player.pos[1] < 460:
                #The movement range is (90-1000, 450-650)
                if x < 90:
                    x = 90
                elif x > 1000:
                    x = 1000
                if y < 450:
                    y = 450
                elif y > 650:
                    y = 650
            #This means you CAN move to the niche:
            else:
                #X movement range is 660-915 but we already checked that the user's click is within that range
                #We already checked that Y is less than 450, but let's just make sure it's not less than 405
                if y < 405:
                    y = 405
                    
        #Now functionality for if they are NOT clicking on the niche:    
        else:
            #This branch means you're not in the niche and not clicking on the niche. Simple functionality.
            #y range is 450-650
            if y < 450:
                y = 450
            elif y > 650:
                y = 650
            #x range is 90-1000
            if x < 90:
                x = 90
            elif x > 1000:
                x = 1000
        
    #This branch checks the movement range if the player is currently located within the niche
    else:
        #The most important restriction is that they cannot move to an X that is too low because it will clip the wall.
        #Let's check the click's X to see if you're making a wall-clipping move:
        if x < 450 and y >= 450:
            #We cut the X off at the minimum
            x = 450
            #We alter the Y based on the general >650 rule for the very bottom of the floor
            if y > 650:
                y = 650
                
        #Movement restrictions for moving about within the niche:
        elif y < 450:
            #X range is 660-915
            if x < 660:
                x = 660
            elif x > 915:
                x = 915
            if y < 405:
                y = 405
                
        #Movement restrictions for moving to a non-wall-clipping part of the main floor; x between 450-1000, y between 450-650
        else:
            if x < 450:
                x = 450
            elif x > 1000:
                x = 1000
            #(We know y isn't less than 450)
            if y > 650:
                y = 650

    #NOW FINALLY we can call move_player.
    # We make a tuple of x,y because move_player takes the pos as a tuple.
    destination = (x,y)
    move_player(destination)
        
        
        
########################################################################
### ROOM 2 INTERACTION FUNCTIONS ###

#This door moves back to room 1. Function called when player clicks it.
def r2_door1_interact():
    #We'll call move_player so they move to the door, then schedule the r1-r2 transition
    #  for the time it takes to get there.
    #(131, 473) is the bottom center of the doorway
    move_player((131, 473))
    clock.schedule_unique(r2_to_r1, calc_time(player.pos[0], player.pos[1], 131, 473))
    
    #This also needs to be unscheduled in case it's going on
    clock.unschedule(r2_tablet_interact)
     
#Called by r2_door1_interact, switches appropriate variables back to room 1
def r2_to_r1():
    #Tell the game it's in room 1
    game.room = 'room1'
    #Make the room 1 image appear
    game.image = "room1"
    #Move player to correct location for r1 door
    player.midbottom = (968, 480)
    
#This displays the text that shows when you interact with the tablet. It's scheduled for the amount of time you need
#  to move there, in on_mouse_down().
def r2_tablet_interact():
    #We fill the textbox with relevant data.
    #Put the right text into the attribute that displays it 
    textbox.text = room2_tablet.text
    #Reset the index to 0
    textbox.index = 0
    textbox.speaker = 'player'
    #We do NOT disable player.movement_allowed for this dialogue
    textbox.skippable = True


#This door moves to room 3. Called when player clicks it.
def r2_door2_interact():
    #We'll call move_player so they move to the door, then schedule the r1-r2 transition
    #  for the time it takes to get there.
    move_player((962, 473))
    clock.schedule_unique(r2_to_r3, calc_time(player.pos[0], player.pos[1], 962, 473))
    
    #This also needs to be unscheduled in case it's going on
    clock.unschedule(r2_tablet_interact)
     
#Called by r2_door1_interact, switches appropriate variables back to room 1
def r2_to_r3():
    #Tell the game it's in room 3
    game.room = 'room3'
    #Make the room 3 image appear
    game.image = "room3"
    #Move player to correct location for r3 door
    player.midbottom = (136, 285)
    
    
#This function is called when you click on the ground in Room 2
#It decides what position you'll move to and then calls move_player.
#This one is pretty simple, because the range of movement in room 2 is a plain square.
def move_room2(pos):
    #First unschedule any potential room transitions
    clock.unschedule(r2_to_r1)
    clock.unschedule(r2_to_r3)
    #This also needs to be unscheduled in case it's going on
    clock.unschedule(r2_tablet_interact)
    
    x = pos[0]
    y = pos[1]
    
    #Check if X is out of range?
    if x > 875:
        x = 875
    elif x < 210:
        x = 210
        
    #Check if Y is out of range?
    if y > 585:
        y = 585
    elif y < 390:
        y = 390
    
    # We make a tuple of x,y because move_player takes the pos as a tuple.
    destination = (x,y)
    #Now we move.
    move_player(destination)




########################################################################
### ROOM 3 INTERACTION FUNCTIONS ###
  
'''  
#TO DO FOR ROOM 3:
   -What will we do for the minion after the encounter? My initial thoughts are that he stays there if you spare or talk to him, and that you can interact with him
    if he's still there. We'll need an interaction function called in on_mouse_down and a draw function in draw() that both are contingent on game.room3_outcome being
    'talk' or 'spare'.
    
   -I was thinking maybe for the final version, the railing on the bridge that's closer to the "camera"
    should be its own actor, layered over the player. (AKA put after player.draw() in the draw() function.)
'''
#
def unschedule3():
    clock.unschedule(r3_to_r2)
    clock.unschedule(r3_to_r4)

#This door moves back to room 2. Function called when player clicks it.
def r3_door_interact():
    #We'll call move_player so they move to the door, then schedule the transition
    #  for the time it takes to get there.
    move_player((136, 256))
    clock.schedule_unique(r3_to_r2, calc_time(player.pos[0], player.pos[1], 136, 256))
    
#Called by r3_door_interact, switches appropriate variables back to room 2
def r3_to_r2():
    #Tell the game it's in room 2
    game.room = 'room2'
    #Make the room 2 image appear
    game.image = "room2"
    #Move player to correct location for r2 door
    player.midbottom = (930, 473)
        
#This is called when the player clicks the r3 bridge. It will transition the player to Room 4
def r3_bridge_interact():
    #We'll call move_player so they move to the door, then schedule the transition
    #  for the time it takes to get there.
    move_player((1105, 534))
    clock.schedule_unique(r3_to_r4, calc_time(player.pos[0], player.pos[1], 1105, 534))
    
#Called by r3_bridge_interact, switches appropriate variables to room 4
def r3_to_r4():
    #Tell the game it's the new room
    game.room = 'room4'
    #Make the right room image appear
    game.image = "room4"
    #Move player to correct location for the new room's entry
    player.midbottom = (85, 502)
     
### MINION ENCOUNTER CUTSCENE SECTION ###
#Everything under this section has the minion encounter    

### MINION ENCOUNTER TAG 5 SECTION ###
#This has r3_cutscene 13- , and runs from Choice 1, if you decided to talk with the minion, until
# the end of the encounter.
def r3_cutscene13():
    if game.room3_tag5 == 1:
        #Set the tag to the next index
        game.room3_tag5 = 2
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["I don't want to fight you.", "", ""],
                        ["I'm sorry if I'm intruding upon your home, but I need", "to retrieve the soul of the dragon", "who lives here, in order to complete a spell."],
                        ["It's the only way I can save my companion.", "", ""]]
        textbox.speaker = 'player'
        textbox.skippable = True
        
    elif game.room3_tag5 == 2:
        #Set the tag to the next index
        game.room3_tag5 = 3
        #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["Not happening, bub.", "It's my sworn duty to protect her.", ""],
                        ["Leave now, or things're gonna get messy.", "", ""]]
        textbox.speaker = 'minion'
    
    elif game.room3_tag5 == 3:
        #Set the tag to the next index
        game.room3_tag5 = 4
        #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["Please, just let me go in peace.", "I have no quarrel with you.", ""],
                        ["It's not your fault that", "you've been fooled into servitude", "by an evil dragon."]]
        textbox.speaker = 'player'
    
    elif game.room3_tag5 == 4:
        #Set the tag to the next index
        game.room3_tag5 = 5
        #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["Fooled? Evil?", "", ""],
                        ["Maybe you're the one who's been fooled,", "because The Queen AIN'T evil.", ""],
                        ["Sure, she's been acting", "a little erratic lately...", "But that's only since she got sick!"]]
        textbox.speaker = 'minion'
    
    elif game.room3_tag5 == 5:
        #Set the tag to the next index
        game.room3_tag5 = 6
        #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["Um... What do you mean, got sick?", "", ""]]
        textbox.speaker = 'player'
 
    elif game.room3_tag5 == 6:
        #Set the tag to the next index
        game.room3_tag5 = 7
        #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["Yeah, she's been sick for a while now.", "It's been making her crazy.", ""],
                        ["It's gotten so bad, us minions even had to lock her up.", "And her MAGIC ORB too.", ""],
                        ["She--poor thing--she, she kept trying to use it.", "And every time, it would end up going wrong.", "Like she couldn't control it anymore."],
                        ["We had to separate her from it.", "We locked them up in separate rooms so she--", ""],
                        ["Crap.", "", ""],
                        ["I've said too much. Forget it.", "", ""]]
        textbox.speaker = 'minion'
        
    elif game.room3_tag5 == 7:
        #Set the tag to the next index
        game.room3_tag5 = 8
        #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["No, wait, please!", "", ""],
                        ["I had no idea about any of that.", "", ""],
                        ["All I was told was that she was evil, and dangerous...", "", ""]]
        textbox.speaker = 'player'
        
    elif game.room3_tag5 == 8:
        #Set the tag to the next index
        game.room3_tag5 = 9
        #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["Well, you can't believe everything you hear!", "", ""]]
        textbox.speaker = 'minion'
        
    elif game.room3_tag5 == 9:
        #Set the tag to the next index
        game.room3_tag5 = 10
        #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["(I don't know WHAT to believe anymore...)", "", ""],
                        ["This- This is a lot to process.", "", ""],
                        ["If your queen is sick, why lock her up?", "Surely you could just use magic to cure her disease.", ""]]
        textbox.speaker = 'player'
    
    elif game.room3_tag5 == 10:
        #Set the tag to the next index
        game.room3_tag5 = 11
        #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["Nothing me and the boys have tried has done any good.", "", ""],
                        ["Believe me, human. Me and the boys have tried everything", "we were capable of.", "None of it did any good."],
                        ["We think it'd probably require way more powerful magic.", "Something much stronger than what any of us", "minions can do."]]
        textbox.speaker = 'minion'
        
    elif game.room3_tag5 == 11:
        #Set the tag to the next index
        game.room3_tag5 = 12
        #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [['What about that "magic orb" you were talking about?', 'Maybe it has something to do with that?', '']]
        textbox.speaker = 'player'
                
    elif game.room3_tag5 == 12:
        #Set the tag to the next index
        game.room3_tag5 = 13
        #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["Hmm...", "", ""], ["You might be onto something with that.", "", ""],
                        ["If you're smart enough to figure out how to", "find her magic orb, then you're probably", "smart enough to use magic, right?"],
                        ["That amulet around your neck certainly looks magic.", "", ""],
                        ["Tell you what, I'll let you in on what I know", "about the ORB...", ""],
                        ["I don't know exactly where the other minions", "hid the orb. I wasn't one of the ones who", "sealed it away."],
                        ["But I think it has something to", "with the next room,", "and a very familiar pattern..."]]
        textbox.speaker = 'minion'
        
    elif game.room3_tag5 == 13:
        #Set the tag to the next index
        game.room3_tag5 = 14
        #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["Thank you, thank you!", "", ""],
                        ["I'll do my best.", "", ""]]
        textbox.speaker = 'player'
        
    elif game.room3_tag5 == 14:
        #Set the tag to the next index
        game.room3_tag5 = 15
                #Reset the index to 0
        textbox.index = 0
        #Put the right text into the attribute that displays it 
        textbox.text = [["Just promise me one thing.", "", ""],
                        ["Whatever happens, don't you hurt my Queen.", "", ""],
                        ["...", "I'm counting on you.", ""]]
        textbox.speaker = 'minion'
    
    elif game.room3_tag5 == 15:
        #This one ends the encounter
        game.room3_tag5 = 16
        
        player.movement_allowed = True
        #These booleans attributed to Game lets us know the minion encounter is over
        game.room3_happening = False
        game.room3_over = True
        textbox.speaker = 'none'
        



### MINION ENCOUNTER TAG 4 SECTION ###
#This has r3_cutscene10-12, and runs from Choice 2, if you decide to kill the minion, until the end
    # of the encounter.
    
#Shows player dialogue right after minion dies. Tag4=3 at the start of this function. Ends the encounter.
def r3_cutscene12():
    if game.room3_tag4 == 3:
        #Set the tag to the next index
        game.room3_tag4 = 4
        #Put the right text into the attribute that displays it 
        textbox.text = [["What the...?", "", ""], ["Nobody told me that THAT could happen...", "", ""]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'player'
        textbox.skippable = True
        
    elif game.room3_tag4 == 4:
        #This one ends the encounter.
        game.room3_tag4 = 5
        
        player.movement_allowed = True
        #These booleans attributed to Game lets us know the minion encounter is over
        game.room3_happening = False
        game.room3_over = True
        textbox.speaker = 'none'
    
#This begins the sequence of the minion dying and the player absorbing his soul
def r3_cutscene11():
    print("Minion dies. Soul taken.")
    #Now we continue to the next dialogue bit
    r3_cutscene12()
    
    
#This begins the kill sequence w/ dialogue.
def r3_cutscene10():
    if game.room3_tag4 == 1:
        #Set the tag to the next index
        game.room3_tag4 = 2
        #Put the right text into the attribute that displays it 
        textbox.text = [["Urgh... My Queen, I'm-- I'm sorry.", "", ""], ["I-- failed-- you-", "", ""]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'minion'
        textbox.skippable = True
        
    elif game.room3_tag4 == 2:
        #Iterate tag4
        game.room3_tag4 = 3
        #Close text box
        textbox.speaker = 'none'
        #Here, we call the function that begins the minion death animation.
        r3_cutscene11()    


### MINION ENCOUNTER TAG 3 SECTION ###
#This has r3_cutscene9, and runs from Choice 2, if you decided to spare the minion, until the end
#  of the encounter.

#This is called by choice2. It begins a text exchange.
def r3_cutscene9():
    if game.room3_tag3 == 1:
        #Set the tag to the next index
        game.room3_tag3 = 2
        #Put the right text into the attribute that displays it 
        textbox.text = [["... Look, I can't do this.", "", ""],
                        ["You don't deserve to die, just because", "you've been fooled into servitude", "by an evil dragon."]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'player'
        textbox.skippable = True
        
    elif game.room3_tag3 == 2:
        #Set the tag to the next index
        game.room3_tag3 = 3
        #Put the right text into the attribute that displays it 
        textbox.text = [["Fooled? Evil?", "", ""],
                        ["I don't know where you've been", "getting your information,", "but The Queen ain't evil."],
                        ["Sure, she's been acting a little, uh, ERRATIC lately...", "But before she got sick, she was so nice!", ""]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'minion'
                
    elif game.room3_tag3 == 3:
        #Set the tag to the next index
        game.room3_tag3 = 4
        #Put the right text into the attribute that displays it 
        textbox.text = [["What do you mean, got sick?", "", ""]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'player'
        
    elif game.room3_tag3 == 4:
        #Set the tag to the next index
        game.room3_tag3 = 5
        #Put the right text into the attribute that displays it 
        textbox.text = [["Yeah, she's been sick for a while now.", "It's been making her crazy.", ""],
                        ["It's gotten so bad, us minions", "eventually had to lock her up.", "And her MAGIC ORB, too."],
                        ["She kept trying to use it,", "but it would always go wrong somehow.", "We had to separate her from it."],
                        ["We were worried she'd--", "", ""],
                        ["Crap.", "", ""],
                        ["I- I've said too much.", "", ""]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'minion'                
        
    elif game.room3_tag3 == 5:
        #Set the tag to the next index
        game.room3_tag3 = 6
        #Put the right text into the attribute that displays it 
        textbox.text = [["Wait, no, tell me more!", "", ""], ["What does her magic orb do?", "Where did you put it?", ""]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'player'
        
    elif game.room3_tag3 == 6:
        #Set the tag to the next index
        game.room3_tag3 = 7
        #Put the right text into the attribute that displays it 
        textbox.text = [["Stop.", "Look, I have no reason to trust an outsider.", "For all I know, you're here to make things worse."],
                        ["I clearly can't stop you from going forward", "while I'm in this state.", "So, please..."],
                        ["Please, just don't hurt my Queen.", "", ""]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'minion'
    
    elif game.room3_tag3 == 7:
        #This one ends the encounter.
        player.movement_allowed = True
        #These booleans attributed to Game lets us know the minion encounter is over
        game.room3_happening = False
        game.room3_over = True
        textbox.speaker = 'none'
        

    
### MINION ENCOUNTER TAG 2 SECTION ###
#This has r3_cutscene6-8, and runs from Choice 1, if you decided to fight the minion, until the
#  choice you make either to spare or kill him.

#This is called at the end of cutscene 7. It is a text exchange that leads to Choice 2.
def r3_cutscene8():
    if game.room3_tag2 == 4:
        #Set the tag to the next index
        game.room3_tag2 = 5
        #Put the right text into the attribute that displays it 
        textbox.text = [["GYAH!", "", ""], ["COUGH, COUGH,", "", ""], ["Ugh...", "", ""]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'minion'
    elif game.room3_tag2 == 5:
        #Set the tag to the next index
        game.room3_tag2 = 6
        #Put the right text into the attribute that displays it 
        textbox.text = [["(Oh man... Am I really about to kill him?)", "", ""]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'player'
    elif game.room3_tag2 == 6:
        #This is the choice section.
        #Increase tag2 to 7 so it becomes undetectable from now on
        game.room3_tag2 = 7
        #(Choice1.tag is already at 2)
        
        #Now set the text to all the right stuff
        textbox.text = ["Spare the", "dragon's minion?", ""]
        textbox.skippable = False
        player.movement_allowed = False
        choice1.text = ["Spare him"]
        choice2.text = ["Kill him"]
        textbox.speaker = 'choice'
        

#This is called by cutscene6 once you skip through the last text. It begins the fighting exchange.
def r3_cutscene7():
    print("minion lands a blow, player lands a blow, minion misses a hit, player lands a blow & minion falls")
    #The final version will probably be a series of function calls ("r3_cutscene7_1" and so on)
    #  but for now cutscene8 is called here.
    r3_cutscene8()

#This is called by choice1 if you decide to fight him. It is a text exchange, starting on tag2==1.
def r3_cutscene6():
    if game.room3_tag2 == 1:
        #Set the tag to the next index
        game.room3_tag2 = 2
        #Put the right text into the attribute that displays it 
        textbox.text = [["Too bad, buddy. I'm not going anywhere.", "", ""]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'player'
        textbox.skippable = True
    elif game.room3_tag2 == 2:
        #Set the tag to the next index
        game.room3_tag2 = 3
        #Put the right text into the attribute that displays it 
        textbox.text = [["Then so be it!", "", ""]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'minion'
    elif game.room3_tag2 == 3:
        #Iterate tag2
        game.room3_tag2 = 4
        #Close text box
        textbox.speaker = 'none'
        #Here, we call the function that begins the minion/player fight animation.
        r3_cutscene7()    



### MINION ENCOUNTER TAG 1 SECTION ###
#This has r3_cutscene1-5, and runs from the beginning of the encounter, to the choice
#  you make as to whether you fight or talk with him.

#This is called by on_key_down when tag1 = 7. It's the choice that determines whether you fight or talk.
def r3_cutscene5():
    #Increase tag1 to 8 so it becomes undetectable from now on
    game.room3_tag1 = 8
    #Now we increase the choice1 tag so that the right function calls when you click stuff 
    choice1.tag = 1

    #Now set the text to all the right stuff
    textbox.text = ["The", "DRAGON'S MINION", "blocks the way!"]
    textbox.skippable = False
    player.movement_allowed = False
    choice1.text = ["Fight him"]
    choice2.text = ["Try to talk"]
    textbox.speaker = 'choice'
    
    
    
    
#This is called multiple times by on_key_down, when we get to the end index of one of the pieces of text.
#Depending on what game.room3_tag1 is equal to, it'll alter the text.
#This constitutes the back-and-forth exchange right before and including the final choice.
def r3_cutscene4():    
    ###THIS SECTION: Room 3 encounter exchange part 1. Dictated by game.room3_tag1
    #This is the first of the switches between who's talking during the initial exchange at the start of the scene.
    if game.room3_tag1 == 3:
        #Set the tag to the next index
        game.room3_tag1 = 4
        #Put the right text into the attribute that displays it 
        textbox.text = [["(This must be one of the creatures that", "the wizard warned me about...)", ""],
                        ["(I should be careful.", "He did say they can be quite deceitful.)", ""],
                        ["I'm not afraid of you...", "You can't stop me from", "getting what I need!"]]
        #Reset the index to 0
        textbox.index = 0
        textbox.speaker = 'player'
        textbox.skippable = True
        
    elif game.room3_tag1 == 4:
        #Set the tag to the next index
        game.room3_tag1 = 5
        #Put the right text into the textbox
        textbox.text = [["Well, that's gonna be a problem,", "because YOU can't stop ME", "from doing my job."],
                        ["The boss might be feeling a little strange right now, but", "I'm up to the task of keeping outsiders like you", "out of our home."]]
        #Alter appropriate variables
        textbox.index = 0
        textbox.speaker = 'minion'
    
    elif game.room3_tag1 == 5:
        #Set the tag to the next index
        game.room3_tag1 = 6
        #Put the right text into the textbox
        textbox.text = [['(Hmm... What does he mean by "feeling a little strange?")', '', '']]
        #Alter appropriate variables
        textbox.index = 0
        textbox.speaker = 'player'
        
    elif game.room3_tag1 == 6:
        #Set the tag to the next index
        game.room3_tag1 = 7
        #Put the right text into the textbox
        textbox.text = [["We won't be having a repeat of the last time.", "This is your final warning.", "Leave, now!"]]
        #Alter appropriate variables
        textbox.index = 0
        textbox.speaker = 'minion'

#This is called by r3_cutscene2 after the minion walks to you.
#It schedules the first part of the text exchange that occurrs next.
#  The text exchange will continue within on_key_down, which will repeatedly call cutscene4.
def r3_cutscene3():
    #Put the right text into the attribute that displays it 
    textbox.text = [["I don't know WHAT kinda creature", "you are, but you are NOT", "supposed to be here!"]]
    #Reset the index to 0
    textbox.index = 0
    textbox.speaker = 'minion'
    textbox.skippable = True
    #Increment the tag1 so that next time you press key down, it'll call cutscene4 for the first time
    game.room3_tag1 = 3
    
    
#This is called by on_key_down when game.room3_tag1 == 1, when you exit the dialogue "Hey, you!"
#It moves the minion to you, and calls the next function when he gets to his destination.
def r3_cutscene2():
    #First we call move_minion to move him to meet the player
    move_minion((560, 570))
    
    #Now we schedule the next function for the time it takes for him to get to his destination.
    #(We use calc_distance()/325 instead of calc_time cuz minion moves slower than player)
    time_sec = (calc_distance(560, 570, minion.pos[0], minion.pos[1]))/300
    
    clock.schedule_unique(r3_cutscene3, (time_sec + 0.25))
    #(We give it an extra quarter-second to let the user have a sec to visually process the minion)

    
    
#This function is scheduled by move_room3_alt() if you move to the correct X range.
# The function begins when you get into place.
def r3_cutscene1():
    #First thing that happens here is displaying a text box. We'll define it as "Other" since the minion's icon shouldn't appear here
    #Define relevant data
    #Put the right text into the attribute that displays it 
    textbox.text = [["Hey, you!", "", ""]]
    #Reset the index to 0
    textbox.index = 0
    textbox.speaker = 'other'
    textbox.skippable = True
    #Now for the final touch we define the "game.room3tag" to 1. This will be referenced in on_key_down, to call r3_cutscene2
    #  once the text is skipped.
    game.room3_tag1 = 1
    
### END OF MINION ENCOUNTER CUTSCENE SECTION ###
    
#Room 3 functions cont'd:

#Moves the player around in room 3
def move_room3(pos):
    #First unschedule any potential room transitions
    unschedule3()
    
    #Now let's calculate the appropriate movement destination.
    x = pos[0]
    y = pos[1]
    #There's two possible areas of movement: The square with topleft (27, 262) & bottomright (231, 452)
    #  and the rectangle with topleft (27, 452) and bottomright (884, 630).
    
    #This handles if the player is in the uppermost square
    if 27 <= player.pos[0] <= 231 and 262 <= player.pos[1] <= 452:
        #Is x out of range? (You can't move to an X value outside of the square)
        if x < 27:
            x = 27
        elif x > 231:
            x = 231
        #Is Y out of range? (You can move down to the bottom edge of the lower rectangle from here)
        if y < 262:
            y = 262
        elif y > 630:
            y = 630
        
    #This handles if the player's X is the same as the uppermost square, but their Y is lower than it
    elif 27 <= player.pos[0] <= 231 and player.pos[1] > 452:
        #We need to handle this differently depending on whether the x of your mouse click was higher or
        #  lower than 231, which is the right edge of the upper square
        if x < 231:
            if x < 27:
                x = 27
            #Check for Y out of range
            if y < 262:
                y = 262
            elif y > 630:
                y = 630
        else:
            if x > 884:
                x = 884
            #Check for Y out of range
            if y < 452:
                y = 452
            elif y > 630:
                y = 630
            
        
    #This handles if the player is a different x AND y than the uppermost square
    else:
        #X's range is 27-884 here
        if x < 27:
            x = 27
        elif x > 884:
            x = 884
        #Y's range is 452-630
        if y < 452:
            y = 452
        elif y > 630:
            y = 630
    
    
    # We make a tuple of x,y because move_player takes the pos as a tuple.
    destination = (x,y)
    #Now we move.
    move_player(destination)
##I think we should try implementing the same sort of process used in Move Room 3 in Move Room 1
    
#This move room 3 function doesn't allow you to move further than a certain X range. When you get to that point,
#  it will trigger the Minion Encounter Scene.
def move_room3_alt(pos):
    #First unschedule any potential room transitions
    unschedule3()
    
    #Now let's calculate the appropriate movement destination.
    x = pos[0]
    y = pos[1]
    #There's two possible areas of movement: The square with topleft (27, 262) & bottomright (231, 452)
    #  and the rectangle with topleft (27, 452) and bottomright (884, 630).
    
    #This handles if the player is in the uppermost square
    if 27 <= player.pos[0] <= 231 and 262 <= player.pos[1] <= 452:
        #Is x out of range? (You can't move to an X value outside of the square)
        if x < 27:
            x = 27
        elif x > 231:
            x = 231
        #Is Y out of range? (You can move down to the bottom edge of the lower rectangle from here)
        if y < 262:
            y = 262
        elif y > 630:
            y = 630
        
    #This handles if the player's X is the same as the uppermost square, but their Y is lower than it
    elif 27 <= player.pos[0] <= 231 and player.pos[1] > 452:
        #We need to handle this differently depending on whether the x of your mouse click was higher or
        #  lower than 231, which is the right edge of the upper square
        if x < 231:
            if x < 27:
                x = 27
            #Check for Y out of range
            if y < 262:
                y = 262
            elif y > 630:
                y = 630
        else:
            if x > 440:
                x = 440
            #Check for Y out of range
            if y < 452:
                y = 452
            elif y > 630:
                y = 630
            
        
    #This handles if the player is a different x AND y than the uppermost square
    else:
        #X's range is 27-440 here
        if x < 27:
            x = 27
        elif x > 440:
            x = 440
        #Y's range is 452-630
        if y < 452:
            y = 452
        elif y > 630:
            y = 630
    
    
    #Here's where the alt part comes in: If your X is 440, then once you get to your destination,
    #  the minion cutscene will begin by calling r3_cutscene1()
    if 435 <= x <= 440:
        #Alter x and y so that you go to the perfect spot for the encounter
        x = 440
        y = 567
        #We disallow movement here so you can't click away and unschedule all this.
        player.movement_allowed = False
        #Also, here is where we declare that room 3 cutscene is currently happening
        game.room3_happening = True
        #Now we schedule the next part of the cutscene
        clock.schedule_unique(r3_cutscene1, calc_time(player.pos[0], player.pos[1], x, y))
        
    # We make a tuple of x,y because move_player takes the pos as a tuple.
    destination = (x,y)
    #Now we move.
    move_player(destination)
   
   
########################################################################
### ROOM 4 INTERACTION FUNCTIONS ###

'''
 TO-DO:
  -Program the fountain interaction function
  -Tweak the movement functions to ensure best usability, least corner-cutting and floating.
     In on_mouse_down, we should probably have an if-branch so that things like room4_bridge_interact()
     are only called when the player is in the right place for non-floating, and otherwise just call move_room4(pos)
'''
#For unscheduling potential functions associated with this room
def unschedule4():
    clock.unschedule(r4_to_r3)
    clock.unschedule(r4_to_r5)
    clock.unschedule(room4_fountain_interact2)

#Clicking on the bridge will move you back to room 3
def room4_bridge_interact():
    #We'll call move_player so they move to the door, then schedule the transition
    #  for the time it takes to get there.
    move_player((0, 489))
    clock.schedule_unique(r4_to_r3, calc_time(player.pos[0], player.pos[1], 0, 489))
    
#Called by room4_bridge_interact. Takes you to room 3.
def r4_to_r3():
    #Tell the game it's the new room
    game.room = 'room3'
    #Make the right room image appear
    game.image = "room3"
    #Move player to correct location for the new room's entry
    player.midbottom = (1009, 534)
    
def room4_door_interact():
    #We'll call move_player so they move to the door, then schedule the transition
    #  for the time it takes to get there.
    move_player((838, 261))
    clock.schedule_unique(r4_to_r5, calc_time(player.pos[0], player.pos[1], 838, 261))

#Called by room4_door_interact. Takes you to room 5
def r4_to_r5():
    #Tell the game it's the new room
    game.room = 'room5'
    #Make the right room image appear
    game.image = "room5"
    #Move player to correct location for the new room's entry
    player.midbottom = (528, 596)

#This function will be called when you click on the fountain.
def room4_fountain_interact1():
    #Since this is a movement function I'm gonna unschedule other interaction/transitions
    unschedule4()
    #Now we move the player 
    move_player((466, 464))
    clock.schedule_unique(room4_fountain_interact2, calc_time(player.pos[0], player.pos[1], 466, 464))
        
#Called by the first fountain interact once you move to the fountain.
#Displays text, based on where you're at in the story.
def room4_fountain_interact2():
   #This runs if you have gotten the obsidian key but haven't given it to the fountain yet.
    if r5a_tablet.solved and not room4_fountain.keyget:
        room4_fountain.keyget = True
        textbox.text = [["You line up the OBSIDIAN KEY with the hole","on the rim of the fountain.","It's a perfect fit."],
                        ["When you insert the key all the way, you hear a click,","and water begins to flow.",""],
                        ["The sound of stone sliding against stone","begins to echo down from the hallway","to the north."]]
        textbox.index = 0
        player.movement_allowed = False
        textbox.skippable = True
        textbox.speaker = 'textbox_other'
        #sounds.fountain.play()
    #This runs if you haven't solved the Secret Puzzle
    elif not r5a_tablet.solved:
        textbox.text = [["It's an obsidian fountain?","",""],["No water's running.","I wonder if it ever worked.",""]]
        textbox.index = 0
        player.movement_allowed = True
        textbox.skippable = True
        textbox.speaker = 'textbox_player'
    #This runs if you've solved the secret puzzle AND given the key to the fountian.
    else:
        textbox.text = [["Wow...","Was that magic?",""]]
        textbox.index = 0
        player.movement_allowed = True
        textbox.skippable = True
        textbox.speaker = 'textbox_player'

        
    
#Will calculate the appropriate destination based on the mouse click and the room's range of motion, then call move_player.
def move_room4(pos):
    #Unschedule potential room transitions
    unschedule4()
    
    #Pull out the variables we're working with
    x = pos[0]
    y = pos[1]
    
    #THere are two possible regions of movement in this area: The left region is from (20, 425) to (782, 520)
    #  and to its right, the right region is from (782, 283) to (1085, 520)
    #Your possible destination depends on where you already are in these two regions.
    
    #This is for if you're within the left region:
    if player.pos[0] <= 782:
        #From here, you can only move in areas with a Y in [425-520]
        #Is X out of range?
        if x < 20:
            x = 20
        elif x > 1085:
            x = 1085
        #Is Y out of range?
        if y < 425:
            y = 425
        elif y > 520:
            y = 520
    
    #This is for if you're within the right region, but on the same Y as the left region 
    elif player.pos[0] > 782 and player.pos[1] >= 425:
        #From here, you can move into the left region, or you can move anywhere within the right region
        #Let's check to see which the user was trying to do.
        if x <= 782:
            #This means our destination is in the left region
            #  (Which impacts what the range can be for X and Y)
            #Is x out of range?
            if x < 20:
                x = 20
            #Is y out of range?
            if y < 425:
                y = 425
            elif y > 520:
                y = 520
        else:
            #This means our destination is in the right region
            #Is X out of range?
            if x > 1085:
                x = 1085
            #Is Y out of range?
            if y < 283:
                y = 283
            elif y > 520:
                y = 520
    
    #This is for if you're in the right region but not the same Y as the left
    else:
        #Our range here is just the square from (782, 283) to (1085, 520)
        #Is x out of range?
        if x < 782:
            x = 782
        elif x > 1085:
            x = 1085
        #Is Y out of range?
        if y < 283:
            y = 283
        elif y > 520:
            y = 520
    
    
    # We make a tuple of x,y because move_player takes the pos as a tuple.
    destination = (x,y)
    #Now we move.
    move_player(destination)

########################################################################
### ROOM 5 INTERACTION FUNCTIONS ###

#Called when clicking on the door.
def room5_door_interact():
    if not r5a_button.solved:
        print("the door is closed")
        #Player text will display here
    else:
        #Maybe have a dialogue asking if ur sure you're ready, since after the boss room you cant go back?
        move_player((530, 274))
        clock.schedule_unique(r5_to_r6, calc_time(player.pos[0], player.pos[1], 530, 274))
        
#Changes game files for boss room
def r5_to_r6():
    #Tell the game what room its in and what pic it has
    game.room = 'room6'
    game.image = 'room6'
    #Because room 6 is special, it doesn't have a border, it moves to 0,0 so as to fit correctly in the window
    game.topleft = (0,0)
    #Put the player in the right spot
    player.pos = (552, 740)
    #Now, depending if the good ending has happened or not, we'll schedule two different cutscenes
    if r5d_orb.destroyed:
        room6_dragon.image = 'room6_dragon_healed'
        r6_cutscene1_1()
    else:
        room6_dragon.image = 'room6_dragon_sick'
        r6_cutscene2_1()
    
    
    
#Called when clicking on the pathway connecting room 5 to room 4.
def room5_pathway_interact():
    #We'll call move_player so they move to the door, then schedule the transition
    #  for the time it takes to get there.
    move_player((538, 757))
    clock.schedule_unique(r5_to_r4, calc_time(player.pos[0], player.pos[1], 538, 757))
    
#Called by room5_pathway_interact. Takes you to room 4.
def r5_to_r4():
    #Tell the game it's the new room
    game.room = 'room4'
    #Make the right room image appear
    game.image = "room4"
    #Move player to correct location for the new room's entry
    player.midbottom = (862, 301)
    
#Called when you click tunnel 1
def room5_tunnel1_interact():
    #We store the coordinates of where you'll come out when you exit back to room 5.
    room5_tunnel1.coords = (139,299)
    #We also store a string (a, b or c) representing what room you went into.
    room5_tunnel1.letter = 'a'
    #Now we move to that place.
    move_player((139, 299))
    clock.schedule_unique(r5_to_r5ac, calc_time(player.pos[0], player.pos[1], 139, 299))
    

#Called when you click tunnel 2
def room5_tunnel2_interact():
    #We store the coordinates of where you'll come out when you exit back to room 5.
    room5_tunnel1.coords = (290, 300)
    #We also store a string (a, b or c) representing what room you went into.
    room5_tunnel1.letter = 'b'
    #Now we move to that place.
    move_player((290, 300))
    clock.schedule_unique(r5_to_r5ac, calc_time(player.pos[0], player.pos[1], 290, 300))
    
#Called when you click tunnel 3
def room5_tunnel3_interact():
    #We store the coordinates of where you'll come out when you exit back to room 5.
    room5_tunnel1.coords = (797, 295)
    #We also store a string (a, b or c) representing what room you went into.
    room5_tunnel1.letter = 'c'
    #Now we move to that place.
    move_player((797, 295))
    clock.schedule_unique(r5_to_r5ac, calc_time(player.pos[0], player.pos[1], 797, 295))

#Called by interacting with any of the three tunnels. Transitions to the room A-C room.
#Takes an argument, a string with a/b/c, to know what room to go to
def r5_to_r5ac():
    #Make the right room image appear
    game.image = "room5a"
    #Move player to correct location for the new room's entry
    player.midbottom = (544, 627)
    
    #Now we need to alter certain variables specifically based on what room we're in.
    #To find what room we're in, we'll pull out the letter stored within room5_tunnel1.
    letter = room5_tunnel1.letter
    
    #For altering the tablet's image, and for editing game.room, we'll use a conditional branch to check what room we're in:
    if letter == 'a':
        r5a_tablet.image = '5a_tablet'
        game.room = 'room5a'
    elif letter == 'b':
        r5a_tablet.image = '5b_tablet'
        game.room = 'room5b'
    else:
        r5a_tablet.image = '5c_tablet'
        game.room = 'room5c'
        
    #For the button, we check if this button has been pressed
    if letter in r5a_button.clicked:
        r5a_button.image = '5a_button_pressed'
    else:
        r5a_button.image = '5a_button'
    
    

#Called when you click tunnel 4, if tunnel 4 is available
def room5_tunnel4_interact():
    move_player((949, 293))
    clock.schedule_unique(r5_to_r5d, calc_time(player.pos[0], player.pos[1], 949, 293))
    
def r5_to_r5d():
    #Make the right room image appear
    game.image = "room5d"
    #Tell the game what room it is
    game.room = 'room5d'
    #Move player to correct location for the new room's entry
    player.midbottom = (552, 644)

#Called when you click the tablet
def room5_tablet_interact():
    print("room 5 tablet interact")
    #Moves player to tablet and displays text explaining the puzzle opening r5door
    
#Calculates destination in room 5.
def move_room5(pos):
    #Unschedule potential room transitions
    clock.unschedule(r5_to_r4)
    clock.unschedule(r5_to_r5ac)
    
    x = pos[0]
    y = pos[1]
    
    #The range of movement in Room 5 is a simple rectangle region from (65, 298) to (1012, 583)
    #Is X out of range?
    if x < 65:
        x = 65
    elif x > 1012:
        x = 1012
    #Is Y out of range?
    if y < 298:
        y = 298
    elif y > 583:
        y = 583
    
    # We make a tuple of x,y because move_player takes the pos as a tuple.
    destination = (x,y)
    #Now we move.
    move_player(destination)


########################################################################
### ROOMS 5A-C INTERACTION FUNCTIONS ###
    
#Called by on_mouse_down if you click on the button,
#  when r5a_button.solved == False
#Takes an argument "letter", a string containing either a, b, or c, to know which room we're in
def r5_button_interact(letter):
    #sounds.button.play()
    #First let's check to see if this button has been clicked before
    #We'll only append a/b/c to the list if it has NOT been clicked already
    if not letter in r5a_button.clicked:
        #Put the letter into the list storing the order of buttons clicked
        r5a_button.clicked.append(letter)
        #Make the button's image the pressed one
        r5a_button.image = "5a_button_pressed"
        
        #Now let's check to see if the list is 3 long.
        if len(r5a_button.clicked) == 3:
            #If so, we need to check whether the buttons are in the correct order.
            if r5a_button.clicked == ["c", "b", "a"]:
                #The buttons are in the correct order!
                #Alter the boolean storing whether the puzzle has been solved:
                r5a_button.solved = True
                #Alter the room 5 door's image to be open:
                room5_door.image = 'room5_door_open'
                print("yay")
            else:
                #The buttons were not in the correct order. Let's reset the puzzle.
                #Empty the list
                r5a_button.clicked = []
                #Make the button into the unclicked image again
                r5a_button.image = '5a_button'
                print("try again")
                '''
                TO-DO: Maybe make like a stone shuffling sound play, and/or have some player dialogue text like "that didn't seem to be right..."
                
                -Also, as it stands, the button will not actually be the pressed image at all, since it immediately resets.
                   is there a way to make a little pause before it resets to the unpressed version? 
                '''

#Called when you click the tablet. Takes a string argument to know what room it's in.
def r5a_tablet_interact(letter):
    #We append the letter to the tablet's clicked list
    r5a_tablet.clicked.append(letter)
    
    #Is the list 4 long? If so we need to check if the pattern was correct
    if len(r5a_tablet.clicked) == 4:
        #Is it correct?
        if r5a_tablet.clicked == ['a', 'c', 'b', 'a']:
            r5a_tablet.solved = True
            print('you got the stone key!')
        else:
            #This means the pattern wasn't right
            r5a_tablet.clicked = []
            print("try again")
    


#Moves you off the pathway and then transitions back to room 5     
def r5_pathway_interact():
    move_player((547, 770))
    clock.schedule_unique(r5ac_to_r5, calc_time(player.pos[0], player.pos[1], 547, 770))

#Switches the room back to room 5
def r5ac_to_r5():
    #Tell the game what room you're in
    game.room = 'room5'
    #Make the right room image appear
    game.image = "room5"
    #Put the player in front of the tunnel they went through, as stored in tunnel1
    player.pos = room5_tunnel1.coords
    
def move_room5ac(pos):
    clock.unschedule(r5ac_to_r5)
    
    x = pos[0]
    y = pos[1]
    
    #The acceptable range for this room is (292, 262) to (767, 544)
    #Is X out of range?
    if x < 292:
        x = 292
    elif x > 767:
        x = 767
    #Is Y out of range?
    if y < 262:
        y = 262
    elif y > 544:
        y = 544
    
    
    # We make a tuple of x,y because move_player takes the pos as a tuple.
    destination = (x,y)
    #Now we move.
    move_player(destination)
    
########################################################################
### ROOM 5D INTERACTION FUNCTIONS ###

def r5d_pathway_interact():
    clock.unschedule(r5d_orb_interact)
    move_player((552, 770))
    clock.schedule_unique(r5d_to_r5, calc_time(player.pos[0], player.pos[1], 552, 770))

def r5d_to_r5():
    #Tell the game what room you're in
    game.room = 'room5'
    #Make the right room image appear
    game.image = "room5"
    #Put the player in front of the tunnel they went through
    player.pos = (949, 293)
    
#This is scheduled when you click on the orb for the first time
#It's called after you move to the orb. It begins the room 5 cutscene
def r5d_orb_interact():
    #Set relevant variables
    game.room5_happening = True
    player.movement_allowed = False
    game.room5_tag1 = 1
    #Queue up first dialogue
    #Text is slightly different depending on if the minion ever told you about the Dragon's Magic Orb
    if game.room3_outcome == 'talk' or game.room3_outcome == 'spare':
        textbox.text = [["Woah.","",""],["This must be the dragon's","Magic Orb.",""],["It looks... Infected, somehow. I feel like","there's something I have to do with it.","Like, destroy it?"],
                        ["Hmm...","",""]]   
    else:
        textbox.text = [["Woah.","",""],["What is this thing?","",""],["It looks... Infected, somehow. I feel like","there's something I have to do with it.","Like, destroy it?"],
                        ["Hmm...","",""]]
    
    textbox.index = 0
    textbox.skippable = True
    textbox.speaker = 'player'

    
### ROOM 5 CUTSCENE FUNCTIONS BEGIN

#Called when you skip through the dialogue 
def r5_cutscene1():
    if game.room5_tag1 == 1:
        #Set variable to make wizard appear
        wizard.pos = (411, 296)
        wizard.appear = True
        #Some kinda sound effect to show the wizard appears maybe?
        textbox.text = [["Woah!","What are you doing here, sir?!",""]]
        textbox.index = 0
        game.room5_tag1 = 2
    
    elif game.room5_tag1 == 2:
        textbox.text = [["I implore you to cease what you are doing!","",""],["I saw through my scrying pool","that you were planing to","destroy MY MAGIC ORB."]]
        textbox.index = 0
        textbox.speaker = 'wizard'
        game.room5_tag1 = 3
    
    elif game.room5_tag1 == 3:
        textbox.text = [["Your magic orb?","I thought this belonged to","the Dragon?"]]
        textbox.index = 0
        textbox.speaker = 'player'
        game.room5_tag1 = 4
        
    elif game.room5_tag1 == 4:
        textbox.text = [["Ohohoho!","Do not believe everything you hear,","foolish child."], ["Yes, yes, I need this... I need this","in order to harvest that DRAGON'S SOUL","for my healing spell."],
                        ["The dragon, she- she STOLE this from me!","As you can see by its appearance,","SHE placed an evil curse upon it..."],
                        ["...","","......."],
                        ["You believe me,","don't you, child?",""]]
        textbox.index = 0
        textbox.speaker = 'wizard'
        game.room5_tag1 = 5
    
    elif game.room5_tag1 == 5:
        textbox.text = [["...Yes?","Yes.",""]]
        textbox.index = 0
        textbox.speaker = 'player'
        game.room5_tag1 = 6
        
    elif game.room5_tag1 == 6:
        textbox.text = [["Good, because I need your assistance with this.","Help me to take back my MAGIC ORB, and we can retrieve","the soul of the evil dragon!"],
                        ["Just step away from the orb, child.","Come closer to me, now.",""]]
        textbox.index = 0
        textbox.speaker = 'wizard'
        game.room5_tag1 = 7
        
    elif game.room5_tag1 == 7:
        textbox.text = [["(Hmm... Something seems off.)","",""],["...","",""],["No.","I don't trust you.","What do you REALLY want from me?"]]
        textbox.index = 0
        textbox.speaker = 'player'
        game.room5_tag1 = 8
        
    elif game.room5_tag1 == 8:
        textbox.speaker = 'none'
        move_player((620, 476))
        game.room5_tag1 = 9
        clock.schedule_unique(r5_cutscene1, 0.65)
    
    elif game.room5_tag1 == 9:
        textbox.text = [["STOP!","WHAT ARE YOU DOING?!","",""]]
        textbox.index = 0
        textbox.speaker = 'wizard'
        game.room5_tag1 = 10
        
    elif game.room5_tag1 == 10:
        textbox.text = [["Something I should've done","the moment I stepped in here.",""]]
        textbox.index = 0
        textbox.speaker = 'player'
        game.room5_tag1 = 11
        
    elif game.room5_tag1 == 11:
        #INSERT GLASS SHATTERING NOISE HERE
        r5d_orb.destroyed = True
        r5d_orb.image = '5d_orb_destroyed'
        #Make the wizard disappear
        #(ALTERNATE FOR LATER POLISHING: Make him a puff of smoke and THEN disappear.)
        wizard.appear = False
        textbox.speaker = 'none'
        game.room5_tag1 = 12
        clock.schedule_unique(r5_cutscene1, 0.75)
        
    elif game.room5_tag1 == 12:
        textbox.text = [["Huh...", "Did I kill the wizard?", "I guess that orb contained some of his magic."],
                        ['I wonder what that did to the "evil" dragon.',"I should see if there's a way","into her chamber."]]
        textbox.index = 0
        textbox.speaker = 'player'
        game.room5_tag1 = 13
        
    elif game.room5_tag1 == 13:
        #This all ends the encounter here. Next the player will move to the dragon's chamber.
        textbox.speaker = 'none'
        game.room5_tag2 = 1
        player.movement_allowed = True
        #We say "button solved" to true here cuz that's what opens the door. So when the player exits, door'll be open
        r5a_button.solved = True
        #Alter the room 5 door's image to be open:
        room5_door.image = 'room5_door_open'
        #End cutscene
        game.room5_happening = False
    
    
### ROOM 5 CUTSCENE FUNCTIONS END
    

def move_room5d(pos):
    clock.unschedule(r5d_to_r5)
    
    x = pos[0]
    y = pos[1]
    
    #Range of movement here is a square from (316, 190) to (790, 538)
    #(Highly optional to-do: Make movement range into a few different rectangles, since 5d is a circleish room & this square has parts
    #  you can't move to?)
    
    #Is x out of range?
    if x < 316:
        x = 316
    elif x > 790:
        x = 790
    #Is Y out of range?
    if y < 190:
        y = 190
    elif y > 538:
        y = 538
    
    # We make a tuple of x,y because move_player takes the pos as a tuple.
    destination = (x,y)
    #Now we move.
    move_player(destination)

########################################################################
### ROOM 6 INTERACTION FUNCTIONS ###

'''
If you enter this room, and you haven't destroyed the orb & killed the wizard, the dragon will be all sick and creepy
   and it'll attack you. You'll get hit and be like half-down, and that's when the wizard will appear! You'll go like
   "oh thank god the wizards here, he can defeat the evil dragon for me!" but of course the wizard will do an evil little
   laugh and take your soul. You die, the end, roll credits.
If you enter this room after destroying the orb, the dragon will be all happy and thank you for saving her from the possession
   spell she'd been put under. She will heal your pet, everything will be great, roll credits.
'''
#CUTSCENE 1 FUNCTIONS
#These run if you enter the room AFTER destroying the orb
def r6_cutscene1_1():
    if game.room6_tag1 == 0:
        game.room6_happening = True
        player.movement_allowed = False
        game.room6_tag1 = 1
        clock.schedule_unique(r6_cutscene1_1, 1)
    
    elif game.room6_tag1 == 1:
        textbox.text = [["Are you...?","",""]]
        textbox.index = 0
        textbox.speaker = 'player'
        game.room6_tag1 = 2
        
    elif game.room6_tag1 == 2:
        textbox.text = [["Yes.","I am the queen of this cavern.",""],["Thank you, human, for restoring my health","by undoing the terrible curse that the wizard","cast upon me."],
                        ["Come closer, that I might return the kindness","you have done for me.",""]]
        textbox.index = 0
        textbox.speaker = 'dragon'
        game.room6_tag1 = 3
        
    elif game.room6_tag1 == 3:
        move_player((576, 585))
        game.room6_tag1 = 4
        textbox.speaker = 'none'
        clock.schedule_unique(r6_cutscene1_1, calc_time(player.pos[0], player.pos[1], 576, 585))
        
    elif game.room6_tag1 == 4:
        textbox.text = [["I understand that your companion is in need of healing?","",""], ["With my magic restored,","I can do this for you.",""]]
        textbox.index = 0
        textbox.speaker = 'dragon'
        game.room6_tag1 = 5
        
    elif game.room6_tag1 == 5:
        textbox.speaker = 'none'
        game.room6_happening = False
        clock.schedule_unique(start_credits, 0.5)

#CUTSCENE 2 FUNCTIONS
#These run if you enter the room WITHOUT destroying the orb
def r6_cutscene2_1():
    if game.room6_tag2 == 0:
        game.room6_happening = True
        player.movement_allowed = False
        game.room6_tag2 = 1
        clock.schedule_unique(r6_cutscene2_1, 1)
        
    elif game.room6_tag2 == 1:
        textbox.text = [["Oh god,","It's more terrifying than I ever","could have imagined."]]
        textbox.index = 0
        textbox.speaker = 'player'
        game.room6_tag2 = 2
        
    elif game.room6_tag2 == 2:
        wizard.pos = (416, 519)
        wizard.appear = True
        textbox.text = [["Wizard, sir?!","What are you doing here?",""]]
        textbox.index = 0
        textbox.speaker = 'player'
        game.room6_tag2 = 3
        
    elif game.room6_tag2 == 3:
        textbox.text = [["...Heh heh.", "Heh heh heh.", ""]]
        textbox.index = 0
        textbox.speaker = 'wizard'
        game.room6_tag2 = 4
        
    elif game.room6_tag2 == 4:
        wizard.image = 'wizard2'
        textbox.text = [["BAH HA HA HAH!", "YOU FOOL! -HAHA- YOU ABSOLUTE IMBECILE!", ""],
                        ["IDIOT CHILD, HOW EASY IT WAS TO FOOL YOU", "WITH MY CLEVER LIES!",""],
                        ["I am not here to SAVE YOU.", "I am here to GATHER MY SPELL COMPONENTS!", ""],
                        ["One cursed dragon's soul...", "And one magically-empowered HUMAN SOUL!", "GAHAHAHAHA!"],
                        ["WORLD DOMINATION IS MINE!","",""]]
        textbox.index = 0
        textbox.speaker = 'wizard'
        game.room6_tag2 = 5
        
    elif game.room6_tag2 == 5:
        textbox.speaker = 'none'
        game.room6_happening = False
        clock.schedule_unique(start_credits, 0.5)


########################################################################
### CREDITS SEQUENCE FUNCTIONS ###

#This is called at the very end after the ending cutscene (whichever one) is totally over.
#Like a room transition scene, it changes all the variables to match what's going on
def start_credits():
    #???
    screen.clear()
    #Just in case, to avoid bugs, disallow movement
    player.movement_allowed = False
    #Set the credits actor's position (pos is set to midtop)
    credit_text.pos = (552, (HEIGHT+10))
    #Edit the game files
    game.room = 'credits'
    game.image = 'blankscreen'
    game.pos = (20,20)
    #Now that game.room = credits, the Update function will take it from here.
    
#This is called by the Update function during the credits sequence.
#It checks if the credits text has passed all the way up yet. It returns a T/F boolean.
    #True = The credits text is now above the top of the screen.
def check_credits():
    if credit_text.midbottom[1] <= -35:
        return True
    else:
        return False
    
#One function that just resets every important actor variable to its initial state
def initialize_everything():
    #Game
    game.topleft = (20,20)
    game.room3_over = False
    game.room3_happening = False
    game.room3_tag1 = 0
    game.room3_tag2 = 0
    game.room3_tag3 = 0
    game.room3_tag4 = 0
    game.room3_tag5 = 0
    game.room3_outcome = ''
    player.midbottom = (160,540)
    player.movement_allowed = False
    player.moving = False
    #Room 1
    room1_door2.closed = True
    room1_dragon1.clickable = False
    room1_dragon1.solved = False
    room1_dragon1.image = 'room1_dragon1'
    room1_dragon2.image = 'room1_dragon2'
    room1_dragon3.image = 'room1_dragon3'
    #Room 3
    minion.bottomleft = (1106, 520)
    minion.image = 'minion1'
    #Room 4
    room4_fountain.keyget = False
    room4_fountain.image = 'room4_fountain'
    #Room 5
    room5_tunnel1.coords = (0,0)
    room5_tunnel1.letter = 'a'
    room5_door.image = 'room5_door_closed'
    r5a_tablet.clicked = []
    r5a_tablet.solved = False
    r5a_button.clicked = []
    r5a_button.solved = False
    r5a_button.image = '5a_button'
    r5d_orb.destroyed = False
    r5d_orb.image = '5d_orb'
    
    #Now let's reset back to the title
    game.room = 'title'
    game.image = 'title_screen'

########################################################################
### CHOICE TEXT INTERACTION FUNCTIONS ###

#This is called when you click a choice box, when choice box tag == 1.
#The variable "choice" should be either 1 or 2, corresponding with whether you pressed box1 or box2.
def choicebox_1(choice):
    if choice == 1:
        #This is the "fight" choice.
        
        #Begin iterating tag 2
        game.room3_tag2 = 1
        #Call the next function
        r3_cutscene6()
        game.room3_outcome = 'fight'

    else:
        #Begin iterating tag 5
        game.room3_tag5 = 1
        game.room3_outcome = 'talk'
        
        r3_cutscene13()
        
    #Now we increment the choice tag so this specific function can't be called again.
    choice1.tag = 2
    
#This is the choice in the minion encounter, when you have the minion on his knees, to spare or kill.
def choicebox_2(choice):
    if choice == 1:
        #This is the spare choice
        game.room3_tag3 = 1
        game.room3_outcome = 'spare'
        #This brings you to the beginning of the following cutscene branch:
        r3_cutscene9()
        
    else:
        #This is the kill choice

        game.room3_tag4 = 1
        game.room3_outcome = 'kill'
        #This brings you to the beginning of the following cutscene branch:
        r3_cutscene10()
    
    #Now we move it to the next tag
    choice1.tag = 3


########################################################################
### BUILT-IN KEY HANDLERS ###
        
#Mouse click handler. Calls other functions (see Interaction Functions) based on what room you're in and where you click.
def on_mouse_down(pos):
#You're only allowed to move around/interact with stuff if player.movement_allowed. SO we check that at the top of everything else.
    if player.movement_allowed:
        #Before we check what room we're in, let's see if we should close the dialogue box because of the click.
        if not textbox.speaker == 'none':
            textbox.speaker = 'none'
        
        #NOW, let's check what room we're in, to see what interactions might be happening. Different interactions happen in each room.
        if game.room == 'room0':
                if room0_door.collidepoint(pos):
                    r0_door_interact()
                else:
                    move_room0(pos)
                
        
        elif game.room == 'room1':
                #Let's see if the user clicked on any actor in the game
                if room1_door1.collidepoint(pos):
                    #If you're in a certain part of the room, you can't reach door1 without cutting a corner,
                    #  so let's check your position to avoid that.
                    if player.pos[1] >= 450:
                        r1_door1_interact()
                    else:
                        #If you're in the wrong place you'll just move.
                        move_room1(pos)
                
                elif room1_door2.collidepoint(pos):
                    r1_door2_interact()
                    
                elif room1_dragon1.collidepoint(pos) or room1_dragon2.collidepoint(pos) or room1_dragon3.collidepoint(pos):
                    if room1_dragon1.clickable:
                        room1_dragon_clicked(pos)
                    
                #Otherwise let's do a movement
                else:
                    #We call the function that handles deciding the (x,y) of the destination
                    move_room1(pos)
                    
                    
        elif game.room == 'room2':
                if room2_door1.collidepoint(pos):
                    r2_door1_interact()
                
                elif room2_door2.collidepoint(pos):
                    r2_door2_interact()
                    
                elif room2_tablet.collidepoint(pos):
                    #First we unschedule possible room transitions in case those have been scheduled
                    clock.unschedule(r2_to_r1)
                    clock.unschedule(r2_to_r3)
                    #Now we move you to a spot in the floor near the tablet, before the text displays
                    move_player((726, 423))
                    #Schedule the text to display
                    clock.schedule_unique(r2_tablet_interact, calc_time(player.pos[0], player.pos[1], 726, 423))

                else:
                    move_room2(pos)
                
                
        elif game.room == 'room3':
                if room3_door.collidepoint(pos):
                    #You can only move to this door if you're in the right X range for it
                    if 27<= player.pos[0] <= 231:
                        r3_door_interact()
                    else:
                        move_room3(pos)
                
                elif room3_bridge.collidepoint(pos):
                    #If the cutscene has already happened, you can move to room 4
                    if game.room3_over:
                        #Before we move to the bridge we also need to make sure we're in the right Y range to be able
                        #  to move to it without cutting corners.
                        if player.pos[1] >= 452:
                            r3_bridge_interact()
                        else:
                            move_room3(pos)
                    #Otherwise, we'll just call the move function, to avoid the possibility of skipping the cutscene
                    #  by moving past the room
                    else:
                        move_room3_alt(pos)
                    
                else:
                    #This branch will run if the minion cutscene has Already Happened
                    if game.room3_over:
                        move_room3(pos)
                    #This else branch will run if you haven't yet had the cutscene
                    else:
                        move_room3_alt(pos)
                      
                      
        elif game.room == 'room4':
                if room4_bridge.collidepoint(pos):
                    #Let's check to see if the player is in the right place to move to the bridge.
                    #  (Their Y has to be within 425-520)
                    if player.pos[1] > 425:
                        room4_bridge_interact()
                    #If not, we'll just make them move toward the mouse click.
                    else:
                        move_room4(pos)
      
                elif room4_door.collidepoint(pos):
                    #Let's check to see if the player is in the right place to move to the door.
                    #  (Their X has to be within 782-1085)
                    if player.pos[0] >= 782:
                        room4_door_interact()
                    #If not, we'll just make them move toward the mouse click.
                    else:
                        move_room4(pos)
                    
                elif room4_fountain.collidepoint(pos):
                    #Let's check to see if the player is in the right place to move to the fountain.
                    #  (Their Y has to be within 425-520
                    if player.pos[1] >= 425:
                        room4_fountain_interact1()
                    #If not, we'll just make them move toward the mouse click.
                    else:
                        move_room4(pos)
                    
                else:
                    move_room4(pos)
            
            
        elif game.room == 'room5':
                if room5_door.collidepoint(pos):
                    room5_door_interact()
                    
                elif room5_pathway.collidepoint(pos):
                    room5_pathway_interact()
                    
                elif room5_tablet.collidepoint(pos):
                    room5_tablet_interact()
                    
                elif room5_tunnel1.collidepoint(pos):
                    room5_tunnel1_interact()
                    
                elif room5_tunnel2.collidepoint(pos):
                    room5_tunnel2_interact()
                
                elif room5_tunnel3.collidepoint(pos):
                    room5_tunnel3_interact()
                    
                #This will call if tunnel 4 is clicked AND is showed
                elif room5_tunnel4.collidepoint(pos) and room4_fountain.keyget:
                    room5_tunnel4_interact()
                    
                else:
                    move_room5(pos)
              
        #Everything but the tablet/button press is the same whether you're in 5a, 5b, or 5c
        elif game.room == 'room5a' or game.room == 'room5b' or game.room == 'room5c':
                #This is for if you clicked any of the buttons. Functionality depends on what room you're in.
                if r5a_button.collidepoint(pos) and not r5a_button.solved:
                    #We call a different button interact depending on what room we're in
                    if game.room == 'room5a':
                        r5_button_interact('a')
                    elif game.room == 'room5b':
                        r5_button_interact('b')
                    else:
                        r5_button_interact('c')
                
                #This is for if you clicked any of the tablets. Functionality depends on what room you're in.
                elif r5a_tablet.collidepoint(pos):
                    if game.room == 'room5a':
                        r5a_tablet_interact('a')
                    elif game.room == 'room5b':
                        r5a_tablet_interact('b')
                    else:
                        r5a_tablet_interact('c')
                    
                #This is the same in all 3 rooms
                elif r5a_pathway.collidepoint(pos):
                    r5_pathway_interact()
                
                #This is also the same for all 3 rooms
                else:
                    move_room5ac(pos)
                    
        elif game.room == 'room5d':
                if r5d_orb.collidepoint(pos):
                    #Moves you to The Orb
                    move_player((669, 523))
                    clock.schedule_unique(r5d_orb_interact, calc_time(player.pos[0], player.pos[1], 669, 523))

                    
                elif r5d_pathway.collidepoint(pos):
                    clock.unschedule(r5d_to_r5)
                    r5d_pathway_interact()
                    
                else:
                    clock.unschedule(r5d_to_r5)
                    move_room5d(pos)

#ONE THING that exists outside of the movement_allowed if-branch is clicking textbox choice boxes.
    elif textbox.speaker == 'choice' and (choice1.collidepoint(pos) or choice2.collidepoint(pos)):
        #Let's define a variable "chosen" which will be passed to the choice box interaction function when it's called
        if choice1.collidepoint(pos):
            chosen = 1
        elif choice2.collidepoint(pos):
            chosen = 2
            
        #Now we see which cbox interaction function to call depending on choicebox1.index
        if choice1.tag == 1:
            choicebox_1(chosen)
        elif choice1.tag == 2:
            choicebox_2(chosen)
            
            
            
            
################## ON KEY DOWN FUNCTION #####################
            
#This function handles the pressing of any key. It starts the game when you press enter at the start sequence, and
#  allows you to skip through text when dialogue has appeared. During special cutscenes, this function helps
#  the progression of the cutscene.
def on_key_down(key):
    #When the title is showing, the return key starts the game
    if game.room == 'title':
        if key == keys.RETURN:
            #This calls up the intro cutscene
            intro_cutscene1()
            
            
    #During gameplay itself, the return key skips through dialogue.
    #Let's check to see if someone is speaking right now.
    elif not textbox.speaker == 'none':
        #Now we see if the key pressed was return/enter.
        if key == keys.RETURN:   
            #If the textbox hasn't reached its end yet, pressing enter just cycles through the index.
            if not textbox.index == (len(textbox.text)-1):
                textbox.index += 1
                
            #If the textbox is at its final index, then pressing enter will close the text IF the textbox is currently skippable.
            #(Skippable means the textbox can be "skipped through" by pressing enter.)
            elif textbox.skippable:
                #There are certain instances in which skipping to the end of text is part of a certain scene. This happens for the intro cutscene
                if game.room == 'intro_cutscene':
                    #Getting to the end of the text at the intro will begin the game
                    #Make the screen black for the second between the dialogue ending & the game proper starting
                    game.image = 'blankscreen'
                    #Close the speaker window
                    textbox.speaker = 'none'
                    #Schedule the start of the game in a second
                    clock.schedule_unique(game_start, 1)
                
                #Closing the text box during the room 3 encounter is part of what progresses the encounter.
                # This section here handles that part:
                elif game.room3_happening == True:
                #Let's check whether we're within tag1 territory
                    if game.room3_tag1 == 1:
                        #Close the text box
                        textbox.speaker = 'none'
                        #Progress the scene's progression tag
                        game.room3_tag1 = 2
                        #Call the next function, which moves the minion towards you
                        r3_cutscene2()
                    elif game.room3_tag1 == 2:
                        r3_cutscene3()
                    elif 3<= game.room3_tag1 <= 6:
                        #This is called multiple times and has different functions depending on
                        #  what game.room3_tag1 is right now. (Which is iterated within cutscene 4)
                        r3_cutscene4()
                    elif game.room3_tag1 == 7:
                        r3_cutscene5()
                #If none of those were true... let's move to tag2.
                    elif 2 <= game.room3_tag2 <= 3:
                        r3_cutscene6()
                    elif 5 <= game.room3_tag2 <= 6:
                        r3_cutscene8()
                #If none of those were true, then let's move to tag3
                    elif 2 <= game.room3_tag3 <= 7:
                        r3_cutscene9()
                #Let's move to tag 4...
                    elif game.room3_tag4 == 2:
                        r3_cutscene10()
                    elif game.room3_tag4 == 4:
                        r3_cutscene12()
                #Tag 5?
                    elif 2 <= game.room3_tag5 <= 15:
                        r3_cutscene13()
                
                #How about the Good Ending cutscene in room 5?
                elif game.room5_happening == True:
                    if 1 <= game.room5_tag1 <= 13:
                        r5_cutscene1()
                
                elif game.room6_happening == True:
                    #Good ending cutscene
                    if r5d_orb.destroyed == True:
                        if 0 <= game.room6_tag1 <= 5:
                            r6_cutscene1_1()
                    #Bad ending cutscene
                    else:
                        if 0 <= game.room6_tag2 <= 5:
                            r6_cutscene2_1()
                
                #This is the REGULAR skipping-through procedure.
                else:
                    textbox.speaker = 'none'
                    #We allow player movement now.
                    player.movement_allowed = True
                    
            #If the text isn't skippable then nothing will happen. You have to do something else to close it. (This is the case for choice functions)         
            
            
    '''
    Pressing enter at the end of of the credits should take you back to the title screen.
      If we make the game re-playable without closing the window, we'd need a function to call that
      initializes/resets all of the variables and such.
    I'd also like to maybe have it so that in certain places, maybe during credits and the title screen,
      if you press ESC, you can close the window?
    '''

########################################################################
       
pgzrun.go()