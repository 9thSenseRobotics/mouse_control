import time as t
import create as c
import pygame
import pygame.joystick
import serial
from pygame.locals import *
from math import *

c.fetch = 0
c.tm = t.time()
c.tgap = 0
c.skip = 0
c.y = 0
c.x = 0
c.th = 0
c.speed = 0
ON = 7
OFF = 0

r = c.Create('/dev/ttyUSB1')
r.power_arduino(ON)

STOP = 0
SHUTDOWN = 7
GRASP = 1
RELEASE = 2
LEVEL = 3
TILT = 4
RAISE = 5
LOWER = 6

TRUE = 1
FALSE = 0

c.finger = RELEASE
c.tilter = LEVEL
c.lift = LOWER

r.servo_cmd(RELEASE)
t.sleep(0.1)
r.setPose(0,0,0)

# handle mouse event
def handleMouseMotion(e):
# reset fetch button
#    c.fetch = 0 
    t.sleep(0.040)
    ekey = pygame.event.peek(KEYDOWN)
    if (ekey == 1):
        r.go()
        r.power_arduino(OFF)
        r.start()
        return
        
    relpos = pygame.mouse.get_rel()
    c.x = relpos[0]
    c.y = relpos[1]
                    
    if (c.x == 0):
        c.th = 2
    else:
        c.th = fabs(c.y/c.x)
        
    if (c.th <= 1 and c.th >= -1):
        turn = c.x * 0.5        # turning speed customization
#        print 'turning speed: ', turn
        r.setWheelVelocities(turn, -turn)
    else:
        speed = -c.y * 2    # 7: speed customization
        r.go( speed, 0)     
#        print 'speed: ', speed
        
def handleMouseButton(e):                
#******************************************************
#**************    Lifting Starts      ****************    
    if (e.dict['button'] == 3):
        if (e.type == pygame.MOUSEBUTTONDOWN):
            if (c.lift == LOWER):
                print "Lifting\n"
                c.lift = RAISE
                r.servo_cmd(c.lift)
            else:
                print "Lowering\n"
                c.lift = LOWER
                r.servo_cmd(c.lift)
        else:
            r.servo_cmd(STOP)
            
#************       Lifting Ends         ***************            
#*******************************************************   


#******************************************************
#**************    Action Starts       ****************   
 
    elif (e.dict ['button'] == 1):
        if (e.type == pygame.MOUSEBUTTONUP):
            #finger closes
            if (c.finger != GRASP):
                c.finger = GRASP
                r.servo_cmd(c.finger)            
                # waiting loop for finger closing
                for actionTimer in range(100):
                    ekey = pygame.event.peek(KEYDOWN)
                    if (ekey != 1):
                        # no input from the interface               
                        t.sleep(0.01)
                    else:
                        r.go()
                        r.power_arduino(OFF)
                        r.start()
                        return             
                                  
            # level tilter
            if (c.tilter != LEVEL):
                c.tilter = LEVEL
                r.servo_cmd(c.tilter) 
                # waiting loop for pan leveling
                for actionTimer in range(50):
                    ekey = pygame.event.peek(KEYDOWN)
                    # ebutton = pygame.event.peek(pygame.MOUSEBUTTONUP)
                    if (ekey != 1):
                        # no input from the interface               
                        t.sleep(0.01)
                    else:
                        r.go()
                        r.power_arduino(OFF)
                        r.start()
                        return 
        else:    
            c.tgap = t.time() - c.tm
            c.tm = t.time()
            # double button press
            if (c.tgap <= 0.3):
                r.go()
                r.power_arduino(OFF)
                r.start()
                return
            # fetch button pressed the first time
            elif (c.lift == LOWER):
                # c.fetch = c.fetch + 1
                # if finger hasn't been released
                if (c.finger != RELEASE):
                    # release finger
                    c.finger = RELEASE
                    r.servo_cmd(c.finger)            
                # waiting loop for finger release
                    for actionTimer in range(100):
                        ekey = pygame.event.peek(KEYDOWN)
                        ebutton = pygame.event.peek(pygame.MOUSEBUTTONUP)
                        if ( ebutton != 1 and ekey != 1):
                # no input from the interface               
                            t.sleep(0.01)
                        elif (ekey == 1):
                            r.go()
                            r.power_arduino(OFF)
                            r.start()
                            return          
                        else:
                            pass
                else:
                    pass
                
                c.tilter = TILT
                r.servo_cmd(c.tilter) 
                # waiting loop for pan tilting
                for actionTimer in range(50):
                    ekey = pygame.event.peek(KEYDOWN)
                    ebutton = pygame.event.peek(pygame.MOUSEBUTTONUP)
                    if ( ebutton != 1 and ekey != 1):
                # no input from the interface               
                        t.sleep(0.01)
                    elif (ekey == 1):
                        r.go()
                        r.power_arduino(OFF)
                        r.start()
                        return              
                    else:
                        pass
                
                # robot going forward    
                r.go(15,0)            
                # waiting loop for mobile base moving forward
                forward = TRUE
                while (forward == TRUE):
                    ekey = pygame.event.peek(KEYDOWN)
                    ebutton = pygame.event.peek(pygame.MOUSEBUTTONUP)
                    emotion = pygame.event.peek(pygame.MOUSEMOTION)
                    if (ebutton != 1 and ekey != 1 and emotion != 1):
                        #   no input from the interface               
                        t.sleep(0.01)
                    elif (ekey == 1):
                        r.go()
                        r.power_arduino(OFF)
                        r.start()
                        return
                    elif (emotion == 1 or ebutton == 1):
                        forward = FALSE

                # robot stop
                r.go()
                
                if (emotion == 1):
                    pass
                else:
                    # finger closes
                    c.finger = GRASP
                    r.servo_cmd(c.finger)            
                    # waiting loop for finger closing
                    for actionTimer in range(100):
                        ekey = pygame.event.peek(KEYDOWN)
                        if (ekey != 1):
                            # no input from the interface               
                            t.sleep(0.01)
                        else:
                            r.go()
                            r.power_arduino(OFF)
                            r.start()
                            return             
                                          
                    # level tilter
                    c.tilter = LEVEL
                    r.servo_cmd(c.tilter) 
                    # waiting loop for pan leveling
                    for actionTimer in range(50):
                        ekey = pygame.event.peek(KEYDOWN)
                        # ebutton = pygame.event.peek(pygame.MOUSEBUTTONUP)
                        if (ekey != 1):
                            # no input from the interface               
                            t.sleep(0.01)
                        else:
                            r.go()
                            r.power_arduino(OFF)
                            r.start()
                            return 
                    


            # if fetch button pressed the third time                       
            elif (c.lift == RAISE):
                # c.fetch = 0
                # release/grasp finger    
                if (c.finger == RELEASE):               
                    c.finger = GRASP
                else:
                    c.finger = RELEASE
                r.servo_cmd(c.finger)            
            # waiting loop for finger release/grasp
                for actionTimer in range(100):
                    ekey = pygame.event.peek(KEYDOWN)
                    ebutton = pygame.event.peek(pygame.MOUSEBUTTONUP)
                    if ( ebutton != 1 and ekey != 1):
                        # no input from the interface               
                        t.sleep(0.01)
                    elif (ekey == 1):
                        r.go()
                        r.power_arduino(OFF)
                        r.start()
                        return              
                    else:
                        pass
                          
            else:
                # c.fetch = 0
                # release finger
                c.finger = RELEASE
                r.servo_cmd(c.finger)            
            # waiting loop for finger release/grasp
                for actionTimer in range(100):
                    ekey = pygame.event.peek(KEYDOWN)
                    ebutton = pygame.event.peek(pygame.MOUSEBUTTONUP)
                    if ( ebutton != 1 and ekey != 1):
            # no input from the interface               
                        t.sleep(0.01)
                    elif (ekey == 1):
                        r.go()
                        r.power_arduino(OFF)
                        r.start()
                        return             
                    else:
                        pass
                
                # tilt pan
                c.tilter = TILT
                r.servo_cmd(c.tilter) 
                # waiting loop for pan tilting
                for actionTimer in range(50):
                    ekey = pygame.event.peek(KEYDOWN)
                    ebutton = pygame.event.peek(pygame.MOUSEBUTTONUP)
                    if ( ebutton != 1 and ekey != 1):
                # no input from the interface               
                        t.sleep(0.01)
                    elif (ekey == 1):
                        r.go()
                        r.power_arduino(OFF)
                        r.start()
                        return             
                    else:
                        pass

#************        Action Ends         ***************            
#*******************************************************                

# wait for joystick input
def inputControl():
    while True:
#        for event in pygame.event.get():
#            if event.type == QUIT:
#                return
        while True:
            equit = pygame.event.peek(QUIT)
            ekey = pygame.event.peek(KEYDOWN)
            if (equit == 1 or ekey == 1):
                r.go()
                r.power_arduino(OFF)
                r.start()
                return
            
            buttonPressed = pygame.event.peek([pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
            if (buttonPressed != 1):         
# no button is pressed
                e = pygame.event.poll()
                if (e.type == pygame.NOEVENT):
                    r.go()
                elif (e.type == pygame.MOUSEMOTION):
                    handleMouseMotion(e)
#   button pressed
            else:                                                                                           
                buttonEvent = pygame.event.get([pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
                pygame.event.clear()
                for bEvent in buttonEvent:
                    handleMouseButton(bEvent)
                    
                

# main method
def main():
    # Call this function so the Pygame library can initialize itself
    pygame.init()
    screen = pygame.display.set_mode([600,600])
#    screen = pygame.display.set_mode([0,0],FULLSCREEN)
 
    # initialize pygame
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
    # run mouse listener loop
    inputControl()

# allow use as a module or standalone script
if __name__ == "__main__":
    main()






