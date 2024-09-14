import time
t = 0.1

def stop():
    print("stop")

def forward():
    print("forward")
    time.sleep(t)
    stop()

def backward():
    print("bakward")
    time.sleep(t)
    stop()

def turnRight():
    print("turnright")
    time.sleep(t)
    stop()

def turnLeft():
    print("turnleft")
    time.sleep(t)
    stop()

def cleanup():
    stop()
