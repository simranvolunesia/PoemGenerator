from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/poemgenerator", methods=['POST'])
def poemgenerator():

    try:
        inputs = request.form["inputs"]
        no_of_chars = int(request.form["no_of_chars"])

        data = open("Shakespeare.txt")
        s = ""
        for i in data:
            s = s + i
        T = {}
        def generateTransition(data, k=4):
            for i in range(len(data) - k):
                X = data[i:i + k]
                Y = data[i + k]

                if T.get(X) is None:
                    T[X] = {}
                    T[X][Y] = 1
                else:
                    if T[X].get(Y) is None:
                        T[X][Y] = 1
                    else:
                        T[X][Y] += 1
            return T

        T = generateTransition(s)

        def poem(inputs):
            possible_char = list(T[inputs[-4:]].keys())
            possible_freq = list(T[inputs[-4:]].values())
            probab = [freq / sum(possible_freq) for freq in possible_freq]
            return np.random.choice(possible_char, p=probab)

        for i in range(no_of_chars):
            inputs = inputs + poem(inputs)
        a = []
        for i in inputs.expandtabs().splitlines():
            mydict = {"line": i}
            a.append(mydict)
        return render_template("result.html",inputs=a)
    except:
        return render_template("exception.html")

if __name__=="__main__":
    app.run(debug=True)

