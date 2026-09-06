import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import sys
import os
import csv
from datetime import datetime


# ==================================================
# PATHS
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ATTENDANCE_FILE = os.path.join(
    BASE_DIR, "attendance.csv"
)

DATASET_PATH = os.path.join(
    BASE_DIR, "dataset"
)


# ==================================================
# LOGIN DETAILS
# ==================================================

USERNAME = "admin"
PASSWORD = "admin123"


# ==================================================
# MAIN WINDOW
# ==================================================

root = tk.Tk()

root.title("Face Recognition Attendance System")
root.geometry("700x650")
root.resizable(False, False)

root.configure(bg="#EAF2FF")


# ==================================================
# CLEAR WINDOW
# ==================================================

def clear_window():

    for widget in root.winfo_children():
        widget.destroy()


# ==================================================
# ATTENDANCE STATISTICS
# ==================================================

def get_stats():

    total_students = 0

    if os.path.exists(DATASET_PATH):

        for folder in os.listdir(DATASET_PATH):

            folder_path = os.path.join(
                DATASET_PATH,
                folder
            )

            if os.path.isdir(folder_path):
                total_students += 1

    present_students = set()

    today = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(ATTENDANCE_FILE):

        with open(
            ATTENDANCE_FILE,
            "r",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if (
                    row.get("Date") == today
                    and row.get("Status") == "Present"
                ):

                    present_students.add(
                        row.get("Roll No")
                    )

    present = len(present_students)

    absent = max(
        total_students - present,
        0
    )

    return total_students, present, absent


# ==================================================
# UPDATE DASHBOARD
# ==================================================

def update_dashboard():

    total, present, absent = get_stats()

    total_label.config(text=str(total))

    present_label.config(text=str(present))

    absent_label.config(text=str(absent))


# ==================================================
# REGISTER STUDENT
# ==================================================

def register_student():

    window = tk.Toplevel(root)

    window.title("Register Student")
    window.geometry("430x380")
    window.resizable(False, False)

    window.configure(bg="#F5F8FF")

    tk.Label(
        window,
        text="📚 Register New Student",
        font=("Arial", 20, "bold"),
        bg="#F5F8FF",
        fg="#3157D5"
    ).pack(pady=25)

    tk.Label(
        window,
        text="👤 Student Name",
        font=("Arial", 11, "bold"),
        bg="#F5F8FF"
    ).pack()

    name_entry = tk.Entry(
        window,
        width=35,
        font=("Arial", 12)
    )

    name_entry.pack(
        pady=8,
        ipady=5
    )

    tk.Label(
        window,
        text="🎓 Roll Number",
        font=("Arial", 11, "bold"),
        bg="#F5F8FF"
    ).pack()

    roll_entry = tk.Entry(
        window,
        width=35,
        font=("Arial", 12)
    )

    roll_entry.pack(
        pady=8,
        ipady=5
    )


    def start_registration():

        name = name_entry.get().strip()

        roll_no = roll_entry.get().strip()

        if name == "" or roll_no == "":

            messagebox.showwarning(
                "Missing Details",
                "Please enter Name and Roll Number.",
                parent=window
            )

            return

        window.destroy()

        messagebox.showinfo(
            "Camera",
            "Camera will open now.\n\n"
            "Look at the camera until 20 images are captured."
        )

        try:

            subprocess.run(
                [
                    sys.executable,
                    os.path.join(
                        BASE_DIR,
                        "register.py"
                    )
                ],
                input=f"{name}\n{roll_no}\n",
                text=True,
                cwd=BASE_DIR
            )

            update_dashboard()

            messagebox.showinfo(
                "Success",
                "Student registration completed!"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


    tk.Button(
        window,
        text="📷 Start Registration",
        command=start_registration,
        width=24,
        height=2,
        font=("Arial", 11, "bold"),
        bg="#3157D5",
        fg="white",
        bd=0
    ).pack(pady=30)


# ==================================================
# START ATTENDANCE
# ==================================================

def start_attendance():

    messagebox.showinfo(
        "Attendance",
        "Camera will open now.\n\n"
        "Face the camera for recognition.\n"
        "Press Q to stop."
    )

    try:

        subprocess.Popen(
            [
                sys.executable,
                os.path.join(
                    BASE_DIR,
                    "recognize.py"
                )
            ],
            cwd=BASE_DIR
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ==================================================
# VIEW REPORT
# ==================================================

def view_report():

    try:

        result = subprocess.run(
            [
                sys.executable,
                os.path.join(
                    BASE_DIR,
                    "report.py"
                )
            ],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )

        report_window = tk.Toplevel(root)

        report_window.title(
            "Attendance Report"
        )

        report_window.geometry(
            "750x550"
        )

        tk.Label(
            report_window,
            text="📊 Attendance Report",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        text_area = scrolledtext.ScrolledText(
            report_window,
            width=85,
            height=27,
            font=("Courier New", 10)
        )

        text_area.pack(
            padx=15,
            pady=10,
            fill="both",
            expand=True
        )

        text_area.insert(
            tk.END,
            result.stdout
        )

        text_area.config(
            state="disabled"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ==================================================
# DASHBOARD
# ==================================================

def show_dashboard():

    clear_window()

    root.title(
        "Face Recognition Attendance System"
    )

    root.geometry(
        "900x700"
    )

    root.configure(
        bg="#EAF2FF"
    )


    # ------------------------------------------------
    # HEADER
    # ------------------------------------------------

    header = tk.Frame(
        root,
        bg="#3157D5",
        height=150
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="📚 FACE RECOGNITION",
        font=("Arial", 28, "bold"),
        fg="white",
        bg="#3157D5"
    ).pack(
        pady=(25, 3)
    )

    tk.Label(
        header,
        text="ATTENDANCE MANAGEMENT SYSTEM",
        font=("Arial", 17, "bold"),
        fg="white",
        bg="#3157D5"
    ).pack()

    tk.Label(
        header,
        text="🎓 Smart Attendance • Better Tomorrow",
        font=("Arial", 11),
        fg="#E8EEFF",
        bg="#3157D5"
    ).pack(
        pady=8
    )


    # ------------------------------------------------
    # DATE
    # ------------------------------------------------

    tk.Label(
        root,
        text=datetime.now().strftime(
            "%d %B %Y"
        ),
        font=("Arial", 12, "bold"),
        bg="#EAF2FF",
        fg="#34415C"
    ).pack(
        pady=15
    )


    # ------------------------------------------------
    # STATISTICS
    # ------------------------------------------------

    stats_frame = tk.Frame(
        root,
        bg="#EAF2FF"
    )

    stats_frame.pack(
        pady=10
    )


    # TOTAL

    total_box = tk.Frame(
        stats_frame,
        width=230,
        height=130,
        bg="white",
        relief="solid",
        bd=1
    )

    total_box.grid(
        row=0,
        column=0,
        padx=12
    )

    total_box.pack_propagate(False)

    tk.Label(
        total_box,
        text="👨‍🎓 TOTAL STUDENTS",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#3157D5"
    ).pack(
        pady=18
    )

    global total_label

    total_label = tk.Label(
        total_box,
        text="0",
        font=("Arial", 30, "bold"),
        bg="white",
        fg="#3157D5"
    )

    total_label.pack()


    # PRESENT

    present_box = tk.Frame(
        stats_frame,
        width=230,
        height=130,
        bg="white",
        relief="solid",
        bd=1
    )

    present_box.grid(
        row=0,
        column=1,
        padx=12
    )

    present_box.pack_propagate(False)

    tk.Label(
        present_box,
        text="✅ PRESENT TODAY",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#238636"
    ).pack(
        pady=18
    )

    global present_label

    present_label = tk.Label(
        present_box,
        text="0",
        font=("Arial", 30, "bold"),
        bg="white",
        fg="#238636"
    )

    present_label.pack()


    # ABSENT

    absent_box = tk.Frame(
        stats_frame,
        width=230,
        height=130,
        bg="white",
        relief="solid",
        bd=1
    )

    absent_box.grid(
        row=0,
        column=2,
        padx=12
    )

    absent_box.pack_propagate(False)

    tk.Label(
        absent_box,
        text="❌ ABSENT TODAY",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#D73A49"
    ).pack(
        pady=18
    )

    global absent_label

    absent_label = tk.Label(
        absent_box,
        text="0",
        font=("Arial", 30, "bold"),
        bg="white",
        fg="#D73A49"
    )

    absent_label.pack()


    # ------------------------------------------------
    # BUTTONS
    # ------------------------------------------------

    button_frame = tk.Frame(
        root,
        bg="#EAF2FF"
    )

    button_frame.pack(
        pady=25
    )


    tk.Button(
        button_frame,
        text="👤 Register Student",
        command=register_student,
        width=27,
        height=2,
        font=("Arial", 12, "bold"),
        bg="#3157D5",
        fg="white",
        bd=0
    ).grid(
        row=0,
        column=0,
        padx=12,
        pady=8
    )


    tk.Button(
        button_frame,
        text="📷 Start Attendance",
        command=start_attendance,
        width=27,
        height=2,
        font=("Arial", 12, "bold"),
        bg="#238636",
        fg="white",
        bd=0
    ).grid(
        row=0,
        column=1,
        padx=12,
        pady=8
    )


    tk.Button(
        button_frame,
        text="📊 View Attendance Report",
        command=view_report,
        width=27,
        height=2,
        font=("Arial", 12, "bold"),
        bg="#7C3AED",
        fg="white",
        bd=0
    ).grid(
        row=1,
        column=0,
        padx=12,
        pady=8
    )


    tk.Button(
        button_frame,
        text="🔄 Refresh Dashboard",
        command=update_dashboard,
        width=27,
        height=2,
        font=("Arial", 12, "bold"),
        bg="#F59E0B",
        fg="white",
        bd=0
    ).grid(
        row=1,
        column=1,
        padx=12,
        pady=8
    )


    # ------------------------------------------------
    # LOGOUT
    # ------------------------------------------------

    tk.Button(
        root,
        text="🔐 Logout",
        command=show_login,
        width=20,
        height=2,
        font=("Arial", 11, "bold"),
        bg="#6B7280",
        fg="white",
        bd=0
    ).pack(
        pady=8
    )


    update_dashboard()


# ==================================================
# LOGIN PAGE
# ==================================================

def show_login():

    clear_window()

    root.title(
        "Login - Face Recognition Attendance System"
    )

    root.geometry(
        "700x650"
    )

    root.configure(
        bg="#EAF2FF"
    )


    # ------------------------------------------------
    # HEADER
    # ------------------------------------------------

    header = tk.Frame(
        root,
        bg="#3157D5",
        height=155
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="📚 FACE RECOGNITION",
        font=("Arial", 27, "bold"),
        fg="white",
        bg="#3157D5"
    ).pack(
        pady=(25, 3)
    )

    tk.Label(
        header,
        text="ATTENDANCE SYSTEM",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#3157D5"
    ).pack()

    tk.Label(
        header,
        text="🎓 Smart Attendance • Better Tomorrow",
        font=("Arial", 11),
        fg="#E8EEFF",
        bg="#3157D5"
    ).pack(
        pady=8
    )


    # ------------------------------------------------
    # LOGIN CARD
    # ------------------------------------------------

    card = tk.Frame(
        root,
        bg="white",
        relief="solid",
        bd=1
    )

    card.pack(
        padx=140,
        pady=30,
        fill="both",
        expand=True
    )


    tk.Label(
        card,
        text="🔐 Admin Login",
        font=("Arial", 21, "bold"),
        fg="#243B80",
        bg="white"
    ).pack(
        pady=(25, 5)
    )


    tk.Label(
        card,
        text="Login to manage student attendance",
        font=("Arial", 10),
        fg="#68738A",
        bg="white"
    ).pack(
        pady=(0, 20)
    )


    # ------------------------------------------------
    # USERNAME
    # ------------------------------------------------

    tk.Label(
        card,
        text="👤 Username",
        font=("Arial", 11, "bold"),
        fg="#34415C",
        bg="white"
    ).pack(
        anchor="w",
        padx=35
    )

    username_entry = tk.Entry(
        card,
        width=30,
        font=("Arial", 12),
        relief="solid",
        bd=1
    )

    username_entry.pack(
        padx=35,
        pady=(6, 15),
        ipady=7,
        fill="x"
    )


    # ------------------------------------------------
    # PASSWORD
    # ------------------------------------------------

    tk.Label(
        card,
        text="🔑 Password",
        font=("Arial", 11, "bold"),
        fg="#34415C",
        bg="white"
    ).pack(
        anchor="w",
        padx=35
    )

    password_entry = tk.Entry(
        card,
        width=30,
        show="●",
        font=("Arial", 12),
        relief="solid",
        bd=1
    )

    password_entry.pack(
        padx=35,
        pady=(6, 20),
        ipady=7,
        fill="x"
    )


    # ------------------------------------------------
    # LOGIN FUNCTION
    # ------------------------------------------------

    def login_user():

        username = username_entry.get().strip()

        password = password_entry.get().strip()

        if (
            username == USERNAME
            and password == PASSWORD
        ):

            show_dashboard()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password!"
            )


    # ------------------------------------------------
    # LOGIN BUTTON
    # ------------------------------------------------

    tk.Button(
        card,
        text="LOGIN  ➜",
        command=login_user,
        width=22,
        height=2,
        font=("Arial", 12, "bold"),
        bg="#3157D5",
        fg="white",
        activebackground="#243FA8",
        activeforeground="white",
        bd=0,
        cursor="hand2"
    ).pack(
        pady=5
    )


    # ------------------------------------------------
    # STUDY EMOJIS
    # ------------------------------------------------

    tk.Label(
        root,
        text="📖  ✏️  💻  🎓  📝",
        font=("Segoe UI Emoji", 20),
        bg="#EAF2FF"
    ).pack(
        pady=5
    )

    tk.Label(
        root,
        text="✨ Learn • Grow • Succeed ✨",
        font=("Arial", 10, "bold"),
        fg="#3157D5",
        bg="#EAF2FF"
    ).pack(
        pady=(0, 12)
    )


    # Enter key
    root.bind(
        "<Return>",
        lambda event: login_user()
    )

    username_entry.focus()


# ==================================================
# START APPLICATION
# ==================================================

show_login()

root.mainloop()