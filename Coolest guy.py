
# Library imports
from vex import *


# Brain should be defined by default
brain=Brain()


controller = Controller()

# Monday signatures
# Vision__LEMON = Signature (1, 3875, 4701, 4288, -4909, -4543, -4726, 2.5, 0)
# Vision__LIME = Signature (2, -5741, -5009, -5375, -5881, -5393, -5637, 2.5, 0)
# Vision__ORANGE_FRUIT = Signature (3, 8847, 10363, 9605, -3589, -3147, -3368, 2.5, 0)

# Tuesday signatures
# Vision__LEMON = Signature (1, 3027, 3633, 3330, -3801, -3577, -3689, 2.5, 0)
# Vision__LIME = Signature (2, -5957, -5271, -5614, -3933, -3429, -3681, 2.5, 0)
# Vision__ORANGE_FRUIT = Signature (3, 6773, 8085, 7429, -2683, -2449, -2566, 2.5, 0)

# Friday Signatures
Vision__LEMON = Signature (1, 2331, 3021, 2676, -4071, -3545, -3808, 2.5, 0)
Vision__LIME = Signature (2, -6751, -4967, -5859, -4243, -3277, -3760, 2.5, 0)
Vision__ORANGE_FRUIT = Signature (3, 6773, 8085, 7429, -2683, -2449, -2566, 2.5, 0)
Vision__PINK_BASKET = Signature (4, 5031, 5219, 5125, 1419, 1739, 1579, 2.5, 0)


vision = Vision(Ports.PORT2, 50, Vision__LEMON, Vision__LIME, Vision__ORANGE_FRUIT, Vision__PINK_BASKET)


rightMotor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
leftMotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
hDriveMotor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, True)
horizontalMotor = Motor(Ports.PORT17, GearSetting.RATIO_18_1)
verticalMotor = Motor(Ports.PORT16, GearSetting.RATIO_18_1)
basketMotor = Motor(Ports.PORT12, GearSetting.RATIO_18_1)

# FAKE PORTS, FIX LATER
leftLine = Line(brain.three_wire_port.a)
rightLine = Line(brain.three_wire_port.b)
button = Bumper(brain.three_wire_port.c)

ROBOT_IDLE = 0
ROBOT_SEARCHING = 1
ROBOT_CENTERING = 2
ROBOT_APPROACHING = 3
ROBOT_PICKING = 4
ROBOT_FIND_LINE = 5
ROBOT_LINING = 6
ROBOT_BASKET = 7
ROBOT_DROP_OFF = 8

largestFruit = 0

robotstate = ROBOT_IDLE

def handleL1():
    global robotstate
    print("button L1")
    if(robotstate != ROBOT_IDLE):
        leftMotor.stop()
        rightMotor.stop()
        horizontalMotor.stop()
        verticalMotor.stop()
        robotstate = ROBOT_IDLE
        print("idle")
    else:
        robotstate = ROBOT_SEARCHING
        print("searching")
       
controller.buttonL1.pressed(handleL1)

def handleIdle():
    rightMotor.stop()
    leftMotor.stop()
    verticalMotor.stop()
    horizontalMotor.stop()
    basketMotor.stop()
    hDriveMotor.stop()

def handleSearch():
    global robotstate
   
    if(vision.take_snapshot(Vision__LEMON)):
        print("lemon?")
        lemonheight = vision.largest_object().height
        if(vision.largest_object().originY < 5):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM)
            vision.take_snapshot(Vision__LEMON)
            lemonheight = vision.largest_object().height
        if(vision.largest_object().originY + lemonheight > 195):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM)
            vision.take_snapshot(Vision__LEMON)
            lemonheight = vision.largest_object().height
        if(lemonheight < 10):
            lemonheight = 0
    else: lemonheight = 0


    if(vision.take_snapshot(Vision__ORANGE_FRUIT)):
        print("orange?")
        orangeheight = vision.largest_object().height
        if(vision.largest_object().originY < 5):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM)
            vision.take_snapshot(Vision__ORANGE_FRUIT)
            orangeheight = vision.largest_object().height
        if(vision.largest_object().originY + orangeheight > 195):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM)
            vision.take_snapshot(Vision__ORANGE_FRUIT)
            orangeheight = vision.largest_object().height
        if(orangeheight < 10):
            orangeheight = 0
    else: orangeheight = 0


    if(vision.take_snapshot(Vision__LIME)):
        print("lime?")
        limeheight = vision.largest_object().height
        if(vision.largest_object().originY < 5):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM)
            vision.take_snapshot(Vision__LIME)
            limeheight = vision.largest_object().height
        if(vision.largest_object().originY + limeheight > 195):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM)
            vision.take_snapshot(Vision__LIME)
            limeheight = vision.largest_object().height
        if(limeheight < 10):
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
        verticalMotor.spin_for(REVERSE, .25, TURNS, 20, RPM, True)
        return 0


def center_fruit():
    global largestFruit
    global robotstate

    if(largestFruit == 1): vision.take_snapshot(Vision__LEMON)
    elif(largestFruit == 2): vision.take_snapshot(Vision__LIME)
    elif(largestFruit == 3): vision.take_snapshot(Vision__ORANGE_FRUIT)

    idealx = 150
    # UNTESTED VALUE
    idealy = 120


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
    kx = .75
    ky = .75
    effortx = kx*errorx
    efforty = ky*errory

    if(errorx < 5 and errory < 5):
        horizontalMotor.stop()
        verticalMotor.stop()
        robotstate = ROBOT_APPROACHING


    horizontalMotor.spin(REVERSE, effortx)
    verticalMotor.spin(REVERSE, efforty)
    sleep(50)


def handleApproach():
    global robotstate
    global largestFruit

    horizontalMotor.stop()
    verticalMotor.stop()

    if(largestFruit == 1): vision.take_snapshot(Vision__LEMON)
    elif(largestFruit == 2): vision.take_snapshot(Vision__LIME)
    elif(largestFruit == 3): vision.take_snapshot(Vision__ORANGE_FRUIT)

    goalHeight = 180
    height = vision.largest_object().height
    heightError = goalHeight-height
    kh = .5
    approachEffort = kh*heightError

    if(heightError < 5):
        leftMotor.stop()
        rightMotor.stop()
        robotstate = ROBOT_PICKING

    leftMotor.spin(FORWARD, approachEffort)
    rightMotor.spin(FORWARD, approachEffort)


def handlePick():
    print("picking")
    global robotstate
    # verticalMotor.spin_for(REVERSE, .6, TURNS, 20, RPM)

    leftMotor.spin_for(FORWARD, 1.5, TURNS, 40, RPM, False)
    rightMotor.spin_for(FORWARD, 1.5, TURNS, 40, RPM, True)

    verticalMotor.spin_for(FORWARD, 1.5, TURNS, 20, RPM)

    robotstate = ROBOT_IDLE
    verticalMotor.stop()
    horizontalMotor.stop()
    leftMotor.stop()
    rightMotor.stop()


def findLine():
    global robotstate
    leftMotor.spin(REVERSE, 20, RPM)
    rightMotor.spin(REVERSE, 20, RPM)
    if(rightLine.reflectivity() > 35 or leftLine.reflectivity() > 35):
        while(rightLine.reflectivity() != leftLine.reflectivity or 
              leftLine.reflectivity() < 10):
            leftMotor.spin(REVERSE, 20, RPM)
            rightMotor.spin(FORWARD, 20, RPM)
        robotstate = ROBOT_LINING
    if(button.pressing() == True):
        robotstate = ROBOT_BASKET
    rightMotor.stop()
    leftMotor.stop()

def handleLine():
    global robotstate
    leftref = leftLine.reflectivity()
    rightref = rightLine.reflectivity()

    referror = leftref-rightref
    kr = 1
    refeffort = kr*referror

    leftMotor.spin(REVERSE, 50-refeffort)
    rightMotor.spin(REVERSE, 50+refeffort)

    if(leftref > 35 and rightref > 35):
        #turn 90 degrees (untested)
        leftMotor.spin_for(REVERSE, 5, TURNS, 40, RPM)
        rightMotor.spin_for(FORWARD, 5, TURNS, 40, RPM)
    if(button.pressing() == True):
        robotstate = ROBOT_BASKET


def findBasket():
    global robotstate
    global largestFruit

    leftMotor.spin_for(FORWARD, 5, TURNS, 40, RPM)
    rightMotor.spin_for(FORWARD, 5, TURNS, 40, RPM)

    verticalMotor.spin_for(FORWARD, verticalMotor.position(), DEGREES, 20, RPM)

    #I DON"T KNOW IF REV OR FORWARD
    hDriveMotor.spin(FORWARD, 10, RPM)

    vision.take_snapshot(Vision__PINK_BASKET)
    basket = vision.largest_object()
    vision.take_snapshot(Vision__LEMON)
    lemonCheck = vision.largest_object()
    vision.take_snapshot(Vision__LIME)
    limeCheck = vision.largest_object()
    vision.take_snapshot(Vision__ORANGE_FRUIT)
    orangeCheck = vision.largest_object()
    if(largestFruit == 1 and basket.originX + basket.width == lemonCheck.originX):
        targetX = 150
        error = targetX-lemonCheck.originX
        kp = .5
        effort = kp*error
        hDriveMotor.spin(REVERSE, effort, RPM)
        if(error < 5):
            hDriveMotor.stop
            robotstate = ROBOT_DROP_OFF
    if(largestFruit == 2 and basket.originX + basket.width == limeCheck.originX):
        targetX = 150
        error = targetX-limeCheck.originX
        kp = .5
        effort = kp*error
        hDriveMotor.spin(REVERSE, effort, RPM)
        if(error < 5):
            hDriveMotor.stop
            robotstate = ROBOT_DROP_OFF
        if(largestFruit == 3 and basket.originX + basket.width == orangeCheck.originX):
        targetX = 150
        error = targetX-orangeCheck.originX
        kp = .5
        effort = kp*error
        hDriveMotor.spin(REVERSE, effort, RPM)
        if(error < 5):
            hDriveMotor.stop
            robotstate = ROBOT_DROP_OFF
        

while True:
    if(robotstate == ROBOT_IDLE): handleIdle()
    if(robotstate == ROBOT_SEARCHING): largestFruit = handleSearch()
    if(robotstate == ROBOT_CENTERING): center_fruit()
    if(robotstate == ROBOT_APPROACHING): handleApproach()
    if(robotstate == ROBOT_PICKING): handlePick()
    if(robotstate == ROBOT_FIND_LINE): findLine()
    if(robotstate == ROBOT_LINING): handleLine()
    if(robotstate == ROBOT_BASKET): findBasket()
#    if(robotstate == ROBOT_DROP_OFF):  