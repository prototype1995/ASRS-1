from asrs import asrsOps as asrs
def calibrate(slots=120):
    asrs.auto_home()
    l = []
    asrs.enc.start()
    for i in range(slots):
        ch = input("{} : Enter/n".format(i))
        if ch == "n":
            break
        l.append(asrs.enc.encoderValue*360)
    asrs.enc.stop()
    return l


if __name__ == "__main__":

    print("1. Storage Calibration\n2.Retrieval Calibration\n")
    ch = input("Enter choice: ")
    if ch == "1":
        print("Storage Calibration Starting...\nPress Enter to calibtrate slot Or Input 'n' to abort at current position")
        m = calibrate(120)
        print("storage_pos = ", m)
    elif ch == "2":
        print("Retrieval Calibration Starting...\nPress Enter to calibtrate slot Or Input 'n' to abort at current position")
        m = calibrate(120)
        print("retrieval_pos = ", m)

