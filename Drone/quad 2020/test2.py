import Quadcopter

quad = Quadcopter.Motors()

while True:
    data = quad.readdata()
    datas = data.split(",")
    print(datas)
    #sens = float(datas[1])
    #sens2 = float(datas[2])
