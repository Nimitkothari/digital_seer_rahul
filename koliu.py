from flask import Flask,send_from_directory,request,Response
from flask_cors import CORS
import os
path = os.getcwd()
print(path)
port = int(os.getenv("PORT", 3030))
upload_folder = path
ALLOWED_EXTENSIONS = set(['pkl','txt','csv'])
app = Flask(__name__)
import json

def linear_function(d):
    # pos=0
    base = []
    diff = 0
    base1 = d["day_of_month"]
    base = d["energy"]
    size = len(base)
    print
    size
    # print base
    start = base[0]
    # print start
    count = 0
    while (count != size):
        for i in base:
            diff = abs(i - start)
            print
            diff
            count += 1

            if (diff > 5):
                check1 = abs(base[base.index(i) + 1] - start)
                print("check1=" + str(check1))
                check2 = abs(base[base.index(i) + 2] - start)
                print("check2=" + str(check2))
                check3 = abs(base[base.index(i) + 3] - start)
                print("check3=" + str(check3))
                if (check1 > 5 and check2 > 5 and check3 > 5):
                    print(" in check")
                    print("count=" + str(count))
                    start = i
                    base = base[count - 1:size - 1]
                    base1 = base1[count - 1:size - 1]
                    # base=base[count-1:size-1]
                    print
                    base
                    print
                    base1
                    print("start=" + str(start))
                    break

    data = set()
    # converting the json x and y values into set data
    data = (zip(base1, base))
    print (data)
    # variables to store average
    avgx = 0.0
    avgy = 0.0
    # loop to calculate the average
    for i in data:
        avgx += i[0] / len(data)
        avgy += i[1] / len(data)

    # least mean square logic to calculate the best fit line
    totalxx = 0
    totalxy = 0
    for i in data:
        totalxx += (i[0] - avgx) ** 2
        totalxy += (i[0] - avgx) * (i[1] - avgy)
    m = totalxy / totalxx
    b = avgy - m * avgx
    y = d["energy_value"]
    d["line_equation"] = "y = " + str(m) + "x + " + str(b)
    d["estimated_days"] = str((y - b) / m)

    # print(mse(base1,base,m,b))
    return(json.dumps(d))

if __name__ == '__main__':
    json_data = {"energy":[250,251,255,245,239,248,246,249,237,239,240,235,237,240,236,225,245,236,250,
248,
246,
247,
247,
248,
247,
248,
247,
247,247,247,247],"day_of_month":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],"predict":225}
    json_object=linear_function(json_data)
    print(json_object)
    app.run(debug=True, port=port)