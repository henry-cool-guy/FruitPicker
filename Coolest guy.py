from vex import *

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
# Vision__LEMON = Signature (1, 2331, 3021, 2676, -4071, -3545, -3808, 2.5, 0)
# Vision__LIME = Signature (2, -6751, -4967, -5859, -4243, -3277, -3760, 2.5, 0)
# Vision__ORANGE_FRUIT = Signature (3, 6773, 8085, 7429, -2683, -2449, -2566, 2.5, 0)
# Vision__PINK_BASKET = Signature (4, 5031, 5219, 5125, 1419, 1739, 1579, 2.5, 0)

# Saturday signatures
Vision__LEMON = Signature (1, 2331, 3021, 2676, -4071, -3545, -3808, 2.5, 0)
Vision__LIME = Signature (2, -6751, -4967, -5859, -4243, -3277, -3760, 2.5, 0)
Vision__ORANGE_FRUIT = Signature (3, 6301, 7253, 6778, -2387, -2117, -2252, 2.5, 0)
Vision__PINK_BASKET = Signature (4, 5293, 5663, 5478, 1335, 1639, 1487, 2.5, 0)


vision = Vision(Ports.PORT3, 50, Vision__LEMON, Vision__LIME, Vision__ORANGE_FRUIT, Vision__PINK_BASKET)


rightMotor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
leftMotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
hDriveMotor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, True)
horizontalMotor = Motor(Ports.PORT17, GearSetting.RATIO_18_1)
verticalMotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)
basketMotor = Motor(Ports.PORT12, GearSetting.RATIO_18_1)

hDriveMotor.set_stopping(COAST)

frontLine = Line(brain.three_wire_port.e)
backLine = Line(brain.three_wire_port.f)
# FAKE PORTS, FIX LATER
leftButton = Bumper(brain.three_wire_port.c)

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

    horizontalMotor.reset_position()

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
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM, wait = True)
            vision.take_snapshot(Vision__LEMON)
            lemonheight = vision.largest_object().height
        if(vision.largest_object().originY + lemonheight > 195):
            verticalMotor.spin_for(REVERSE, .25, TURNS, 40, RPM,wait = True)
            vision.take_snapshot(Vision__LEMON)
            lemonheight = vision.largest_object().height
        if(lemonheight < 10):
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
        if(orangeheight < 10):
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
        verticalMotor.spin_for(REVERSE, .25, TURNS, 20, RPM, wait = True)
        return 0


def center_fruit():
    global largestFruit
    global robotstate

    if(largestFruit == 1): vision.take_snapshot(Vision__LEMON)
    elif(largestFruit == 2): vision.take_snapshot(Vision__LIME)
    elif(largestFruit == 3): vision.take_snapshot(Vision__ORANGE_FRUIT)

    idealx = 150
    idealy = 150


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

    if(errorx < 10 and errory < 10):
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

    goalHeight = 180
    height = vision.largest_object().height
    heightError = goalHeight-height
    kh = .6
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

    leftMotor.spin_for(FORWARD, 1, TURNS, 40, RPM, wait = False)
    rightMotor.spin_for(FORWARD, 1, TURNS, 40, RPM, wait = True)

    verticalMotor.spin_for(FORWARD, 1, TURNS, 200, RPM, wait = True)

    robotstate = ROBOT_FIND_LINE


def findLine():
    global robotstate
    leftMotor.spin(REVERSE, 50, RPM)
    rightMotor.spin(REVERSE, 50, RPM)
    print(backLine.reflectivity())
    print(frontLine.reflectivity())
    if (frontLine.reflectivity() > 40):
        robotstate = ROBOT_LINING
        rightMotor.stop()
        leftMotor.stop()
    # Future us problem: what if at no line area


    #re-center picker camera
    horizontalMotor.spin_for(FORWARD, horizontalMotor.position(), DEGREES, 20, RPM, wait = False)
    verticalMotor.spin_for(FORWARD, verticalMotor.position(), DEGREES, 20, RPM, wait = False)

def handleLine():
    global robotstate
    frontref = frontLine.reflectivity()
    backref = backLine.reflectivity()

    referror = frontref-backref - 3
    kr = .2
    refeffort = kr*referror

    print(hDriveMotor.power())
    print(hDriveMotor.torque())

    hDriveMotor.spin(FORWARD, 25)
    leftMotor.spin(FORWARD, -refeffort)
    rightMotor.spin(FORWARD, refeffort)

    if(frontref > 60 and backref > 60):
        hDriveMotor.stop()
        leftMotor.spin_for(REVERSE, 4.5, TURNS, 60, RPM, wait = False)
        rightMotor.spin_for(FORWARD, 4.5, TURNS, 60, RPM, wait = True)
        hDriveMotor.spin_for(FORWARD, .5, TURNS, 30, RPM, wait = True)
    if(leftButton.pressing() == True):
        # untested hdrive turn amount
        hDriveMotor.spin_for(REVERSE, 1, TURNS, 60, RPM, wait = True)
        leftMotor.spin_for(FORWARD, 4.25, TURNS, 60, RPM, wait = False)
        rightMotor.spin_for(REVERSE, 4.25, TURNS, 60, RPM, wait = True)
        robotstate = ROBOT_BASKET


def findBasket():
    global robotstate
    global largestFruit

    verticalMotor.spin_for(FORWARD, verticalMotor.position(), DEGREES, 20, RPM, wait = False)

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
    if(largestFruit == 1 and basket.originX + basket.width - lemonCheck.originX < 10):
        targetX = 150
        error = targetX-lemonCheck.originX
        kp = .5
        effort = kp*error
        hDriveMotor.spin(REVERSE, effort, RPM)
        if(error < 5):
            hDriveMotor.stop
            robotstate = ROBOT_DROP_OFF
    if(largestFruit == 2 and basket.originX + basket.width - limeCheck.originX < 10):
        targetX = 150
        error = targetX-limeCheck.originX
        kp = .5
        effort = kp*error
        hDriveMotor.spin(REVERSE, effort, RPM)
        if(error < 5):
            hDriveMotor.stop
            robotstate = ROBOT_DROP_OFF
        if(largestFruit == 3 and basket.originX + basket.width - orangeCheck.originX < 10):
            targetX = 150
            error = targetX-orangeCheck.originX
            kp = .5
            effort = kp*error
            hDriveMotor.spin(REVERSE, effort, RPM)
        if(error < 5):
            hDriveMotor.stop
            robotstate = ROBOT_DROP_OFF
        

def dropFruit():
    global robotstate
    rightMotor.spin(FORWARD, 20, RPM)
    leftMotor.spin(FORWARD, 20, RPM)
    if(vision.take_snapshot(Vision__PINK_BASKET) is None):
        rightMotor.spin_for(FORWARD, 3, TURNS, 20, RPM)
        leftMotor.spin_for(FORWARD, 3, TURNS, 20, RPM)
        basketMotor.spin(FORWARD, 200)
        if basketMotor.power() > 3: 
            basketMotor.stop()
            wait(2000, MSEC)
            basketMotor.spin_for(REVERSE,360,100,RPM, wait = False)


while True:
    if(robotstate == ROBOT_IDLE): handleIdle()
    if(robotstate == ROBOT_SEARCHING): largestFruit = handleSearch()
    if(robotstate == ROBOT_CENTERING): center_fruit()
    if(robotstate == ROBOT_APPROACHING): handleApproach()
    if(robotstate == ROBOT_PICKING): handlePick()
    if(robotstate == ROBOT_FIND_LINE): findLine()
    if(robotstate == ROBOT_LINING): handleLine()
    if(robotstate == ROBOT_BASKET):
        print("yoppee")
        robotstate = ROBOT_IDLE
        # findBasket()
    if(robotstate == ROBOT_DROP_OFF): dropFruit()  
