import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk, Canvas, Scrollbar

class Course:
    def __init__(self, code, name, credit_hours, lecture_hours, practical_hours, semester, course_type, prerequisites=None):
        self.code = code
        self.name = name
        self.credit_hours = credit_hours
        self.lecture_hours = lecture_hours
        self.practical_hours = practical_hours
        self.semester = semester
        self.course_type = course_type
        self.prerequisites = prerequisites if prerequisites is not None else []

    def add_prerequisite(self, prerequisite):
        self.prerequisites.append(prerequisite)


class Student:
    def __init__(self):
        self.semester = 0
        self.cgpa = 0.0
        self.passed_courses = []
        self.failed_courses = []
        self.registered_courses = []

    def set_semester(self, semester):
        self.semester = semester

    def set_cgpa(self, cgpa):
        self.cgpa = cgpa

    def add_passed_course(self, course_code):
        self.passed_courses.append(course_code)

    def add_failed_course(self, course_code):
        self.failed_courses.append(course_code)

    def can_register_for_course(self, course):
        if course.semester > self.semester:
            return "You cannot register for this course because it is offered in a higher semester than your current semester."
        if any(prerequisite not in self.passed_courses for prerequisite in course.prerequisites):
            missing_prerequisites = [prerequisite for prerequisite in course.prerequisites if prerequisite not in self.passed_courses]
            return f"You cannot register for this course because you have not passed the following prerequisite(s): {', '.join(missing_prerequisites)}"
        max_credit_hours = self.max_credit_hours()
        if course.credit_hours + sum(course.credit_hours for course in self.registered_courses) > max_credit_hours:
            return f"You cannot register for this course because it would exceed the maximum credit hour limit of {max_credit_hours} credit hours per semester."
        return None

    def enroll_course(self, course):
        registration_status = self.can_register_for_course(course)
        if registration_status:
            return registration_status
        elif course.code in [c.code for c in self.registered_courses]:
            return "You are already enrolled in this course."
        else:
            self.registered_courses.append(course)
            return f"Enrolled in course: {course.name}"

    def drop_course(self, course_code):
        for course in self.registered_courses:
            if course.code == course_code:
                self.registered_courses.remove(course)
                return f"Dropped course: {course.name}"
        return "Course not found in registered courses."

    def view_enrolled_courses(self):
        return self.registered_courses

    def max_credit_hours(self):
        if self.cgpa < 1.67:
            return 13  # Half load
        elif 1.67 <= self.cgpa < 3.0:
            return 20  # Full load
        else:
            return 22  # Overload


class KnowledgeBase:
    def __init__(self):
        self.courses = {}

    def add_course(self, course):
        self.courses[course.code] = course

    def get_course_by_code(self, code):
        return self.courses.get(code)

    def get_all_course_codes(self):
        return list(self.courses.keys())

    def advise_courses(self, student):
        failed_courses_set = set(student.failed_courses)
        eligible_courses = [course for course in self.courses.values() if course.semester <= student.semester and course.code not in student.passed_courses]
        advised_courses = sorted(eligible_courses, key=lambda course: course.code in failed_courses_set, reverse=True)
        return advised_courses

    def delete_course(self, code):
        if code in self.courses:
            del self.courses[code]
            return f"Course {code} deleted successfully."
        else:
            return "Course not found."


class AcademicAdvisorApp:
    def __init__(self, root, knowledge_base):
        self.root = root
        self.knowledge_base = knowledge_base

        self.root.title("Academic Advisor System")
        self.root.geometry("800x600")

        self.main_frame = tk.Frame(root, bg='#e0f7fa')
        self.main_frame.pack(fill="both", expand=True)

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame(self.main_frame)
        tk.Label(self.main_frame, text="Welcome to the Academic Advisor System", font=("Helvetica", 18, "bold"), bg='#e0f7fa', fg='#00796b').pack(pady=20)

        tk.Button(self.main_frame, text="Student Portal", command=self.student_portal, font=("Helvetica", 14, "bold"), bg='#00796b', fg='white', width=20).pack(pady=10)
        tk.Button(self.main_frame, text="Advisor Portal", command=self.advisor_portal, font=("Helvetica", 14, "bold"), bg='#00796b', fg='white', width=20).pack(pady=10)

    def student_portal(self):
        self.clear_frame(self.main_frame)
        self.student = Student()

        tk.Label(self.main_frame, text="Student Portal", font=("Helvetica", 18, "bold"), bg='#e0f7fa', fg='#00796b').grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self.main_frame, text="Enter your semester:", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).grid(row=1, column=0, sticky='e', pady=5)
        self.semester_entry = tk.Entry(self.main_frame, font=("Helvetica", 12))
        self.semester_entry.grid(row=1, column=1, sticky='w', pady=5)

        tk.Label(self.main_frame, text="Enter your CGPA:", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).grid(row=2, column=0, sticky='e', pady=5)
        self.cgpa_entry = tk.Entry(self.main_frame, font=("Helvetica", 12))
        self.cgpa_entry.grid(row=2, column=1, sticky='w', pady=5)

        tk.Label(self.main_frame, text="Enter the codes of your passed courses (separated by comma):", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).grid(row=3, column=0, sticky='e', pady=5)
        self.passed_courses_entry = tk.Entry(self.main_frame, width=50, font=("Helvetica", 12))
        self.passed_courses_entry.grid(row=3, column=1, sticky='w', pady=5)

        tk.Label(self.main_frame, text="Enter the codes of your failed courses (separated by comma):", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).grid(row=4, column=0, sticky='e', pady=5)
        self.failed_courses_entry = tk.Entry(self.main_frame, width=50, font=("Helvetica", 12))
        self.failed_courses_entry.grid(row=4, column=1, sticky='w', pady=5)

        tk.Button(self.main_frame, text="Submit", command=self.submit_student_info, bg='#00796b', fg='white', font=("Helvetica", 12)).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_main_menu, bg='#00796b', fg='white', font=("Helvetica", 12)).grid(row=6, column=0, columnspan=2, pady=10)

    def submit_student_info(self):
        try:
            semester = int(self.semester_entry.get())
            cgpa = float(self.cgpa_entry.get())
            self.student.set_semester(semester)
            self.student.set_cgpa(cgpa)

            passed_courses_input = self.passed_courses_entry.get().upper()
            passed_courses = passed_courses_input.split(",")
            for course_code in passed_courses:
                self.student.add_passed_course(course_code.strip())

            failed_courses_input = self.failed_courses_entry.get().upper()
            failed_courses = failed_courses_input.split(",")
            for course_code in failed_courses:
                self.student.add_failed_course(course_code.strip())

            self.show_advised_courses()

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid inputs for semester and CGPA.")

    def show_advised_courses(self):
        self.clear_frame(self.main_frame)
        eligible_courses = self.knowledge_base.advise_courses(self.student)
        remaining_credit_hours = self.student.max_credit_hours() - sum(course.credit_hours for course in self.student.registered_courses)

        if eligible_courses:
            tk.Label(self.main_frame, text=f"You can enroll in {remaining_credit_hours} credit hours.", font=("Helvetica", 14, "bold"), bg='#e0f7fa', fg='#00796b').pack(pady=10)
            tk.Label(self.main_frame, text="Advised Courses for Registration:", font=("Helvetica", 14, "bold"), bg='#e0f7fa', fg='#00796b').pack(pady=10)

            # Create a scrollable frame
            canvas = Canvas(self.main_frame, bg='#e0f7fa')
            scroll_y = Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#e0f7fa')

            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scroll_y.set)

            for course in eligible_courses:
                tk.Label(scrollable_frame, text=f"{course.code}: {course.name} - Credit Hours: {course.credit_hours}", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).pack()

            canvas.pack(side="left", fill="both", expand=True)
            scroll_y.pack(side="right", fill="y")

            self.course_code_entry = tk.Entry(self.main_frame, font=("Helvetica", 12))
            self.course_code_entry.pack(pady=5)
            tk.Button(self.main_frame, text="Enroll in Course", command=self.enroll_course, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)
            tk.Button(self.main_frame, text="View Enrolled Courses", command=self.view_enrolled_courses, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)
            tk.Button(self.main_frame, text="Drop Course", command=self.drop_course, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)
            tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_main_menu, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)
        else:
            tk.Label(self.main_frame, text="No courses advised for the given semester.", font=("Helvetica", 14, "bold"), bg='#e0f7fa', fg='#00796b').pack(pady=10)
            tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_main_menu, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)

    def enroll_course(self):
        course_code = self.course_code_entry.get().upper()
        course = self.knowledge_base.get_course_by_code(course_code)
        if course:
            message = self.student.enroll_course(course)
            messagebox.showinfo("Enrollment Status", message)
            self.show_advised_courses()  # Update advised courses list after enrolling
        else:
            messagebox.showerror("Invalid Course", "Course not found.")

    def view_enrolled_courses(self):
        enrolled_courses = self.student.view_enrolled_courses()
        self.clear_frame(self.main_frame)
        tk.Label(self.main_frame, text="Enrolled Courses:", font=("Helvetica", 14, "bold"), bg='#e0f7fa', fg='#00796b').pack(pady=10)

        # Create a scrollable frame
        canvas = Canvas(self.main_frame, bg='#e0f7fa')
        scroll_y = Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#e0f7fa')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        if enrolled_courses:
            for course in enrolled_courses:
                tk.Label(scrollable_frame, text=f"{course.code}: {course.name}", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).pack()
        else:
            tk.Label(scrollable_frame, text="No courses enrolled.", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).pack()

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_main_menu, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)

    def drop_course(self):
        course_code = self.course_code_entry.get().upper()
        message = self.student.drop_course(course_code)
        messagebox.showinfo("Drop Course Status", message)
        self.show_advised_courses()  # Update advised courses list after dropping

    def advisor_portal(self):
        self.clear_frame(self.main_frame)
        tk.Label(self.main_frame, text="Advisor Portal", font=("Helvetica", 18, "bold"), bg='#e0f7fa', fg='#00796b').pack(pady=20)

        tk.Button(self.main_frame, text="Add a New Course", command=self.add_new_course, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)
        tk.Button(self.main_frame, text="Add Prerequisites to a Course", command=self.add_prerequisites, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)
        tk.Button(self.main_frame, text="Display All Courses", command=self.display_all_courses, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)
        tk.Button(self.main_frame, text="Delete a Course", command=self.delete_course, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_main_menu, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)

    def add_new_course(self):
        self.clear_frame(self.main_frame)
        tk.Label(self.main_frame, text="Add New Course", font=("Helvetica", 18, "bold"), bg='#e0f7fa', fg='#00796b').pack(pady=20)

        fields = ["Code", "Name", "Credit Hours", "Lecture Hours", "Practical Hours", "Semester", "Type", "Prerequisites"]
        self.course_entries = {}

        for field in fields:
            tk.Label(self.main_frame, text=f"Enter {field}:", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).pack(pady=5)
            entry = tk.Entry(self.main_frame, font=("Helvetica", 12))
            entry.pack(pady=5)
            self.course_entries[field] = entry

        tk.Button(self.main_frame, text="Submit", command=self.save_new_course, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_main_menu, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=10)

    def save_new_course(self):
        code = self.course_entries["Code"].get()
        name = self.course_entries["Name"].get()
        credit_hours = int(self.course_entries["Credit Hours"].get())
        lecture_hours = int(self.course_entries["Lecture Hours"].get())
        practical_hours = int(self.course_entries["Practical Hours"].get())
        semester = int(self.course_entries["Semester"].get())
        course_type = self.course_entries["Type"].get()
        prerequisites = self.course_entries["Prerequisites"].get().split(",")

        new_course = Course(code, name, credit_hours, lecture_hours, practical_hours, semester, course_type, [p.strip() for p in prerequisites])
        self.knowledge_base.add_course(new_course)
        messagebox.showinfo("Success", f"New course '{code}' added successfully.")
        self.advisor_portal()

    def add_prerequisites(self):
        self.clear_frame(self.main_frame)
        tk.Label(self.main_frame, text="Add Prerequisites", font=("Helvetica", 18, "bold"), bg='#e0f7fa', fg='#00796b').pack(pady=20)

        tk.Label(self.main_frame, text="Enter the code of the course:", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).pack(pady=5)
        self.course_code_entry = tk.Entry(self.main_frame, font=("Helvetica", 12))
        self.course_code_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Enter the code of the prerequisite course:", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).pack(pady=5)
        self.prerequisite_code_entry = tk.Entry(self.main_frame, font=("Helvetica", 12))
        self.prerequisite_code_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Submit", command=self.save_prerequisites, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_main_menu, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)

    def save_prerequisites(self):
        course_code = self.course_code_entry.get()
        prerequisite_code = self.prerequisite_code_entry.get()

        if course_code in self.knowledge_base.courses and prerequisite_code in self.knowledge_base.courses:
            self.knowledge_base.courses[course_code].add_prerequisite(prerequisite_code)
            messagebox.showinfo("Success", f"Prerequisite '{prerequisite_code}' added for course '{course_code}' successfully.")
        else:
            messagebox.showerror("Error", "Course or prerequisite not found.")
        self.advisor_portal()

    def display_all_courses(self):
        self.clear_frame(self.main_frame)
        tk.Label(self.main_frame, text="All Courses in Knowledge Base", font=("Helvetica", 18, "bold"), bg='#e0f7fa', fg='#00796b').pack(pady=20)

        # Create a scrollable frame
        canvas = Canvas(self.main_frame, bg='#e0f7fa')
        scroll_y = Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#e0f7fa')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        if self.knowledge_base.courses:
            for course in self.knowledge_base.courses.values():
                tk.Label(scrollable_frame, text=f"{course.code}: {course.name}", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).pack()
        else:
            tk.Label(scrollable_frame, text="No courses in the knowledge base.", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).pack()

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_main_menu, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)

    def delete_course(self):
        self.clear_frame(self.main_frame)
        tk.Label(self.main_frame, text="Delete Course", font=("Helvetica", 18, "bold"), bg='#e0f7fa', fg='#00796b').pack(pady=20)

        tk.Label(self.main_frame, text="Enter the code of the course to delete:", bg='#e0f7fa', fg='#00796b', font=("Helvetica", 12)).pack(pady=5)
        self.delete_course_code_entry = tk.Entry(self.main_frame, font=("Helvetica", 12))
        self.delete_course_code_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Submit", command=self.remove_course, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Main Menu", command=self.create_main_menu, bg='#00796b', fg='white', font=("Helvetica", 12)).pack(pady=5)

    def remove_course(self):
        code = self.delete_course_code_entry.get()
        message = self.knowledge_base.delete_course(code)
        messagebox.showinfo("Course Deletion", message)
        self.advisor_portal()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

def load_data():
    knowledge_base = KnowledgeBase()

    # Load courses data
    df = pd.read_excel("D:\\University\\Semester 6\\KBS\\new.xlsx")
    for index, row in df.iterrows():
        course_info = (row["Code"], row["Course Name"], row["CH"], row["LCT"], row["LAB"], row["Semester"], row["Type"],[] if pd.isnull(row["prerequisites"]) else [prerequisite.strip() for prerequisite in row["prerequisites"].split(",")])
        course = Course(*course_info)
        knowledge_base.add_course(course)

    # Load UC courses data
    df_uc_courses = pd.read_excel("D:\\University\\Semester 6\\KBS\\new.xlsx", sheet_name="uc_courses")
    for index, row in df_uc_courses.iterrows():
        course_info = (row["Course Code"], row["Course Name"], row["CH "], 0, 0, 0, "Unknown", [])
        course = Course(*course_info)
        knowledge_base.add_course(course)

    return knowledge_base

def main():
    knowledge_base = load_data()
    root = tk.Tk()
    app = AcademicAdvisorApp(root, knowledge_base)
    root.mainloop()

if __name__ == "__main__":
    main()
