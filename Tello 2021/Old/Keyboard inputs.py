import keyboard
while True:
    if keyboard.is_pressed("8"):
        print("8")
    elif keyboard.is_pressed("2"):
        print("2")
    elif keyboard.is_pressed("esc"):
        print("esc")
    elif keyboard.is_pressed("l") or keyboard.is_pressed("backspace"):
        print("l")
    elif keyboard.is_pressed("t") or keyboard.is_pressed("tab"):
        print("T or Tab")
    elif keyboard.is_pressed("space"):
        print("Space")
    elif keyboard.is_pressed("shift"):
        print("Shift")
    elif keyboard.is_pressed("e"):
        print("e")
    elif keyboard.is_pressed("q"):
        print("q")
    elif keyboard.is_pressed("w"):
        print("w")
    elif keyboard.is_pressed("s"):
        print("s")
    elif keyboard.is_pressed("d"):
        print("d")
    elif keyboard.is_pressed("a"):
        print("a")
    else:
        print("Stop")