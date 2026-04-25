import os

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".doc", ".docx"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.secret_key = "excusetrack-secret-key"

# ---------------- TEMP DATABASE ----------------
TEACHER_ACCOUNTS = {
    "Ma'am Joh": "joh@pshs.edu.ph",
    "Ma'am Anne": "anne@pshs.edu.ph",
    "Ma'am Vesh": "vesh@pshs.edu.ph",
    "Sir Asis": "asis@pshs.edu.ph",
    "Sir Den": "den@pshs.edu.ph",
    "Sir Ruel": "ruel@pshs.edu.ph",
    "Ma'am Bing": "bing@pshs.edu.ph",
    "Sir Rolex": "rolex@pshs.edu.ph",
    "Sir X": "x@pshs.edu.ph",
    "Ma'am Nida": "nida@pshs.edu.ph",
    "Ma'am Gaye": "gaye@pshs.edu.ph",
    "Ma'am Jen": "jen@pshs.edu.ph",
    "Sir Renzo": "renzo@pshs.edu.ph",
    "Sir Joshua": "joshua@pshs.edu.ph",
    "Sir Dennis": "dennis@pshs.edu.ph",
    "Ma'am Ali": "ali@pshs.edu.ph",
    "Sir Vinci": "vinci@pshs.edu.ph",
    "Sir Ely": "ely@pshs.edu.ph",
    "Ma'am Cindy": "cindy@pshs.edu.ph",
    "Ma'am Caam": "caam@pshs.edu.ph",
    "Ma'am Brenda": "brenda@pshs.edu.ph",
    "Sir Niche": "niche@pshs.edu.ph",
    "Ma'am Datch": "datch@pshs.edu.ph"
}

accounts = {
    "nurse@nurse.pshs.edu.ph": {"password": "1234", "role": "nurse", "inbox": [], "display_name": "School Nurse"}
}

for teacher_name, teacher_email in TEACHER_ACCOUNTS.items():
    accounts[teacher_email] = {
        "password": "1234",
        "role": "teacher",
        "inbox": [],
        "display_name": teacher_name
    }

admission_slips = []

TEACHER_DIRECTORY = {
    "grade 7": [
        {"aliases": ["pehm1", "pehm"], "teacher": "Ma'am Joh"},
        {"aliases": ["valed2", "valed"], "teacher": "Ma'am Anne"},
        {"aliases": ["filipino1", "filipino"], "teacher": "Ma'am Vesh"},
        {"aliases": ["math1", "math"], "teacher": "Sir Asis"},
        {"aliases": ["eng1", "english1", "english"], "teacher": "Sir Den"},
        {"aliases": ["is"], "teacher": "Sir Ruel"},
        {"aliases": ["socsci1", "socsci"], "teacher": "Ma'am Bing"},
        {"aliases": ["cs1", "cs"], "teacher": "Sir Rolex"},
        {"aliases": ["adtech1", "adtech"], "teacher": "Sir X"}
    ],
    "grade 8 camia": [
        {"aliases": ["bio", "biology"], "teacher": "Ma'am Nida"},
        {"aliases": ["chem", "chemistry"], "teacher": "Ma'am Gaye"},
        {"aliases": ["cs2", "cs"], "teacher": "Ma'am Datch"},
        {"aliases": ["math2"], "teacher": "Ma'am Jen"},
        {"aliases": ["math3"], "teacher": "Sir Renzo"},
        {"aliases": ["physics"], "teacher": "Sir Joshua"},
        {"aliases": ["es"], "teacher": "Sir Dennis"},
        {"aliases": ["socsci2", "socsci"], "teacher": "Ma'am Ali"},
        {"aliases": ["valed"], "teacher": "Ma'am Ali"},
        {"aliases": ["adtech"], "teacher": "Sir Vinci"},
        {"aliases": ["filipino"], "teacher": "Sir Ely"},
        {"aliases": ["pehm"], "teacher": "Ma'am Cindy"},
        {"aliases": ["english"], "teacher": "Ma'am Caam"}
    ],
    "grade 8 sampa": [
        {"aliases": ["bio", "biology"], "teacher": "Ma'am Nida"},
        {"aliases": ["chem", "chemistry"], "teacher": "Ma'am Gaye"},
        {"aliases": ["cs2", "cs"], "teacher": "Ma'am Datch"},
        {"aliases": ["math2"], "teacher": "Sir Asis"},
        {"aliases": ["math3"], "teacher": "Sir Renzo"},
        {"aliases": ["physics"], "teacher": "Sir Joshua"},
        {"aliases": ["es"], "teacher": "Ma'am Brenda"},
        {"aliases": ["socsci2", "socsci"], "teacher": "Ma'am Ali"},
        {"aliases": ["valed"], "teacher": "Ma'am Ali"},
        {"aliases": ["adtech"], "teacher": "Sir Vinci"},
        {"aliases": ["filipino"], "teacher": "Sir Ely"},
        {"aliases": ["pehm"], "teacher": "Ma'am Cindy"},
        {"aliases": ["english"], "teacher": "Ma'am Caam"}
    ],
    "grade 8 jasmine": [
        {"aliases": ["bio", "biology"], "teacher": "Sir Niche"},
        {"aliases": ["chem", "chemistry"], "teacher": "Ma'am Gaye"},
        {"aliases": ["physics","p6"], "teacher": "Sir Joshua"},
        {"aliases": ["cs2", "cs"], "teacher": "Ma'am Datch"},
        {"aliases": ["math2"], "teacher": "Ma'am Jen"},
        {"aliases": ["math3"], "teacher": "Sir Renzo"},
        {"aliases": ["es"], "teacher": "Ma'am Brenda"},
        {"aliases": ["socsci2", "socsci"], "teacher": "Ma'am Ali"},
        {"aliases": ["valed"], "teacher": "Ma'am Anne"},
        {"aliases": ["filipino"], "teacher": "Sir Ely"},
        {"aliases": ["pehm"], "teacher": "Ma'am Cindy"},
        {"aliases": ["english"], "teacher": "Ma'am Caam"}
    ]
}

HOMEROOM_ADVISERS = {
    "grade 7 ruby": {"name": "Ma'am Joh", "email": TEACHER_ACCOUNTS["Ma'am Joh"]},
    "grade 7 diamond": {"name": "Sir Ruel", "email": TEACHER_ACCOUNTS["Sir Ruel"]},
    "grade 7 emerald": {"name": "Ma'am Bing", "email": TEACHER_ACCOUNTS["Ma'am Bing"]},
    "grade 8 camia": {"name": "Sir Den", "email": TEACHER_ACCOUNTS["Sir Den"]},
    "grade 8 sampa": {"name": "Ma'am Cindy", "email": TEACHER_ACCOUNTS["Ma'am Cindy"]},
    "grade 8 jasmine": {"name": "Ma'am Datch", "email": TEACHER_ACCOUNTS["Ma'am Datch"]}
}

# ---------------- ROLE DETECTION ----------------
def get_role_from_email(email):
    if email.endswith("@student.pshs.edu.ph"):
        return "student"
    elif email.endswith("@pshs.edu.ph"):
        return "teacher"
    elif email.endswith("@nurse.pshs.edu.ph"):
        return "nurse"
    elif email.endswith("@homeroom.pshs.edu.ph"):
        return "homeroom"
    return None


def normalize_text(value):
    return " ".join(value.lower().replace("-", " ").split())


def get_subject_variants(subject):
    normalized = normalize_text(subject)
    variants = {normalized}

    compact = normalized.replace(" ", "")
    if compact:
        variants.add(compact)

    return variants


def get_grade_section_key(grade_section):
    normalized = normalize_text(grade_section)

    if normalized.startswith("grade 7"):
        for section in ["ruby", "diamond", "emerald"]:
            if section in normalized:
                return f"grade 7 {section}"
        return "grade 7"

    if normalized.startswith("grade 8"):
        for section in ["camia", "sampa", "jasmine"]:
            if section in normalized:
                return f"grade 8 {section}"

    return None


def get_teacher_targets(grade_section, subjects):
    section_key = get_grade_section_key(grade_section)
    subject_map = TEACHER_DIRECTORY.get(section_key, [])
    if not subject_map and section_key and section_key.startswith("grade 7 "):
        subject_map = TEACHER_DIRECTORY.get("grade 7", [])
    teacher_targets = {}

    for subject in subjects:
        subject_variants = get_subject_variants(subject)
        for entry in subject_map:
            alias_variants = {normalize_text(alias).replace(" ", "") for alias in entry["aliases"]}
            if subject_variants & alias_variants:
                teacher_name = entry["teacher"]
                teacher_email = TEACHER_ACCOUNTS.get(teacher_name, "")
                if teacher_email:
                    teacher_targets.setdefault(
                        teacher_email,
                        {"name": teacher_name, "email": teacher_email, "subjects": []}
                    )
                    if subject not in teacher_targets[teacher_email]["subjects"]:
                        teacher_targets[teacher_email]["subjects"].append(subject)
                break

    return list(teacher_targets.values())


def get_homeroom_adviser(grade_section):
    section_key = get_grade_section_key(grade_section)
    return HOMEROOM_ADVISERS.get(section_key)


def is_allowed_upload(filename):
    _, extension = os.path.splitext(filename.lower())
    return extension in ALLOWED_UPLOAD_EXTENSIONS


def validate_submission_payload(form, files):
    student_name = form.get("student_name", "").strip()
    student_email = form.get("student_email", "").strip()
    grade_section = form.get("grade_section", "").strip()
    date_of_absence = form.get("date_of_absence", "").strip()

    if not student_name:
        return "Student name is required."

    if get_role_from_email(student_email) != "student":
        return "Please use a valid student email."

    if not grade_section:
        return "Grade and section are required."

    if not date_of_absence:
        return "Please choose a date of absence."

    offenses = [
        "offense_absent" in form,
        "offense_tardy" in form,
        "offense_cutting" in form
    ]
    if not any(offenses):
        return "Please select at least one offense: absent, tardy, or cutting."

    if "offense_absent" in form:
        absent_days = form.get("absent_days", "").strip()
        if not absent_days:
            return "Please enter the number of days absent."
        try:
            absent_day_count = int(absent_days)
        except ValueError:
            return "Days absent must be a valid number."
        if absent_day_count < 1:
            return "Days absent must be at least 1."

        absent_dates = [value.strip() for value in form.getlist("absent_dates[]") if value.strip()]
        if len(absent_dates) != absent_day_count:
            return "Please enter absent dates that match the number of days absent."

    if "offense_tardy" in form:
        tardy_minutes = form.get("tardy_minutes", "").strip()
        if not tardy_minutes:
            return "Please enter the tardy minutes."
        try:
            if int(tardy_minutes) < 1:
                return "Tardy minutes must be at least 1."
        except ValueError:
            return "Tardy minutes must be a valid number."

    if "offense_cutting" in form:
        cutting_classes = form.get("cutting_classes", "").strip()
        if not cutting_classes:
            return "Please enter the number of classes cut."
        try:
            if int(cutting_classes) < 1:
                return "Classes cut must be at least 1."
        except ValueError:
            return "Classes cut must be a valid number."

    subjects = [subject.strip() for subject in form.getlist("subjects[]") if subject.strip()]
    if not subjects:
        return "Please enter at least one affected subject."

    attachment = files.get("attachment")
    if attachment is None or not attachment.filename:
        return "Please upload your excuse letter or medical certificate."

    if not is_allowed_upload(attachment.filename):
        return "Please upload a PDF, image, or Word document for the attachment."

    return None


def validate_slip_action(slip, role, email, action):
    if action not in {"approve", "reject"}:
        return "Invalid action."

    if slip is None:
        return "Unable to update that slip."

    if slip["current_inbox"] in {"completed", "rejected", "pending_homeroom"}:
        return "This slip can no longer be updated."

    if role == "teacher" and slip["current_inbox"] == "teacher":
        approval = slip["teacher_approvals"].get(email)
        if approval is None:
            return "This slip is not assigned to your teacher account."
        if approval["status"] != "pending":
            return "You have already acted on this slip."

    return None


def get_account_by_role(role):
    for email, account in accounts.items():
        if account["role"] == role:
            return email, account
    return None, None


def get_slip_by_id(slip_id):
    for slip in admission_slips:
        if slip["id"] == slip_id:
            return slip
    return None


def remove_from_all_inboxes(slip):
    for account in accounts.values():
        if slip in account["inbox"]:
            account["inbox"].remove(slip)


def send_to_role_inbox(role, slip):
    remove_from_all_inboxes(slip)
    inbox_email, inbox_account = get_account_by_role(role)
    if inbox_account is not None:
        inbox_account["inbox"].append(slip)
        slip["current_inbox"] = role
        slip["assigned_email"] = inbox_email


def send_to_teacher_inboxes(slip):
    remove_from_all_inboxes(slip)

    for teacher in slip["teacher_targets"]:
        teacher_account = accounts.get(teacher["email"])
        if teacher_account is not None:
            teacher_account["inbox"].append(slip)

    slip["current_inbox"] = "teacher"
    slip["assigned_email"] = ""


def send_to_homeroom_inbox(slip):
    remove_from_all_inboxes(slip)
    adviser = slip.get("homeroom_adviser")
    if adviser:
        homeroom_account = accounts.get(adviser["email"])
        if homeroom_account is not None:
            homeroom_account["inbox"].append(slip)
            slip["current_inbox"] = "homeroom"
            slip["assigned_email"] = adviser["email"]
            return

    slip["current_inbox"] = "pending_homeroom"
    slip["assigned_email"] = ""


def approve_slip(slip, approver_email):
    if slip["current_inbox"] == "nurse":
        if slip["teacher_targets"]:
            send_to_teacher_inboxes(slip)
            slip["status"] = "Approved by Nurse - Sent to Subject Teacher Inboxes"
        else:
            send_to_homeroom_inbox(slip)
            if slip.get("homeroom_adviser"):
                slip["status"] = "Approved by Nurse - No Subject Teacher Match, Sent to Homeroom Adviser"
            else:
                slip["status"] = "Approved by Nurse - Waiting for Homeroom Adviser Mapping"
    elif slip["current_inbox"] == "teacher":
        approval = slip["teacher_approvals"].get(approver_email)
        if approval is not None:
            approval["status"] = "approved"
            teacher_account = accounts.get(approver_email)
            if teacher_account is not None and slip in teacher_account["inbox"]:
                teacher_account["inbox"].remove(slip)

            pending_count = sum(
                1 for teacher in slip["teacher_approvals"].values() if teacher["status"] == "pending"
            )

            if pending_count == 0:
                send_to_homeroom_inbox(slip)
                if slip.get("homeroom_adviser"):
                    slip["status"] = "All Subject Teachers Approved - Sent to Homeroom Adviser"
                else:
                    slip["status"] = "All Subject Teachers Approved - Waiting for Homeroom Adviser Mapping"
            else:
                slip["status"] = (
                    f"Approved by {approval['name']} - Waiting for {pending_count} more subject teacher(s)"
                )
    elif slip["current_inbox"] == "homeroom":
        remove_from_all_inboxes(slip)
        slip["current_inbox"] = "completed"
        slip["assigned_email"] = ""
        slip["status"] = "Fully Approved by Homeroom"


def reject_slip(slip, role, approver_email):
    remove_from_all_inboxes(slip)
    slip["current_inbox"] = "rejected"
    slip["assigned_email"] = ""
    if role == "teacher" and approver_email in slip["teacher_approvals"]:
        slip["teacher_approvals"][approver_email]["status"] = "rejected"
        slip["status"] = f"Rejected by {slip['teacher_approvals'][approver_email]['name']}"
    else:
        slip["status"] = f"Rejected by {role.title()}"

# ---------------- HOME (LOGIN PAGE) ----------------
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    if email in accounts and accounts[email]["password"] == password:
        role = accounts[email]["role"]
        return redirect(url_for("dashboard", role=role, email=email))

    flash("Invalid email or password!")
    return redirect(url_for("home"))

# ---------------- SIGNUP PAGE ----------------
@app.route("/signup")
def signup_page():
    return render_template("signup.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    password = request.form["password"]

    role = get_role_from_email(email)

    if role is None:
        flash("Invalid school email!")
        return redirect(url_for("signup_page"))

    if email in accounts:
        flash("Account already exists!")
        return redirect(url_for("signup_page"))

    # Create account
    accounts[email] = {
        "password": password,
        "role": role,
        "inbox": []
    }

    role = accounts[email]["role"]

    flash("Account created successfully!")
    return redirect(url_for("dashboard", role=role, email=email))


# ---------------- ADMISSION SLIP ----------------
@app.route("/submit-slip", methods=["POST"])
def submit_slip():
    student_email = request.form["student_email"].strip()
    role = get_role_from_email(student_email)

    if role != "student":
        flash("Only student accounts can submit an admission slip.")
        return redirect(url_for("dashboard", role="student", email=student_email))

    validation_error = validate_submission_payload(request.form, request.files)
    if validation_error:
        flash(validation_error)
        return redirect(url_for("dashboard", role="student", email=student_email))

    offense_absent = "offense_absent" in request.form
    offense_tardy = "offense_tardy" in request.form
    offense_cutting = "offense_cutting" in request.form

    absent_days = request.form["absent_days"].strip() if offense_absent else ""
    tardy_minutes = request.form["tardy_minutes"].strip() if offense_tardy else ""
    cutting_classes = request.form["cutting_classes"].strip() if offense_cutting else ""

    subjects = request.form.getlist("subjects[]")
    subjects = [subject.strip() for subject in subjects if subject.strip()]

    absent_dates = []
    if offense_absent:
        absent_dates = request.form.getlist("absent_dates[]")
        absent_dates = [date_value.strip() for date_value in absent_dates if date_value.strip()]

    grade_section = request.form["grade_section"].strip()
    teacher_targets = get_teacher_targets(grade_section, subjects)
    homeroom_adviser = get_homeroom_adviser(grade_section)
    attachment = request.files.get("attachment")

    safe_filename = secure_filename(attachment.filename)
    stored_filename = f"{len(admission_slips) + 1}_{safe_filename}"
    attachment.save(os.path.join(UPLOAD_FOLDER, stored_filename))

    teacher_approvals = {
        teacher["email"]: {
            "name": teacher["name"],
            "subjects": teacher["subjects"],
            "status": "pending"
        }
        for teacher in teacher_targets
    }

    slip = {
        "id": len(admission_slips) + 1,
        "student_name": request.form["student_name"].strip(),
        "student_email": student_email,
        "grade_section": grade_section,
        "date_of_absence": request.form["date_of_absence"],
        "offense_absent": offense_absent,
        "absent_days": absent_days,
        "absent_dates": absent_dates,
        "offense_tardy": offense_tardy,
        "tardy_minutes": tardy_minutes,
        "offense_cutting": offense_cutting,
        "cutting_classes": cutting_classes,
        "subjects": subjects,
        "teacher_targets": teacher_targets,
        "teacher_approvals": teacher_approvals,
        "homeroom_adviser": homeroom_adviser,
        "attachment_name": safe_filename,
        "attachment_file": stored_filename,
        "status": "Sent to Nurse Inbox",
        "current_inbox": "",
        "assigned_email": "",
        "hidden_from_student": False
    }

    admission_slips.append(slip)
    send_to_role_inbox("nurse", slip)
    flash("Admission slip submitted and sent to the nurse inbox.")
    return redirect(url_for("dashboard", role="student", email=student_email))


@app.route("/update-slip/<int:slip_id>", methods=["POST"])
def update_slip(slip_id):
    role = request.form["role"]
    email = request.form["email"]
    action = request.form["action"]

    slip = get_slip_by_id(slip_id)
    account = accounts.get(email)

    if slip is None or account is None or account["role"] != role:
        flash("Unable to update that slip.")
        return redirect(url_for("dashboard", role=role, email=email))

    is_homeroom_adviser = (
        slip.get("homeroom_adviser") is not None and
        slip["homeroom_adviser"]["email"] == email
    )

    if slip["current_inbox"] == "homeroom":
        if not is_homeroom_adviser:
            flash("This slip is not assigned to your homeroom adviser account.")
            return redirect(url_for("dashboard", role=role, email=email))
    elif slip["current_inbox"] != role:
        flash("This slip is no longer assigned to your inbox.")
        return redirect(url_for("dashboard", role=role, email=email))

    if role == "teacher" and slip["current_inbox"] == "teacher" and email not in slip["teacher_approvals"]:
        flash("This slip is not assigned to your teacher account.")
        return redirect(url_for("dashboard", role=role, email=email))

    validation_error = validate_slip_action(slip, role, email, action)
    if validation_error:
        flash(validation_error)
        return redirect(url_for("dashboard", role=role, email=email))

    if action == "approve":
        approve_slip(slip, email)
        flash("Slip approved and forwarded successfully.")
    elif action == "reject":
        reject_slip(slip, role, email)
        flash("Slip rejected successfully.")

    return redirect(url_for("dashboard", role=role, email=email))


@app.route("/hide-slip/<int:slip_id>", methods=["POST"])
def hide_slip(slip_id):
    email = request.form["email"]
    slip = get_slip_by_id(slip_id)

    if slip is None or slip["student_email"] != email:
        flash("Unable to hide that slip.")
        return redirect(url_for("dashboard", role="student", email=email))

    if slip["status"] == "Sent to Nurse Inbox":
        flash("You can only remove a slip after it has been accepted or rejected by staff.")
        return redirect(url_for("dashboard", role="student", email=email))

    slip["hidden_from_student"] = True
    flash("Slip removed from your submitted list.")
    return redirect(url_for("dashboard", role="student", email=email))

# ---------------- DASHBOARD ----------------
@app.route("/dashboard/<role>")
def dashboard(role):
    email = request.args.get("email", "")
    account = accounts.get(email)
    display_name = account["display_name"] if account and "display_name" in account else email

    if role == "student" and email:
        visible_slips = [
            slip for slip in admission_slips
            if slip["student_email"] == email and not slip.get("hidden_from_student", False)
        ]
        inbox_items = []
    else:
        visible_slips = []
        inbox_items = account["inbox"] if account else []

    return render_template(
        "dashboard.html",
        role=role,
        email=email,
        display_name=display_name,
        slips=visible_slips,
        inbox_items=inbox_items
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
