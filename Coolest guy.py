from vex import *

brain=Brain()

controller = Controller()

Vision__LEMON = Signature (1, 1709, 2161, 1936, -3907, -3711, -3808, 3.6, 0)
Vision__LIME = Signature (2, -6605, -6003, -6304, -3673, -2977, -3326, 3.9, 0)
Vision__ORANGE_FRUIT = Signature (3, 7193, 7909, 7551, -2541, -2153, -2347, 3.6, 0)
Vision__PINK_BASKET = Signature (4, 4843, 5171, 5007, 855, 1253, 1054, 3, 0)


vision = Vision(Ports.PORT3, 28, Vision__LEMON, Vision__LIME, Vision__ORANGE_FRUIT, Vision__PINK_BASKET)

rightMotor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
leftMotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
hDriveMotor = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)
horizontalMotor = Motor(Ports.PORT17, GearSetting.RATIO_18_1)
verticalMotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)
basketMotor = Motor(Ports.PORT12, GearSetting.RATIO_18_1)

hDriveMotor.set_stopping(COAST)

frontLine = Line(brain.three_wire_port.e)
backLine = Line(brain.three_wire_port.f)
gyro = Gyro(brain.three_wire_port.a)

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
        fruitpick = 1
        robotstate = ROBOT_FIND_HILL
       
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
        hDriveMotor.spin_for(FORWARD, 12, TURNS, 100, RPM, wait = True)
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
        if(lemonheight < 40):
            lemonheight = 0
    else: lemonheight = 0

    if(vision.take_snapshot(Vision__ORANGE_FRUIT)):
        print("orange?")
        orangeheight = vision.largest_object().height
        if(orangeheight < 40):
            orangeheight = 0
    else: orangeheight = 0

    if(vision.take_snapshot(Vision__LIME)):
        print("lime?")
        limeheight = vision.largest_object().height
        if(limeheight < 40):
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
        verticalMotor.spin_for(REVERSE, .3, TURNS, 100, RPM, wait = True)
        return 0


def center_fruit():
    global largestFruit
    global robotstate

    if(largestFruit == 1): vision.take_snapshot(Vision__LEMON)
    elif(largestFruit == 2): vision.take_snapshot(Vision__LIME)
    elif(largestFruit == 3): vision.take_snapshot(Vision__ORANGE_FRUIT)

    idealx = 170
    idealy = 133

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

    if(errorx < 3 and errory < 3):
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
    kh = .45
    approachEffort = kh*heightError

    if(heightError < 10):
        leftMotor.stop()
        rightMotor.stop()
        robotstate = ROBOT_PICKING

    leftMotor.spin(FORWARD, approachEffort)
    rightMotor.spin(FORWARD, approachEffort)


def handlePick():
    print("picking")
    global robotstate
    global pickCount

    verticalMotor.spin_for(FORWARD, 2, TURNS, 75, RPM, wait = True)
    horizontalMotor.spin_for(REVERSE, horizontalMotor.position(), DEGREES, 100, RPM, wait = True)

    pickCount = pickCount + 1
    robotstate = ROBOT_FIND_LINE


def findLine():
    global robotstate
    global pickCount
    global fruitpick
    aligned = 0

    leftMotor.spin(REVERSE, 50, RPM)
    rightMotor.spin(REVERSE, 50, RPM)
    if (backLine.reflectivity() > 10):
        rightMotor.stop()
        leftMotor.stop()
        if(pickCount == 2):
            pickCount = 0
            verticalMotor.spin_for(REVERSE, verticalMotor.position(), DEGREES, 50, RPM, wait = True)
            # verticalMotor.spin_for(FORWARD, 1, TURNS, 50, RPM, wait = True)
            robotstate = ROBOT_LINING
        else:
            if(fruitpick == 2):
                hDriveMotor.spin_for(FORWARD, 7, TURNS, 75, RPM, wait = True)
            else:
                hDriveMotor.spin_for(REVERSE, 5, TURNS, 75, RPM, wait = True)
            # while hDriveMotor.is_spinning:
            #     robotalign()
            leftMotor.stop()
            rightMotor.stop()
            print("fruit 2")
            robotstate = ROBOT_SEARCHING


def handleLine():
    global robotstate
    global largestFruit
    global Lineconstant
    Lineconstant = -1

    frontref = frontLine.reflectivity()
    backref = backLine.reflectivity()

    referror = frontref-backref #- 4
    # if(abs(referror) > 25): kr = .6
    # else: 
    kr = .4
    refeffort = kr*referror

    print("front:", frontref, "bacK:", backref, "diff:", referror)

    hDriveMotor.spin(REVERSE, 150 * Lineconstant)
    leftMotor.spin(FORWARD, -refeffort)
    rightMotor.spin(FORWARD, refeffort)

    if(frontref > 30 and backref > 30):
        hDriveMotor.stop()
        leftMotor.spin_for(REVERSE, 4.6 * Lineconstant, TURNS, 60, RPM, wait = False)
        rightMotor.spin_for(FORWARD, 4.6 * Lineconstant, TURNS, 60, RPM, wait = True)
        hDriveMotor.spin_for(REVERSE, 1 * Lineconstant, TURNS, 100, RPM, wait = True)
        leftMotor.spin_for(FORWARD, 1.25, TURNS, 60, RPM, wait = False)
        rightMotor.spin_for(FORWARD, 1.25, TURNS, 60, RPM, wait = True)
    
    if vision.take_snapshot(Vision__PINK_BASKET):
        print("Basket?")
        basket = vision.largest_object()
        if(abs(basket.originX + basket.width - 150) < 15 and basket.width > 15):
            hDriveMotor.spin_for(FORWARD, 2, TURNS, 150, RPM)
            hDriveMotor.stop()
            # verticalMotor.spin_for(REVERSE, verticalMotor.position(), DEGREES, 50, RPM, wait = True)
            # verticalMotor.spin_for(FORWARD, 1, TURNS, 50, RPM, wait = True)
            robotstate = ROBOT_DROP_OFF
        

def dropFruit():
    global robotstate
    global fruitpick
    

    if(vision.take_snapshot(Vision__PINK_BASKET)): print("PINK!")
    rightMotor.spin(FORWARD, 100, RPM)
    leftMotor.spin(FORWARD, 100, RPM)
    pinkcount = 0
    if(vision.take_snapshot(Vision__PINK_BASKET) is None):
        print("no basket?")
        rightMotor.spin_for(FORWARD, 6.9, TURNS, 100, RPM, wait = False)
        leftMotor.spin_for(FORWARD, 6.9, TURNS, 100, RPM, wait = True)
        basketMotor.set_stopping(BRAKE)
        print("dropping off")
        basketMotor.spin(FORWARD, 90, RPM)
        wait(2000)
        basketMotor.stop()
        wait(1000)
        # basketMotor.spin_for(REVERSE, .3, TURNS, 45, RPM, wait = True)
        basketMotor.set_stopping(COAST)
        if(fruitpick >= 4):
            robotstate = ROBOT_IDLE
        else:
            while(backLine.reflectivity() < 10):
                rightMotor.spin(REVERSE, 50, RPM)
                leftMotor.spin(REVERSE, 50, RPM)
            # rightMotor.spin_for(FORWARD, .5, TURNS, 100, RPM, wait = False)
            # leftMotor.spin_for(FORWARD, .5, TURNS, 100, RPM, wait = True)
            rightMotor.stop()
            leftMotor.stop()
            robotstate = ROBOT_FIND_TREE


def linetofruit():
    global robotstate
    global largestFruit
    global Lineconstant
    global fruitpick

    if(fruitpick == 1): Lineconstant = -1
    else: Lineconstant = 1

    frontref = frontLine.reflectivity()
    backref = backLine.reflectivity()

    referror = frontref-backref#-5
    # if(abs(referror) > 25): kr = .5
    # else: 
    kr = .4
    refeffort = kr*referror

    print("front:", frontref, "bacK:", backref, "diff:", referror)

    hDriveMotor.spin(REVERSE, 150 * Lineconstant)
    leftMotor.spin(FORWARD, refeffort * Lineconstant)
    rightMotor.spin(FORWARD, -refeffort * Lineconstant)

    if(frontref > 35 and backref > 35):
        hDriveMotor.stop()
        leftMotor.spin_for(REVERSE, 4.5 * Lineconstant, TURNS, 60, RPM, wait = False)
        rightMotor.spin_for(FORWARD, 4.5 * Lineconstant, TURNS, 60, RPM, wait = True)
        hDriveMotor.spin_for(FORWARD, 2 * Lineconstant, TURNS, 100, RPM, wait = True)
    
    if (fruitpick == 1):
        if(vision.take_snapshot(Vision__ORANGE_FRUIT)):
            if(abs(150-vision.largest_object().centerX) < 10 and vision.largest_object().height >10):
                hDriveMotor.stop()
                leftMotor.stop()
                rightMotor.stop()
                hDriveMotor.spin_for(FORWARD, 2.5, TURNS, 100, RPM, wait = False)
                while hDriveMotor.is_spinning():
                    robotalign()
                leftMotor.spin_for(REVERSE, 2, TURNS, 100, RPM, wait = False)
                rightMotor.spin_for(REVERSE, 2, TURNS, 100, RPM, wait = True)
                verticalMotor.spin_for(FORWARD, 2, TURNS, 100, RPM, wait = True)
                leftMotor.stop()
                rightMotor.stop()
                fruitpick += 1
                robotstate = ROBOT_SEARCHING

    if (fruitpick == 2):
        if(vision.take_snapshot(Vision__LEMON)):
            if(abs(150-vision.largest_object().centerX) < 10 and vision.largest_object().height >10):
                hDriveMotor.stop()
                leftMotor.stop()
                rightMotor.stop()
                hDriveMotor.spin_for(REVERSE, 1.25, TURNS, 100, RPM, wait = True)
                # while hDriveMotor.is_spinning():
                #     robotalign()
                leftMotor.spin_for(REVERSE, 2, TURNS, 100, RPM, wait = False)
                rightMotor.spin_for(REVERSE, 2, TURNS, 100, RPM, wait = True)
                verticalMotor.spin_for(FORWARD, 2, TURNS, 100, RPM, wait = True)
                leftMotor.stop()
                rightMotor.stop()
                fruitpick += 1
                robotstate = ROBOT_SEARCHING

    if (fruitpick == 3):
        if(vision.take_snapshot(Vision__LIME)):
            if(abs(150-vision.largest_object().centerX) < 10 and vision.largest_object().height >10):
                hDriveMotor.stop()
                leftMotor.stop()
                rightMotor.stop()
                hDriveMotor.spin_for(REVERSE, 1.25, TURNS, 100, RPM, wait = False)
                while hDriveMotor.is_spinning():
                    robotalign()
                leftMotor.spin_for(REVERSE, 2, TURNS, 100, RPM, wait = False)
                rightMotor.spin_for(REVERSE, 2, TURNS, 100, RPM, wait = True)
                verticalMotor.spin_for(FORWARD, 2, TURNS, 100, RPM, wait = True)
                leftMotor.stop()
                rightMotor.stop()
                fruitpick += 1
                robotstate = ROBOT_SEARCHING

def robotalign():
    global Lineconstant
    frontref = frontLine.reflectivity()
    backref = backLine.reflectivity()

    referror = frontref-backref - 4
    kr = .15
    refeffort = kr*referror

    print("front:", frontref, "bacK:", backref, "diff:", referror)

    leftMotor.spin(FORWARD, +refeffort * Lineconstant)
    rightMotor.spin(FORWARD, -refeffort * Lineconstant)
    
while True:
    # while gyro.is_calibrating():
    #     brain.screen.clear()
    #     brain.screen.print("Gyro Sensor is calibrating.")
    #     wait(50, MSEC)
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
