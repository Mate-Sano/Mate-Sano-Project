from flask import Flask, request

app = Flask(__name__)

campus=""
Last_Name=""
Name=""
Middle_Initial=""
days=""
mins=""
classes=""
Inclusive_Dates=""
Year_Section=""

@app.route("/", methods=["GET","POST"])
def admission_slip():

    global campus, Last_Name, Name, Middle_Initial, days, mins, classes, Inclusive_Dates, Year_Section

    if request.method == "POST":
        campus = request.form.get("campus","")
        Last_Name = request.form.get("lastname","")
        Name = request.form.get("name","")
        Middle_Initial = request.form.get("mi","")
        Year_Section = request.form.get("section","")
        days = request.form.get("days","")
        mins = request.form.get("mins","")
        classes = request.form.get("classes","")
        Inclusive_Dates = request.form.get("dates","")

    return f"""
    <h2>PHILIPPINE SCIENCE HIGH SCHOOL SYSTEM</h2>
    <h3>Class Admission Slip</h3>

    <form method="POST">

    Campus: <input name="campus"><br><br>

    Last Name: <input name="lastname"><br>
    Given Name: <input name="name"><br>
    Middle Initial: <input name="mi"><br><br>

    Year & Section: <input name="section"><br><br>

    Absent Days: <input name="days"><br>
    Tardy Minutes: <input name="mins"><br>
    Cutting Classes: <input name="classes"><br><br>

    Inclusive Dates: <input name="dates"><br><br>

    <input type="submit" value="Generate Admission Slip">

    </form>

    <hr>

    <h3>Generated Admission Slip</h3>

    Campus: {campus}<br><br>

    Please admit {Last_Name} {Name} {Middle_Initial}<br>
    Year & Section: {Year_Section}<br><br>

    Absent: {days} days<br>
    Tardy: {mins} mins<br>
    Cutting: {classes} classes<br><br>

    Inclusive Dates: {Inclusive_Dates}

    """

if __name__ == "__main__":
    app.run(debug=True)