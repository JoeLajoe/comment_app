from flask import Flask, render_template, request, send_file
import random
import os

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

app = Flask(__name__)

# Validate that the student's name contains only alphanumeric characters (with spaces)
def validate_name(name):
    if not name or not name.replace(" ", "").isalnum():
        return False
    return True

# Function to write comments to file
def write_comments_to_file(students, subject, grade, write_mode):
    output_dir = "generate_comments"  # Change this to your new folder name
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"Grade_{grade}_{subject.capitalize()}_comments.txt")

    try:
        with open(output_file, write_mode) as file:
            for student, code in students.items():
                comment = random.choice(subject_comments[subject][code - 1]).format(student)
                file.write(f"{student}, {code}: {comment}\n")
        return output_file
    except Exception as e:
        print(f"Error writing to file: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_comments', methods=['POST'])
def generate_comments():
    if request.method == 'POST':
        # Get form data
        grade = int(request.form['grade'])
        subject = request.form['subject'].lower()

        # Ensure the subject is valid
        if subject not in subject_comments:
            return "Invalid subject. Please try again."

        # Validate grade (5-8)
        if grade not in [5, 6, 7, 8]:
            return "Invalid grade. Please enter a grade between 5 and 8."

        students = {}
        student_entries = request.form['students'].split('\n')

        # Validate and add students
        for entry in student_entries:
            if entry.strip():  # Ignore empty lines
                try:
                    name, code = entry.split(',')
                    name = name.strip()
                    code = int(code.strip())

                    # Validate name and code
                    if validate_name(name) and code in [1, 2, 3]:
                        students[name] = code
                    else:
                        print(f"Skipping invalid entry: {entry.strip()}")  # Debug print

                except ValueError:
                    print(f"Invalid format for entry: {entry.strip()}")  # Debug print
                    continue

        # If no valid students were entered, show an error
        if not students:
            return "No valid students added. Please try again."

        # Determine file mode
        write_mode = 'a' if request.form.get('append') == 'y' else 'w'

        # Generate comments and save to file
        output_file = write_comments_to_file(students, subject, grade, write_mode)

        if output_file:
            # Send the file to the user for download
            response = send_file(output_file, as_attachment=True)

            # After sending, delete the file to clean up
            os.remove(output_file)

            return response
        else:
            return "There was an error generating the comments file."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)