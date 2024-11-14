from flask import Flask, request, jsonify
import sys
try:
    file = sys.argv[1]
    if file != "data.txt":
        sys.exit("Invalid command-line argument")
except:
    sys.exit("Invalid command-line argument")
app = Flask(__name__)
myDict = {
            "ids" : []
        }
years = {
        "2024" : 1,
        "2023" : 2,
        "2022" : 3,
        "2021" : 4,
        "2020" : 5
    }
campuses = {
    "G" : "goa",
    "H" : "hyderabad",
    "P" : "pilani"
}
branches = {
    "A1" : "chemical",
    "A2" : "civil",
    "A3" : "eee",
    "A4" : "mech",
    "A5" : "pharma",
    "A7" : "cs",
    "A8" : "eni",
    "AA" : "ece",
    "AB" : "manu",
    "B1" : "bio",
    "B2" : "chem",
    "B3" : "eco",
    "B4" : "math",
    "B5" : "phy",
    "D2" : "genstudies"
}
@app.route("/", methods = ["GET", "POST"])
def index():
    myDict["ids"].clear()
    with open(file, 'r') as rf:
        for i in rf.readlines():
            myDict['ids'].append(i.rstrip('\n'))
    format, branch, year = '', '', ''
    format = request.args.get("format")
    branch = request.args.get("branch")
    year = request.args.get("year")
    if format == 'text':
        return '<br>'.join(myDict['ids'])
    if branch:
        try:
            li = [i for i in myDict['ids'] if i[4:6] == list(branches.keys())[list(branches.values()).index(branch.lower())]]
            return jsonify({'ids' : li})
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "error" : "Invalid branch",
                    "code" : 404
                }
            )
    if year:
        try:
            li = [i for i in myDict['ids'] if i[:4] == list(years.keys())[list(years.values()).index(int(year))]]
            return jsonify({'ids' : li})
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "error" : "Invalid year",
                    "code" : 404
                }
            )
    return jsonify(myDict)
@app.route("/<id>")
def path(id):
    assert id == request.view_args['id']
    obj = ''
    for i in myDict['ids']:
        if i[8:12] == id:
            obj = i
            break
    try:
        objDict = {
            "year" : years[obj[:4]],
            "branch" : branches[obj[4:6]],
            "campus" : campuses[obj[-1]],
            "email" : f"f{obj[:4]}{id}@{campuses[obj[-1]]}.bits-pilani.ac.in",
            "id" : obj,
            "uid" : id
        }
        return jsonify(objDict)
    except Exception as e:
        print(e)
        return jsonify(
            {
                "error" : "Invalid ID",
                "code" : 404
            }
        )

if __name__ == "__main__":
    app.run()