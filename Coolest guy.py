from vex import *

brain=Brain()

controller = Controller()

Vision__LEMON = Signature (1, 2331, 3021, 2676, -4071, -3545, -3808, 2.5, 0)
Vision__LIME = Signature (2, -6751, -4967, -5859, -4243, -3277, -3760, 2.5, 0)
Vision__ORANGE_FRUIT = Signature (3, 7241, 8085, 7663, -1835, -1387, -1611, 3, 0)
Vision__PINK_BASKET = Signature (4, 5199, 5981, 5590, -445, 263, -91, 2.5, 0) 

vision = Vision(Ports.PORT3, 45, Vision__LEMON, Vision__LIME, Vision__ORANGE_FRUIT, Vision__PINK_BASKET)

rightMotor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
leftMotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
hDriveMotor = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)
horizontalMotor = Motor(Ports.PORT17, GearSetting.RATIO_18_1)
verticalMotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)
basketMotor = Motor(Ports.PORT12, GearSetting.RATIO_18_1)

hDriveMotor.set_stopping(COAST)

frontLine = Line(brain.three_wire_port.e)
backLine = Line(brain.three_wire_port.f)

Lineconstant = 1

ROBOT_IDLE = 0
ROBOT_SEARCHING = 1
ROBOT_CENTERING = 2
ROBOT_APPROACHING = 3
ROBOT_PICKING = 4
ROBOT_FIND_LINE = 5
ROBOT_LINING = 6
ROBOT_DROP_OFF = 7
ROBOT_FIND_TREE = 8
ROBOT_FIND_HILL = 9
ROBOT_LINE_HILL = 10
ROBOT_FIND_ORCHARD = 11

largestFruit = 0
pickCount = 0
fruitpick = 1

robotstate = ROBOT_IDLE

def handleL1():
    global robotstate
    global pickCount
    global fruitpick
    print("button L1")

    horizontalMotor.reset_position()

    if(robotstate != ROBOT_IDLE):
        leftMotor.stop()
        rightMotor.stop()
        horizontalMotor.stop()
        verticalMotor.stop()
        hDriveMotor.stop()
        robotstate = ROBOT_IDLE
        print("idle")
    else:
        pickCount = 0
        robotstate = ROBOT_FIND_HILL
        #TEMP
        fruitpick = 2
       
controller.buttonL1.pressed(handleL1)

def handleIdle():
    rightMotor.stop()
    leftMotor.stop()
    verticalMotor.stop()
    horizontalMotor.stop()
    basketMotor.stop()
    hDriveMotor.stop()

def findHill():
    global robotstate
    leftMotor.spin(FORWARD, 150, RPM)
    rightMotor.spin(FORWARD, 150, RPM)
    if (backLine.reflectivity() > 37):
        robotstate = ROBOT_LINE_HILL
        print("found the line")
        rightMotor.stop()
        leftMotor.stop()

def lineHill():
    global robotstate
    print("lining the hill")
    backRef = backLine.reflectivity()
    error = 37 - backRef
    kr = .35
    effort = kr * error
    leftMotor.spin(FORWARD, 150 + effort)
    rightMotor.spin(FORWARD, 150 - effort)
    if(frontLine.reflectivity() < 7):
        rightMotor.stop()
        leftMotor.stop()
        hDriveMotor.spin_for(FORWARD, 10, TURNS, 100, RPM, wait = True)
        robotstate = ROBOT_FIND_ORCHARD
        print("finding the line")



def findOrchard():
    print("backing up")
    global robotstate
    leftMotor.spin(REVERSE, 50, RPM)
    rightMotor.spin(REVERSE, 50, RPM)
    if (backLine.reflectivity() > 25):
        robotstate = ROBOT_FIND_TREE
        print("found line")

def handleSearch():
    global robotstate
   
    if(vision.take_snapshot(Vision__LEMON)):
        print("lemon?")
        lemonheight = vision.largest_object().height
        if(vision.largest_object().originY < 5):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM, wait = True)
            vision.take_snapshot(Vision__LEMON)
            lemonheight = vision.largest_object().height
        if(vision.largest_object().originY + lemonheight > 195):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM,wait = True)
            vision.take_snapshot(Vision__LEMON)
            lemonheight = vision.largest_object().height
        if(lemonheight < 45):
            lemonheight = 0
    else: lemonheight = 0

    if(vision.take_snapshot(Vision__ORANGE_FRUIT)):
        print("orange?")
        orangeheight = vision.largest_object().height
        if(vision.largest_object().originY < 5):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM, wait = True)
            vision.take_snapshot(Vision__ORANGE_FRUIT)
            orangeheight = vision.largest_object().height
        if(vision.largest_object().originY + orangeheight > 195):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM, wait = True)
            vision.take_snapshot(Vision__ORANGE_FRUIT)
            orangeheight = vision.largest_object().height
        if(orangeheight < 45):
            orangeheight = 0
    else: orangeheight = 0

    if(vision.take_snapshot(Vision__LIME)):
        print("lime?")
        limeheight = vision.largest_object().height
        if(vision.largest_object().originY < 5):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM, wait = True)
            vision.take_snapshot(Vision__LIME)
            limeheight = vision.largest_object().height
        if(vision.largest_object().originY + limeheight > 195):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM, wait = True)
            vision.take_snapshot(Vision__LIME)
            limeheight = vision.largest_object().height
        if(limeheight < 45):
            limeheight = 0
    else: limeheight = 0

    if(lemonheight > limeheight and lemonheight > orangeheight): 
        print("LEMON!")
        robotstate = ROBOT_CENTERING
        return 1
    elif(limeheight > lemonheight and limeheight > orangeheight): 
        print("LIME!")
        robotstate = ROBOT_CENTERING
        return 2
    elif(orangeheight > limeheight and orangeheight > lemonheight): 
        print("ORANGE!")
        robotstate = ROBOT_CENTERING
        return 3
    else: 
        print("retrying")
        verticalMotor.spin_for(REVERSE, .3, TURNS, 150, RPM, wait = True)
        return 0


def center_fruit():
    global largestFruit
    global robotstate

    if(largestFruit == 1): vision.take_snapshot(Vision__LEMON)
    elif(largestFruit == 2): vision.take_snapshot(Vision__LIME)
    elif(largestFruit == 3): vision.take_snapshot(Vision__ORANGE_FRUIT)

    idealx = 165
    idealy = 135

    largest = vision.largest_object()
    if (largest is not None):
        cx = largest.centerX
        cy = largest.centerY
    else:
        verticalMotor.stop()
        horizontalMotor.stop()
        print("no object found")
        return

    errorx = idealx-cx
    errory = idealy-cy
    kx = 1
    ky = 1
    effortx = kx*errorx
    efforty = ky*errory

    if(errorx < 5 and errory < 5):
        horizontalMotor.stop()
        verticalMotor.stop()
        robotstate = ROBOT_APPROACHING


    horizontalMotor.spin(REVERSE, effortx)
    verticalMotor.spin(REVERSE, efforty)
    

def handleApproach():
    global robotstate
    global largestFruit

    horizontalMotor.stop()
    verticalMotor.stop()

    if(largestFruit == 1): vision.take_snapshot(Vision__LEMON)
    elif(largestFruit == 2): vision.take_snapshot(Vision__LIME)
    elif(largestFruit == 3): vision.take_snapshot(Vision__ORANGE_FRUIT)

    goalHeight = 175
    height = vision.largest_object().height
    heightError = goalHeight-height
    kh = .6
    approachEffort = kh*heightError

    if(heightError < 15):
        leftMotor.stop()
        rightMotor.stop()
        robotstate = ROBOT_PICKING

    leftMotor.spin(FORWARD, approachEffort)
    rightMotor.spin(FORWARD, approachEffort)


def handlePick():
    print("picking")
    global robotstate
    global pickCount

    verticalMotor.spin_for(FORWARD, 1.5, TURNS, 100, RPM, wait = True)
    horizontalMotor.spin_for(REVERSE, horizontalMotor.position(), DEGREES, 100, RPM, wait = True)

    pickCount = pickCount + 1
    robotstate = ROBOT_FIND_LINE


def findLine():
    global robotstate
    global pickCount
    leftMotor.spin(REVERSE, 50, RPM)
    rightMotor.spin(REVERSE, 50, RPM)
    if (backLine.reflectivity() > 25):
        rightMotor.stop()
        leftMotor.stop()
        if(pickCount == 2):
            pickCount = 0
            #robotstate = ROBOT_LINING
            robotstate = ROBOT_IDLE
        else:
            hDriveMotor.spin_for(FORWARD, 5, TURNS, 75, RPM, wait = True)
            print("fruit 2")
            robotstate = ROBOT_SEARCHING


def handleLine():
    print("lining")
    global robotstate
    global largestFruit
    global Lineconstant
    Lineconstant = -1

    frontref = frontLine.reflectivity()
    backref = backLine.reflectivity()

    referror = frontref-backref - 4
    kr = .2
    refeffort = kr*referror

    hDriveMotor.spin(REVERSE, 100 * Lineconstant)
    leftMotor.spin(FORWARD, refeffort)
    rightMotor.spin(FORWARD, -refeffort)

    if(frontref > 35 and backref > 35):
        hDriveMotor.stop()
        leftMotor.spin_for(REVERSE, 4.5 * Lineconstant, TURNS, 60, RPM, wait = False)
        rightMotor.spin_for(FORWARD, 4.5 * Lineconstant, TURNS, 60, RPM, wait = True)
        hDriveMotor.spin_for(FORWARD, 2 * Lineconstant, TURNS, 100, RPM, wait = True)
    
    if vision.take_snapshot(Vision__PINK_BASKET):
        print("Basket?")
        basket = vision.largest_object()
        if(abs(basket.originX + basket.width - 150) < 15 and basket.width > 10):
            hDriveMotor.stop()
            robotstate = ROBOT_DROP_OFF
        

def dropFruit():
    global robotstate
    global fruitpick

    if(vision.take_snapshot(Vision__PINK_BASKET)): print("PINK!")
    rightMotor.spin(FORWARD, 100, RPM)
    leftMotor.spin(FORWARD, 100, RPM)
    if(vision.take_snapshot(Vision__PINK_BASKET) is None):
        print("no basket?")
        #Untested turn amount
        rightMotor.spin_for(FORWARD, 6.25, TURNS, 100, RPM, wait = False)
        leftMotor.spin_for(FORWARD, 6.25, TURNS, 100, RPM, wait = True)
        basketMotor.set_stopping(BRAKE)
        print("dropping off")
        basketMotor.spin(FORWARD, 75, RPM)
        wait(2000)
        basketMotor.stop()
        wait(2000, MSEC)
        basketMotor.spin_for(REVERSE, .4, TURNS, 45, RPM, wait = True)
        basketMotor.set_stopping(COAST)
        if(fruitpick >= 4):
            robotstate = ROBOT_IDLE
        else:
            robotstate = ROBOT_FIND_TREE


def linetofruit():
    global robotstate
    global largestFruit
    global Lineconstant
    global fruitpick

    # if(fruitpick == 1): Lineconstant = -1
    # else: Lineconstant = 1

    Lineconstant = 1

    frontref = frontLine.reflectivity()
    backref = backLine.reflectivity()

    referror = frontref-backref - 4
    kr = .2
    refeffort = kr*referror

    hDriveMotor.spin(REVERSE, 75 * Lineconstant)
    leftMotor.spin(FORWARD, -refeffort)
    rightMotor.spin(FORWARD, refeffort)

    if(frontref > 35 and backref > 35):
        hDriveMotor.stop()
        leftMotor.spin_for(REVERSE, 4.5 * Lineconstant, TURNS, 60, RPM, wait = False)
        rightMotor.spin_for(FORWARD, 4.5 * Lineconstant, TURNS, 60, RPM, wait = True)
        hDriveMotor.spin_for(FORWARD, 2 * Lineconstant, TURNS, 100, RPM, wait = True)
    
    if (fruitpick == 1):
        if(vision.take_snapshot(Vision__ORANGE_FRUIT)):
            if(abs(150-vision.largest_object().centerX) < 10):
                hDriveMotor.stop()
                leftMotor.stop()
                rightMotor.stop()
                verticalMotor.spin_for(FORWARD, 4.5, TURNS, 100, RPM, wait = True)
                fruitpick += 1
                robotstate = ROBOT_SEARCHING

    if (fruitpick == 2):
        if(vision.take_snapshot(Vision__LEMON)):
            if(abs(150-vision.largest_object().centerX) < 10):
                hDriveMotor.stop()
                leftMotor.stop()
                rightMotor.stop()
                verticalMotor.spin_for(FORWARD, 4.5, TURNS, 100, RPM, wait = True)
                fruitpick += 1
                robotstate = ROBOT_SEARCHING

    if (fruitpick == 3):
        if(vision.take_snapshot(Vision__LIME)):
            if(abs(150-vision.largest_object().centerX) < 10):
                hDriveMotor.stop()
                leftMotor.stop()
                rightMotor.stop()
                verticalMotor.spin_for(FORWARD, 4.5, TURNS, 100, RPM, wait = True)
                fruitpick += 1
                robotstate = ROBOT_SEARCHING


while True:
    if(robotstate == ROBOT_IDLE): handleIdle()
    if(robotstate == ROBOT_FIND_HILL): findHill()
    if(robotstate == ROBOT_LINE_HILL): lineHill()
    if(robotstate == ROBOT_FIND_ORCHARD) : findOrchard()
    if(robotstate == ROBOT_FIND_TREE): linetofruit()
    if(robotstate == ROBOT_SEARCHING): largestFruit = handleSearch()
    if(robotstate == ROBOT_CENTERING): center_fruit()
    if(robotstate == ROBOT_APPROACHING): handleApproach()
    if(robotstate == ROBOT_PICKING): handlePick()
    if(robotstate == ROBOT_FIND_LINE): findLine()
    if(robotstate == ROBOT_LINING): handleLine()
    if(robotstate == ROBOT_DROP_OFF): dropFruit()  
