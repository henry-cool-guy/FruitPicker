from vex import *

brain=Brain()

controller = Controller()


Vision__LEMON = Signature (1, 2331, 3021, 2676, -4071, -3545, -3808, 2.5, 0)
Vision__LIME = Signature (2, -6751, -4967, -5859, -4243, -3277, -3760, 2.5, 0)
Vision__ORANGE_FRUIT = Signature (3, 6301, 7253, 6778, -2387, -2117, -2252, 2.5, 0)
Vision__PINK_BASKET = Signature (4, 4333, 4819, 4576, 885, 1199, 1042, 2.500, 0) #(4, 1629, 2133, 1881, 1031, 1391, 1211, 2.5, 0)

vision = Vision(Ports.PORT3, 40, Vision__LEMON, Vision__LIME, Vision__ORANGE_FRUIT, Vision__PINK_BASKET)


rightMotor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
leftMotor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
hDriveMotor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, True)
horizontalMotor = Motor(Ports.PORT17, GearSetting.RATIO_18_1)
verticalMotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1)
basketMotor = Motor(Ports.PORT12, GearSetting.RATIO_18_1)

hDriveMotor.set_stopping(COAST)

frontLine = Line(brain.three_wire_port.e)
backLine = Line(brain.three_wire_port.f)

ROBOT_IDLE = 0
ROBOT_SEARCHING = 1
ROBOT_CENTERING = 2
ROBOT_APPROACHING = 3
ROBOT_PICKING = 4
ROBOT_FIND_LINE = 5
ROBOT_LINING = 6
ROBOT_DROP_OFF = 7
OTHER = 8

largestFruit = 0

robotstate = ROBOT_IDLE

def handleL1():
    global robotstate
    global largestFruit
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
        robotstate = ROBOT_DROP_OFF
        # robotstate = ROBOT_SEARCHING
        # print("searching")
       
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
    idealy = 145


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

    verticalMotor.spin_for(REVERSE, verticalMotor.position(), DEGREES, 100, RPM, wait = True)
    horizontalMotor.spin_for(REVERSE, horizontalMotor.position(), DEGREES, 100, RPM, wait = True)

    robotstate = ROBOT_FIND_LINE


def findLine():
    global robotstate
    leftMotor.spin(REVERSE, 50, RPM)
    rightMotor.spin(REVERSE, 50, RPM)
    print(backLine.reflectivity())
    print(frontLine.reflectivity())
    if (frontLine.reflectivity() > 20):
        robotstate = ROBOT_LINING
        rightMotor.stop()
        leftMotor.stop()
    # Future us problem: what if at no line area


def handleLine():
    print("lining")
    global robotstate
    global largestFruit

    frontref = frontLine.reflectivity()
    backref = backLine.reflectivity()

    referror = frontref-backref - 4
    kr = .2
    refeffort = kr*referror

    # print(hDriveMotor.power())
    # print(hDriveMotor.torque())

    hDriveMotor.spin(REVERSE, 25)
    leftMotor.spin(FORWARD, refeffort)
    rightMotor.spin(FORWARD, -refeffort)

    if(frontref > 30 and backref > 30):
        hDriveMotor.stop()
        leftMotor.spin_for(REVERSE, 4.5, TURNS, 60, RPM, wait = False)
        rightMotor.spin_for(FORWARD, 4.5, TURNS, 60, RPM, wait = True)
        hDriveMotor.spin_for(FORWARD, .5, TURNS, 30, RPM, wait = True)
    # if(leftButton.pressing() == True):
    #     # untested hdrive turn amount
    #     hDriveMotor.spin_for(REVERSE, 1, TURNS, 60, RPM, wait = True)
    #     leftMotor.spin_for(FORWARD, 4.5, TURNS, 60, RPM, wait = False)
    #     rightMotor.spin_for(REVERSE, 4.5, TURNS, 60, RPM, wait = True)
    #     verticalMotor.spin_for(FORWARD, verticalMotor.position(), DEGREES, 20, RPM, wait = False)
    #     robotstate = ROBOT_BASKET
    
    if vision.take_snapshot(Vision__PINK_BASKET):
        print("Basket?")
        basket = vision.largest_object()
        if(abs(basket.originX + basket.width - 150) < 15):
            hDriveMotor.stop()
            robotstate = ROBOT_DROP_OFF
        

def dropFruit():
    global robotstate
    if(vision.take_snapshot(Vision__PINK_BASKET)): print("PINK!")
    rightMotor.spin(FORWARD, 100, RPM)
    leftMotor.spin(FORWARD, 100, RPM)
    if(vision.take_snapshot(Vision__PINK_BASKET) is None):
        print("no basket?")
        #Untested turn amount
        rightMotor.spin_for(FORWARD, 8, TURNS, 100, RPM, wait = False)
        leftMotor.spin_for(FORWARD, 8, TURNS, 100, RPM, wait = True)
        basketMotor.set_stopping(BRAKE)
        print("dropping off")
        basketMotor.spin(FORWARD, 75, RPM)
        print(basketMotor.power())
        print(basketMotor.torque())
        wait(2000)
        basketMotor.stop()
        wait(2000, MSEC)
        basketMotor.spin_for(REVERSE, .4, TURNS, 45, RPM, wait = True)
        basketMotor.set_stopping(COAST)
        robotstate = ROBOT_IDLE


while True:
    if(robotstate == ROBOT_IDLE): handleIdle()
    if(robotstate == ROBOT_SEARCHING): largestFruit = handleSearch()
    if(robotstate == ROBOT_CENTERING): center_fruit()
    if(robotstate == ROBOT_APPROACHING): handleApproach()
    if(robotstate == ROBOT_PICKING): handlePick()
    if(robotstate == ROBOT_FIND_LINE): findLine()
    if(robotstate == ROBOT_LINING): handleLine()
    if(robotstate == ROBOT_DROP_OFF): dropFruit()  
