import Quadcopter

quad = Quadcopter.Motors()

while True:
    while len(quad.readdata().split(",")) <= 1:
        print("wait")
    
    data = quad.readdata()
    datas = data.split(",")

    sens = float(datas[1])
    sens2 = float(datas[2])
    print(sens,sens2)
    
    #sens = float(datas[1])
    #sens2 = float(datas[2])
