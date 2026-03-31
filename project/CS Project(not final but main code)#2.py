def get_role_from_email(email):
    if email.endswith("@student.pshs.edu.ph"):
        return "student"
    elif email.endswith("@pshs.edu.ph"):
        return "teacher"
    else:
        return None


def admission_slip(slip, role, current_email):

    def show_slip(slip):
        print("\n                             PHILIPPINE SCIENCE HIGH SCHOOL SYSTEM")
        print(f"                                    Campus: {slip['campus']}")
        print("                                         CLASS ADMISSION SLIP")

        print("\nTo all teachers concerned:")
        print(f"Please admit {slip['Last_Name']:<15}{slip['Name']:<15}{slip['Middle_Initial']:<5}Year & Section: {slip['Year_Section']}")
        print("             Last Name     Given Name     M.I")

        print("\n                                 Subject")
        print(f"[] Absent    - {slip['days']} days         ____")
        print(f"[] Tardy     - {slip['mins']} mins        ____")
        print(f"[] Cutting   - {slip['classes']} classes    ____")
        print("                                     ____")

        print(f"\nInclusive Date/s: {slip['Inclusive_Dates']}")

        print("\nFOR REGISTRAR'S USE ONLY:")
        print("Excused      Unexcused")
        print("[ ]              [ ]")

        print("____________________                 Registrar")

        print("\nDate issued: ____________ Time issued: ____________")
        print("Attachments:   [ ] Medical Certificate        [ ] Letter from parent/guardian")
        print("Reason: ______________________________________________________")

        print("\nCertified by: Health Services Unit - __________________ Guidance Unit - ________________________")
        print("Noted by: Homeroom Adviser - _____________________")

        print("\nNote: This admission slip is valid only if signed by the registrar.")
        print("PSHS-00-F-REG-22-Ver02-Rev0-12/05/20")

    while True:
        print("\n1. Show admission slip")

        if role == "student":
            print("2. Edit admission slip")
            print("3. Send admission slip")
            print("4. Logout")
        else:
            print("2. Show received slips")
            print("3. Logout")

        choice = input("Input choice: ")

        # ---------------- SHOW SLIP ----------------
        if choice == "1":
            if role == "student":
                if slip:
                    show_slip(slip)
                else:
                    print("No slip available.")
            else:
                print("Use option 2 to view received slips.")

        # ---------------- EDIT (STUDENT) ----------------
        elif choice == "2" and role == "student":
            while True:
                print("\nEDIT MENU")
                print("1. Edit campus")
                print("2. Edit name")
                print("3. Edit section")
                print("4. Edit absence days")
                print("5. Edit tardy minutes")
                print("6. Edit cutting classes")
                print("7. Edit inclusive dates")
                print("8. Back")

                choice2 = input("Input choice: ")

                if choice2 == "1":
                    slip["campus"] = input("Input campus: ")

                elif choice2 == "2":
                    slip["Last_Name"] = input("Input Last name: ")
                    slip["Name"] = input("Input Given name: ")
                    slip["Middle_Initial"] = input("Input Middle Initial: ")

                elif choice2 == "3":
                    slip["Year_Section"] = input("Input Year & Section: ")

                elif choice2 == "4":
                    slip["days"] = input("Input number of absent days: ")

                elif choice2 == "5":
                    slip["mins"] = input("Input tardy minutes: ")

                elif choice2 == "6":
                    slip["classes"] = input("Input cutting classes: ")

                elif choice2 == "7":
                    slip["Inclusive_Dates"] = input("Input inclusive dates: ")

                elif choice2 == "8":
                    break

                else:
                    print("Invalid input!")

        # ---------------- SEND SLIP (STUDENT) ----------------
        elif choice == "3" and role == "student":
            teachers = [acc for acc in accounts if accounts[acc]["role"] == "teacher"]

            if not teachers:
                print("No teachers available.")
                continue

            print("\nAvailable teachers:")
            for i, t in enumerate(teachers):
                print(f"{i+1}. {t}")

            try:
                pick = int(input("Choose teacher: ")) - 1
                selected_teacher = teachers[pick]

                # send a copy
                accounts[selected_teacher]["inbox"].append(slip.copy())

                print("Admission slip sent!")

            except:
                print("Invalid selection.")

        # ---------------- TEACHER VIEW INBOX ----------------
        elif choice == "2" and role == "teacher":
            inbox = accounts[current_email]["inbox"]

            if not inbox:
                print("No received slips.")
            else:
                for i, s in enumerate(inbox):
                    print(f"\n--- Slip #{i+1} ---")
                    show_slip(s)

        # ---------------- LOGOUT ----------------
        elif (choice == "4" and role == "student") or (choice == "3" and role == "teacher"):
            print("Logged out.")
            break

        else:
            print("Invalid choice!")


# ---------------- ACCOUNTS ----------------
accounts = {
    "dachel@pshs.edu.ph": {
        "password": "1234",
        "role": "teacher",
        "slip": None,
        "inbox": []
    }
}


# ---------------- MAIN MENU ----------------
while True:
    print("\n1. Make new account")
    print("2. Login")
    print("3. Exit")

    option = input("Choose: ")

    # ---------------- SIGNUP ----------------
    if option == "1":

        while True:
            email = input("Input email: ")
            role = get_role_from_email(email)

            if role is None:
                print("Invalid email domain! Try again.")
            else:
                break

        if email in accounts:
            print("Email already exists!")
            continue

        password = input("Input password: ")

        if role == "student":
            slip = {
                "campus": "",
                "Last_Name": "",
                "Name": "",
                "Middle_Initial": "",
                "days": "",
                "mins": "",
                "classes": "",
                "Inclusive_Dates": "",
                "Year_Section": ""
            }
            inbox = None
        else:
            slip = None
            inbox = []

        accounts[email] = {
            "password": password,
            "role": role,
            "slip": slip,
            "inbox": inbox
        }

        print("Account created successfully!")

    # ---------------- LOGIN ----------------
    elif option == "2":

        while True:
            email = input("Email: ")
            role = get_role_from_email(email)

            if role is None:
                print("Invalid email domain! Try again.")
            else:
                break

        password = input("Password: ")

        if email in accounts and accounts[email]["password"] == password:
            print("Login successful!")

            role = accounts[email]["role"]
            slip = accounts[email]["slip"]

            admission_slip(slip, role, email)

        else:
            print("Invalid email or password!")

    elif option == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")