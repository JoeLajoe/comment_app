import random

# Import subject comment dictionaries
from comments.conduct_comments import conduct_comments
from comments.english_comments import english_comments
from comments.history_comments import history_comments
from comments.reading_comments import reading_comments
from comments.religion_comments import religion_comments
from comments.social_comments import social_comments

# Dictionary to map subjects to their corresponding comment sets
subject_comments = {
    "conduct": conduct_comments,
    "english": english_comments,
    "history": history_comments,
    "reading": reading_comments,
    "religion": religion_comments,
    "social": social_comments
}

def validate_name(name):
    # Ensure name is not empty and contains no special characters or commas
    if not name or not name.replace(" ", "").isalnum():
        print("Invalid name. Names should only contain letters, numbers, and spaces.")
        return False
    return True

def get_grade():
    while True:
        try:
            grade = int(input("Enter grade level (5, 6, 7, or 8):"))
            if grade in [5, 6, 7, 8]:
                return grade
            else:
                print("Invalid grade level. Please enter 5, 6, 7, or 8.")
        except ValueError:
            print("Invalid input. Please enter a numeric grade level.")

def get_student_entries():
    students = {}
    print("Enter student names and comment codes in the format: Name, Code")
    print("Type 'done' when finished.")
    
    while True:
        entry = input("Enter student and code: ").strip()
        if entry.lower() == "done":
            break
        try:
            name, code = entry.split(",")
            name = name.strip()
            code = int(code.strip())
            
            if validate_name(name) and code in [1, 2, 3]:
                students[name] = code
            else:
                print("Invalid input. Make sure the code is 1, 2, or 3 and name is valid.")
        except ValueError:
            print("Invalid format. Please enter in the format: Name, Code")
    return students

def prompt_for_file_mode():
    write_mode = input("Would you like to append to the file? (y/n): ").strip().lower()
    if write_mode == "y":
        return "a"
    elif write_mode == "n":
        return "w"
    else:
        print("Invalid option. Defaulting to overwrite mode.")
        return "w"

def write_comments_to_file(output_file, students, subject, grade, write_mode):
    try:
        with open(output_file, write_mode) as file:
            for student, code in students.items():
                comment = random.choice(subject_comments[subject][code]).format(student)
                file.write(f"{student}, {code}: {comment}\n")
        print(f"Comments have been written to {output_file}")
    except PermissionError:
        print("Permission denied: Unable to write to the file.")
    except IOError as e:
        print(f"An unexpected error occurred while writing to the file: {e}")

def generate_comments():
    grade = get_grade()
    students = get_student_entries()
    
    if not students:
        print("No students added. Exiting program.")
        return
    
    subject = input("Please select a subject (Conduct, Social, Religion, English, Reading, History): ").strip().lower()
    if subject not in subject_comments:
        print("Invalid subject selected.")
        return
    
    output_file = f"Grade_{grade}_{subject.capitalize()}_comments.txt"
    write_mode = prompt_for_file_mode()

    write_comments_to_file(output_file, students, subject, grade, write_mode)

if __name__ == "__main__":
    generate_comments()
