from flask import Flask,send_from_directory,request,Response
from flask_cors import CORS
import os
import json
path = os.getcwd()
print(path)
port = int(os.getenv("PORT", 3030))
upload_folder = path
ALLOWED_EXTENSIONS = set(['pkl','txt','csv'])
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = upload_folder

def train_data(json_data):
    try:
        print("Reading data")
        d = json_data
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
        #print
        #data
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
        y = d["predict"]
        d["line_equation"] = "y = " + str(m) + "x + " + str(b)
        d["estimated_day"] = str((y - b) / m)
        print(json.dumps(d))
        return (json.dumps(d))

    except Exception as e:
        print(e)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json(force=True)
        json_object = train_data(json_data)
        return json_object
    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.run(port=port)