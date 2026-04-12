from flask import Flask, render_template, request, jsonify
import random
import os
import re
import shutil
import zipfile
from datetime import datetime

app = Flask(__name__)

# Keywords for detecting file ratings
rating_keywords = {
    "best": "Best",
    "be": "Best",
    "avg": "Average",
    "av": "Average",
    "wo": "Worst",
    "wor": "Worst",
    "worst": "Worst",
    "sol": "Solution",
    "solution": "Solution",
    "ques": "Question",
    "question": "Question",
}

# Required files per folder type for Course
course_required = {
    "Course Description": {"files": 1, "naming": ["CourseDescription"]},
    "Course Log": {"files": 1, "naming": ["Course-Log"]},
    "Course Module": {"files": 1, "naming": ["Course-Module"]},
    "Course Outline": {"files": 1, "naming": ["Course-Module", "Course-Outline"]},
    "Attendance": {"files": 1, "naming": ["Attendance"]},
    "Final Term": {
        "files": 5,
        "naming": [
            "FinalTerm-Question",
            "FinalTerm-Solution",
            "FinalTerm-Best",
            "FinalTerm-Average",
            "FinalTerm-Worst",
        ],
        "ratings": ["Question", "Solution", "Best", "Average", "Worst"],
    },
    "Mid Term": {
        "files": 5,
        "naming": [
            "MidTerm-Question",
            "MidTerm-Solution",
            "MidTerm-Best",
            "MidTerm-Average",
            "MidTerm-Worst",
        ],
        "ratings": ["Question", "Solution", "Best", "Average", "Worst"],
    },
    "Result": {
        "files": 3,
        "naming": ["Result-Marksheet", "Result-Gradesheet", "Result-CLO-Attainment"],
        "subnames": ["Marksheet", "Gradesheet", "CLO-Attainment"],
    },
}

course_subfolder_required = {
    "Assignment": {
        "min": 1,
        "max": 4,
        "files": 5,
        "ratings": ["Question", "Solution", "Best", "Average", "Worst"],
        "prefix": "Assignment",
    },
    "Quiz": {
        "min": 1,
        "max": 4,
        "files": 5,
        "ratings": ["Question", "Solution", "Best", "Average", "Worst"],
        "prefix": "Quiz",
    },
}

# Required files per folder type for Lab
lab_required = {
    "Course Description": {"files": 1, "naming": ["CourseDescription"]},
    "Course Log": {"files": 1, "naming": ["Course-Log"]},
    "Lab Module": {"files": 1, "naming": ["Lab-Module"]},
    "Attendance": {"files": 1, "naming": ["Attendance"]},
    "Final Term": {
        "files": 5,
        "naming": [
            "FinalTerm-Question",
            "FinalTerm-Solution",
            "FinalTerm-Best",
            "FinalTerm-Average",
            "FinalTerm-Worst",
        ],
        "ratings": ["Question", "Solution", "Best", "Average", "Worst"],
    },
    "Result": {
        "files": 3,
        "naming": ["Result-Marksheet", "Result-Gradesheet", "Result-CLO-Attainment"],
        "subnames": ["Marksheet", "Gradesheet", "CLO-Attainment"],
    },
}

lab_subfolder_required = {
    "Task": {
        "min": 14,
        "max": 16,
        "files": 5,
        "ratings": ["Question", "Solution", "Best", "Average", "Worst"],
        "prefix": "Task",
    },
}

# Alternative folder names
quiz_alternatives = ["Quiz", "Quizs", "Quizes"]
assignment_alternatives = ["Assignment", "Assignments"]

# Format mapping for file naming
format_mapping = {
    "Course": {
        "Assignment": "{session}-{dept}-{section}-{course}-Assignment{number}-{rating}",
        "Quiz": "{session}-{dept}-{section}-{course}-Quiz{number}-{rating}",
        "Attendance": "{session}-{dept}-{section}-{course}-Attendance",
        "Course Description": "{session}-{dept}-{section}-{course}-CourseDescription-Form",
        "Course Log": "{session}-{dept}-{section}-{course}-Course-Log",
        "Course Module": "{session}-{dept}-{section}-{course}-Course-Module",
        "Mid Term": "{session}-{dept}-{section}-{course}-MidTerm-{rating}",
        "Final Term": "{session}-{dept}-{section}-{course}-FinalTerm-{rating}",
        "Result": "{session}-{dept}-{section}-{course}-Result",
    },
    "Lab": {
        "Task": "{session}-{dept}-{section}-{course}-Task{number}-{rating}",
        "Attendance": "{session}-{dept}-{section}-{course}-Attendance",
        "Course Description": "{session}-{dept}-{section}-{course}-CourseDescription-Form",
        "Course Log": "{session}-{dept}-{section}-{course}-Course-Log",
        "Lab Module": "{session}-{dept}-{section}-{course}-Lab-Module",
        "Final Term": "{session}-{dept}-{section}-{course}-FinalTerm-{rating}",
        "Result": "{session}-{dept}-{section}-{course}-Result",
    },
}

# Add title options
title_options = ["Mr.", "Ms.", "Mrs.", "Dr."]


def create_folders(base_path, folder_structure):
    """Create folders based on the provided structure."""
    for folder, subfolders in folder_structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        for subfolder in subfolders:
            os.makedirs(os.path.join(folder_path, subfolder), exist_ok=True)


def create_backup(base_path):
    """Create a backup of the folder structure before renaming."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder_name = f"backup_{timestamp}"

    # Create backup in the parent directory of base_path
    parent_dir = os.path.dirname(base_path)
    backup_path = os.path.join(parent_dir, backup_folder_name)

    # Create a zip file backup
    zip_path = backup_path + ".zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, base_path)
                zipf.write(file_path, arcname)

    return zip_path


def generate_sessions():
    """Generate session options from 2015 to current year."""
    current_year = datetime.now().year
    sessions = []
    for year in range(2015, current_year + 1):
        sessions.extend([f"Fall {year}", f"Spring {year}"])
    return sessions


@app.route("/create-folders", methods=["POST"])
def create_folders_route():
    """Endpoint to create folders dynamically."""
    data = request.json
    base_path = data.get("base_path")
    session_folder = (
        data.get("session").split(" ")[0] + " " + data.get("session").split(" ")[1][-2:]
    )
    dept_folder = data.get("dept")
    section_folder = data.get("section")
    course_folder = data.get("course")
    course_folder = " ".join(word.capitalize() for word in course_folder.split())
    folder_type = data.get("type")
    title = data.get("title")
    teacher_name = data.get("teacher_name")

    if not base_path or not os.path.isdir(base_path):
        return jsonify({"error": "Invalid base path provided"}), 400

    # Capitalize teacher name
    formatted_name = " ".join(word.capitalize() for word in teacher_name.split())
    teacher_folder = f"{title} {formatted_name}"

    folder_structure = course_structure if folder_type == "Course" else lab_structure
    final_path = os.path.join(
        base_path,
        teacher_folder,
        session_folder,
        dept_folder,
        f"Semester {section_folder[0]}",
        section_folder,
        course_folder,
    )

    create_folders(final_path, folder_structure)
    return jsonify(
        {"message": f"{folder_type} folder structure created at {final_path}"}
    ), 200


@app.route("/rename-files", methods=["POST"])
def rename_files_route():
    """Endpoint to rename files based on the naming convention."""
    data = request.json
    base_path = data.get("base_path")

    if not base_path or not os.path.isdir(base_path):
        return jsonify({"error": "Invalid base path provided"}), 400

    # Create backup before renaming
    try:
        backup_path = create_backup(base_path)
        print(f"Backup created at: {backup_path}")
    except Exception as e:
        return jsonify({"error": f"Failed to create backup: {str(e)}"}), 500

    renamed_files = []

    # Check if base_path ends with a session folder (e.g., "Spring 25", "Fall 24")
    base_folder_name = os.path.basename(base_path)
    session_match = re.search(
        r"(Fall|Spring)\s*(\d{2})", base_folder_name, re.IGNORECASE
    )

    if session_match:
        # Direct session folder - rename only this session
        session = session_match.group(1)[0].upper() + session_match.group(2)
        renamed_files.extend(process_session_path(base_path, session))
    else:
        # Teacher folder or higher level - process all sessions within
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path):
                # Check if this is a session folder
                session_match = re.search(
                    r"(Fall|Spring)\s*(\d{2})", item, re.IGNORECASE
                )
                if session_match:
                    session = session_match.group(1)[0].upper() + session_match.group(2)
                    renamed_files.extend(process_session_path(item_path, session))

    return jsonify({"renamed_files": renamed_files}), 200


def process_session_path(session_path, session):
    """Process a single session path for file renaming."""
    renamed_files = []

    # Walk through department folders
    for dept_folder in os.listdir(session_path):
        dept_path = os.path.join(session_path, dept_folder)
        if os.path.isdir(dept_path) and dept_folder in ["AI", "DS", "SE", "CS"]:
            # Walk through semester folders
            for semester_folder in os.listdir(dept_path):
                semester_path = os.path.join(dept_path, semester_folder)
                if os.path.isdir(semester_path) and semester_folder.lower().startswith(
                    "semester"
                ):
                    # Walk through section folders
                    for section_folder in os.listdir(semester_path):
                        section_path = os.path.join(semester_path, section_folder)
                        if os.path.isdir(section_path):
                            # Walk through course folders
                            for course_folder in os.listdir(section_path):
                                course_path = os.path.join(section_path, course_folder)
                                if os.path.isdir(course_path):
                                    # Get course short form
                                    course_short = get_course_short_form(course_folder)

                                    # Detect if it's a Lab or Course
                                    folder_type = detect_folder_type(course_path)

                                    # Rename files using the new short form
                                    renamed_files.extend(
                                        rename_files(
                                            course_path,
                                            session,
                                            dept_folder,
                                            semester_folder,
                                            section_folder,
                                            course_short,
                                            folder_type,
                                        )
                                    )

    return renamed_files


def detect_folder_type(course_path):
    """Determine if a folder represents a Lab or a Course."""
    for root, dirs, files in os.walk(course_path):
        # Look for Lab-specific folders
        if any(folder in dirs for folder in ["Task", "Lab Module"]):
            return "Lab"

        # Look for typical Course-specific folders
        if any(
            folder in dirs
            for folder in ["Assignment", "Quiz", "Final Term", "Mid Term"]
        ):
            return "Course"
    return "Course"  # Default to Course if unclear


def rename_files(course_path, session, dept, semester, section, course, folder_type):
    """Rename files based on the defined naming conventions and specific folder rules."""
    renamed_files = []

    for root, dirs, files in os.walk(course_path):
        # Skip unwanted folders
        # if 'Final Term' in root or 'Mid Term' in root:
        # continue

        file_type = os.path.basename(root)  # Folder name
        print(f"Processing folder: {root}, file_type: {file_type}, files: {files}")

        # Handle missing solution files for Tasks, Assignments, and Quizzes
        print(f"Checking for missing solution file in folder: {root}")

        if (
            file_type.startswith("Task")
            or file_type.startswith("Assignment")
            or file_type.startswith("Quiz")
            or file_type.startswith("Final")
            or file_type.startswith("Mid")
        ):
            print(f"Folder {file_type} is eligible for solution file handling.")
            solution_file = None
            question_file = None

            # Remove spaces from file_type (e.g., "Task 10" -> "Task10")
            cleaned_file_type = file_type.replace(" ", "")

            # Check for existing solution and question file and rename it
            for file in files:
                # Normalize file name for easier matching
                file_lower = file.lower()
                matched_type = None

                # Skip already renamed files
                if file.startswith(session):
                    # Check if this is actually a Solution file, not just any renamed file
                    if "solution" in file_lower:
                        solution_file = os.path.join(root, file)
                    continue
                # Check if file name contains any keyword
                for keyword, file_type in rating_keywords.items():
                    if keyword in file_lower:
                        matched_type = file_type
                        break  # Stop searching once a match is found

                if matched_type:
                    print("Matched file:", file, "Type:", matched_type)
                    # Skip already renamed files
                    if file.startswith(session):
                        continue

                    # Generate new file name
                    question_file = os.path.join(root, file)
                    new_question_name = f"{session}-{dept}-{section}-{course}-{cleaned_file_type}-{matched_type}{os.path.splitext(file)[-1]}"
                    new_question_path = os.path.join(root, new_question_name)

                    try:
                        os.rename(question_file, new_question_path)
                        renamed_files.append(
                            {"original": question_file, "new": new_question_path}
                        )
                        print(f"Renamed file: {new_question_path}")
                    except Exception as e:
                        print(f"Error renaming file: {e}")
                else:
                    print(f"Skipped (no match): {file}")

            # If no solution file exists, create one from the "best" file
            if not solution_file:
                print("Solution file is missing, attempting to create one.")
                best_file_path = None

                # Search for the "best" file - check both original filenames and renamed files
                for file in files:
                    file_lower = file.lower()

                    # Check if the file matches the "best" category in original name
                    if any(keyword in file_lower for keyword in ["best", "be"]):
                        best_file_path = os.path.join(root, file)
                        break

                # If not found in original files, check already renamed files
                if not best_file_path:
                    for file in files:
                        if file.startswith(session) and "-Best-" in file:
                            best_file_path = os.path.join(root, file)
                            break

                if best_file_path:
                    new_solution_path = os.path.join(
                        root,
                        f"{session}-{dept}-{section}-{course}-{cleaned_file_type}-Solution{os.path.splitext(best_file_path)[-1]}",
                    )
                    try:
                        shutil.copy(best_file_path, new_solution_path)
                        renamed_files.append(
                            {"original": best_file_path, "new": new_solution_path}
                        )
                        print(f"Created solution file: {new_solution_path}")
                    except Exception as e:
                        print(f"Error copying file to create solution: {e}")
                else:
                    print("No 'best' file found to create a solution file.")

        # Handle Lab Module or Course Module
        if file_type in ["Lab Module", "Course Module"]:
            for file in files:
                # Skip already renamed files
                if file.startswith(session):
                    continue

                # Debugging: Check folder_type and file_type
                print(f"folder_type: {folder_type}, file_type: {file_type}")

                # Generate the new file name
                try:
                    # Use the appropriate format based on folder type and file type
                    new_name = format_mapping[folder_type][file_type].format(
                        session=session, dept=dept, section=section, course=course
                    )

                    # Create file paths
                    new_file_path = os.path.join(
                        root, new_name + os.path.splitext(file)[-1]
                    )
                    old_file_path = os.path.join(root, file)

                    # Rename the file
                    os.rename(old_file_path, new_file_path)
                    renamed_files.append(
                        {"original": old_file_path, "new": new_file_path}
                    )

                except KeyError as e:
                    print(
                        f"Error: Format for '{folder_type} - {file_type}' not found in mapping."
                    )
                except Exception as e:
                    print(f"Error renaming file '{file}': {e}")

        # Handle specific cases for Result sub-files
        elif file_type == "Result":
            for file in files:
                file_lower = file.lower()
                # Skip already renamed files
                if file.startswith(session):
                    continue
                if (
                    "marksheet" in file_lower
                    or "mark" in file_lower
                    or "ms" in file_lower
                    or "mk" in file_lower
                ):
                    new_name = f"{session}-{dept}-{section}-{course}-Result-Marksheet{os.path.splitext(file)[-1]}"
                elif (
                    "gradesheet" in file_lower
                    or "grade" in file_lower
                    or "gs" in file_lower
                    or "gd" in file_lower
                ):
                    new_name = f"{session}-{dept}-{section}-{course}-Result-Gradesheet{os.path.splitext(file)[-1]}"
                elif "clo attainment" in file_lower or "clo" in file_lower:
                    new_name = f"{session}-{dept}-{section}-{course}-Result-CLO-Attainment{os.path.splitext(file)[-1]}"
                else:
                    continue  # Skip unrelated files

                # Rename the file
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)
                try:
                    os.rename(old_path, new_path)
                    renamed_files.append({"original": old_path, "new": new_path})
                except Exception as e:
                    print(f"Error renaming file '{file}': {e}")

        # Handle other categories
        elif file_type in format_mapping[folder_type]:
            format_string = format_mapping[folder_type][file_type]
            for file in files:
                # Skip already renamed files
                if file.startswith(session):
                    continue

                # Determine the new file name
                new_name = format_string.format(
                    session=session, dept=dept, section=section, course=course
                )
                new_path = os.path.join(root, new_name + os.path.splitext(file)[-1])
                old_path = os.path.join(root, file)

                try:
                    os.rename(old_path, new_path)
                    renamed_files.append({"original": old_path, "new": new_path})
                except Exception as e:
                    print(f"Error renaming file '{file}': {e}")

        # Ensure the function only applies to Tasks, Assignments, Quizzes, Mid Term, and Final Term
        if folder_type == "Lab" and file_type.startswith("Task"):
            number_match = re.search(r"Task\\s*(\\d+)", file_type, re.IGNORECASE)
            if number_match:
                number = number_match.group(1)
                format_string = format_mapping[folder_type]["Task"]
            else:
                continue
        elif folder_type == "Course" and file_type.startswith(("Assignment", "Quiz")):
            number_match = re.search(
                r"(Assignment|Quiz)\\s*(\\d+)", file_type, re.IGNORECASE
            )
            if number_match:
                number = number_match.group(2)
                format_string = format_mapping[folder_type][number_match.group(1)]
            else:
                continue
        elif folder_type == "Course" and file_type.startswith("Mid"):
            number_match = re.search(r"Mid\\s*Term", file_type, re.IGNORECASE)
            if number_match:
                number = "1"
                format_string = format_mapping[folder_type]["Mid Term"]
            else:
                continue
        elif folder_type == "Course" and file_type.startswith("Final"):
            number_match = re.search(r"Final\\s*Term", file_type, re.IGNORECASE)
            if number_match:
                number = "1"
                format_string = format_mapping[folder_type]["Final Term"]
            else:
                continue
        else:
            continue

        # Gather existing ratings in the folder
        existing_ratings = set()
        for file in files:
            _, rating = extract_task_details(file)
            if rating != "Unknown":
                existing_ratings.add(rating)

        for file in files:
            # Skip already renamed files
            if file.startswith(session):
                continue

            file_path = os.path.join(root, file)
            _, rating = extract_task_details(file)

            # Assign random rating if 'Unknown' and ensure it's unique
            if rating == "Unknown":
                possible_ratings = {"Best", "Average", "Worst"} - existing_ratings
                if possible_ratings:
                    rating = random.choice(list(possible_ratings))
                    existing_ratings.add(rating)
                else:
                    rating = random.choice(["Best", "Average", "Worst"])

            try:
                new_name = format_string.format(
                    session=session,
                    dept=dept,
                    section=section,
                    course=course,
                    number=number,
                    rating=rating,
                )
                new_file_path = os.path.join(
                    root, new_name + os.path.splitext(file)[-1]
                )

                os.rename(file_path, new_file_path)
                renamed_files.append({"original": file_path, "new": new_file_path})
            except Exception as e:
                print(f"Error renaming file '{file}': {e}")

    return renamed_files


def extract_task_details(filename):
    print(f"Extracting details from: {filename}")

    # Extract task number (if any). Default to 'Unknown' if no digits found.
    task_number = "".join(filter(str.isdigit, filename)) or "Unknown"

    # If no task number, we might want to assign a default task number, e.g., '1' for simplicity
    if task_number == "Unknown":
        task_number = "1"  # Assign a default task number if none is found

    # Extract rating (if any). Check against the defined keywords
    rating = "Unknown"
    for keyword, mapped_rating in rating_keywords.items():
        if keyword in filename.lower():
            rating = mapped_rating
            print(
                f"Matched rating '{rating}' for keyword '{keyword}' in file '{filename}'"
            )

    if task_number == "Unknown":
        print(f"No task number found in '{filename}'")
    return task_number, rating


@app.route("/list-folders", methods=["POST"])
def list_folders():
    data = request.json
    base_path = data.get("base_path")

    if not base_path or not os.path.isdir(base_path):
        return jsonify({"error": "Invalid base path provided"}), 400

    folder_structure = {}
    for root, dirs, files in os.walk(base_path):
        relative_path = os.path.relpath(root, base_path)
        task_status = {}
        if "Task" in root:  # Check for tasks
            for file in files:
                _, rating = extract_task_details(file)
                if rating != "Unknown":
                    task_status[rating] = True
            # Compute missing ratings
            missing_ratings = {"Best", "Average", "Worst"} - set(task_status.keys())
            task_status["missing"] = list(missing_ratings)
        folder_structure[relative_path] = {
            "folders": dirs,
            "files": files,
            "task_status": task_status if task_status else None,
        }

    return jsonify({"folder_structure": folder_structure}), 200


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-sessions", methods=["GET"])
def get_sessions():
    """Endpoint to get dynamic session options."""
    sessions = generate_sessions()
    return jsonify({"sessions": sessions})


@app.route("/get-titles", methods=["GET"])
def get_titles():
    """Endpoint to get title options."""
    return jsonify({"titles": title_options})


@app.route("/get-teachers", methods=["POST"])
def get_teachers():
    """Get list of teachers from base path."""
    data = request.json
    base_path = data.get("base_path")

    if not base_path or not os.path.isdir(base_path):
        return jsonify({"error": "Invalid base path provided"}), 400

    teachers = []
    sessions = set()

    try:
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path):
                # Check if this looks like a teacher folder
                if any(
                    item.startswith(title) for title in ["Mr.", "Ms.", "Mrs.", "Dr."]
                ):
                    teachers.append(item)

                    # Get sessions for this teacher
                    for session_item in os.listdir(item_path):
                        session_path = os.path.join(item_path, session_item)
                        if os.path.isdir(session_path):
                            sessions.add(session_item)
                else:
                    # Check if it's a session folder directly
                    if any(keyword in item.lower() for keyword in ["fall", "spring"]):
                        sessions.add(item)
    except Exception as e:
        return jsonify({"error": f"Error reading directory: {str(e)}"}), 400

    return jsonify(
        {"teachers": sorted(teachers), "sessions": sorted(list(sessions))}
    ), 200


@app.route("/teacher-report", methods=["POST"])
def teacher_report():
    """Generate teacher-wise file reports with filtering."""
    data = request.json
    base_path = data.get("base_path")
    report_type = data.get("report_type", 1)
    selected_teachers = data.get("teachers", [])  # Empty means all teachers
    selected_sessions = data.get("sessions", [])  # Empty means all sessions

    if not base_path or not os.path.isdir(base_path):
        return jsonify({"error": "Invalid base path provided"}), 400

    report_data = []

    try:
        # Walk through teacher folders
        for item in os.listdir(base_path):
            teacher_path = os.path.join(base_path, item)
            if os.path.isdir(teacher_path):
                # Check if this looks like a teacher folder
                if any(
                    item.startswith(title) for title in ["Mr.", "Ms.", "Mrs.", "Dr."]
                ):
                    # Filter by selected teachers
                    if selected_teachers and item not in selected_teachers:
                        continue

                    teacher_folder = item
                    # Walk through sessions
                    for session_item in os.listdir(teacher_path):
                        session_path = os.path.join(teacher_path, session_item)
                        if os.path.isdir(session_path):
                            # Filter by selected sessions
                            if (
                                selected_sessions
                                and session_item not in selected_sessions
                            ):
                                continue

                            # Process the session folder structure
                            process_session_folder(
                                session_path,
                                teacher_folder,
                                session_item,
                                report_data,
                                report_type,
                            )
                else:
                    # If no teacher structure, treat as direct session folders
                    if selected_sessions and item not in selected_sessions:
                        continue
                    process_session_folder(
                        teacher_path, "No Teacher", item, report_data, report_type
                    )
    except Exception as e:
        return jsonify({"error": f"Error processing folders: {str(e)}"}), 400

    return jsonify({"report": report_data}), 200


def process_session_folder(
    session_path, teacher_name, session_name, report_data, report_type
):
    """Process a session folder and extract course information."""
    try:
        for dept_item in os.listdir(session_path):
            dept_path = os.path.join(session_path, dept_item)
            if os.path.isdir(dept_path) and dept_item in ["AI", "DS", "SE", "CS"]:
                for semester_item in os.listdir(dept_path):
                    semester_path = os.path.join(dept_path, semester_item)
                    if os.path.isdir(
                        semester_path
                    ) and semester_item.lower().startswith("semester"):
                        for section_item in os.listdir(semester_path):
                            section_path = os.path.join(semester_path, section_item)
                            if os.path.isdir(section_path):
                                for course_item in os.listdir(section_path):
                                    course_path = os.path.join(
                                        section_path, course_item
                                    )
                                    if os.path.isdir(course_path):
                                        course_info = f"{session_name}/{dept_item}/{semester_item}/{section_item}/{course_item}"

                                        if report_type == 1:
                                            files_info = analyze_course_files(
                                                course_path
                                            )
                                            report_data.append(
                                                {
                                                    "teacher": teacher_name,
                                                    "course_info": course_info,
                                                    "files": files_info,
                                                }
                                            )
                                        else:
                                            completion_status = get_completion_status(
                                                course_path
                                            )
                                            report_data.append(
                                                {
                                                    "teacher": teacher_name,
                                                    "course_info": course_info,
                                                    "status": completion_status,
                                                }
                                            )
    except Exception as e:
        print(f"Error processing session folder {session_path}: {str(e)}")


def is_lab_course(course_path):
    """Detect if a course folder is a Lab or Course by checking folder names."""
    for root, dirs, files in os.walk(course_path):
        for d in dirs:
            if d.lower() == "task" or d.lower() == "lab module":
                return True
            if d.lower() in [
                "assignment",
                "assignments",
                "quiz",
                "quizs",
                "quizes",
                "mid term",
            ]:
                return False
    return False


def get_folder_status(
    folder_name, files, subdirs, folder_type, dir_list=None, parent_root=None
):
    """Calculate the status of a folder based on required files and naming conventions."""
    dirs = dir_list if dir_list is not None else []
    root = parent_root if parent_root else ""
    status = {
        "color": "red",
        "percentage": 0,
        "missing": [],
        "naming_issues": [],
        "total_required": 0,
        "total_present": 0,
    }

    is_lab = folder_type == "Lab"
    required = lab_required if is_lab else course_required
    subfolder_required = lab_subfolder_required if is_lab else course_subfolder_required

    if folder_name in required:
        req = required[folder_name]
        status["total_required"] = req["files"]

        if folder_name in [
            "Course Description",
            "Course Log",
            "Course Module",
            "Course Outline",
            "Lab Module",
            "Attendance",
        ]:
            status["total_required"] = 1
            status["total_present"] = len(files) if len(files) <= 1 else 1

            if len(files) == 1:
                file_lower = files[0].lower()
                naming_ok = any(n.lower() in file_lower for n in req["naming"])
                if not naming_ok:
                    status["naming_issues"].append(
                        f"File naming may not follow convention: {files[0]}"
                    )
                    status["color"] = "orange"
                else:
                    status["color"] = "green"
            elif len(files) == 0:
                status["color"] = "red"
                status["missing"].append(f"Required file missing")
            else:
                status["naming_issues"].append(f"Expected 1 file, found {len(files)}")
                status["color"] = "orange"

        elif folder_name in ["Final Term", "Mid Term"]:
            ratings = req.get("ratings", [])
            status["total_required"] = len(ratings)
            present_ratings = set()
            naming_issues = []

            for f in files:
                f_lower = f.lower()
                for rating in ratings:
                    if rating.lower() in f_lower:
                        present_ratings.add(rating)

            status["total_present"] = len(present_ratings)

            if len(present_ratings) == 0 and len(files) > 0:
                status["color"] = "red"
                status["missing"].append(
                    "All files missing (only question file counts as missing)"
                )
            elif len(present_ratings) == 0:
                status["color"] = "red"
                status["missing"].append("No files")
            elif len(present_ratings) < len(ratings):
                missing_ratings = set(ratings) - present_ratings
                status["missing"].extend([f"Missing: {r}" for r in missing_ratings])

                pct = len(present_ratings) / len(ratings) * 100
                if pct >= 100:
                    status["color"] = "green"
                elif pct >= 50:
                    status["color"] = "yellow"
                elif pct >= 20:
                    status["color"] = "orange"
                else:
                    status["color"] = "red"
            else:
                status["color"] = "green"

        elif folder_name == "Result":
            subnames = req.get("subnames", [])
            status["total_required"] = len(subnames)
            present_subnames = set()

            for f in files:
                f_lower = f.lower()
                for sn in subnames:
                    if sn.lower().replace("-", "") in f_lower.replace("-", ""):
                        present_subnames.add(sn)

            status["total_present"] = len(present_subnames)

            if len(present_subnames) == 0:
                status["color"] = "red"
                status["missing"].append("All result files missing")
            elif len(present_subnames) < len(subnames):
                missing = set(subnames) - present_subnames
                status["missing"].extend([f"Missing: {m}" for m in missing])
                pct = len(present_subnames) / len(subnames) * 100
                if pct >= 100:
                    status["color"] = "green"
                elif pct >= 50:
                    status["color"] = "yellow"
                elif pct >= 20:
                    status["color"] = "orange"
                else:
                    status["color"] = "red"
            else:
                status["color"] = "green"

    elif any(
        folder_name.lower().startswith(p.lower() + " ")
        and any(
            n in folder_name
            for n in [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
            ]
        )
        for p in ["Task", "Assignment", "Quiz"]
    ):
        prefix = folder_name.split()[0]
        ratings = ["Question", "Solution", "Best", "Average", "Worst"]

        if files:
            file_ratings = set()
            for f in files:
                f_lower = f.lower()
                for r in ratings:
                    if r.lower() in f_lower:
                        file_ratings.add(r)

            status["total_required"] = len(ratings)
            status["total_present"] = len(file_ratings)

            if len(file_ratings) == len(ratings):
                status["color"] = "green"
            elif len(file_ratings) >= 3:
                status["color"] = "yellow"
            elif len(file_ratings) >= 1:
                status["color"] = "orange"
            else:
                status["color"] = "red"
                status["missing"].append("All files missing")

            missing_ratings = set(ratings) - file_ratings
            if missing_ratings:
                status["missing"].extend([f"Missing: {r}" for r in missing_ratings])
        else:
            status["total_required"] = len(ratings)
            status["total_present"] = 0
            status["color"] = "red"
            status["missing"].append(
                f"No files - need 5 files (Question, Solution, Best, Average, Worst)"
            )

    elif folder_name in subfolder_required:
        req = subfolder_required[folder_name]
        prefix = req["prefix"]
        min_subs = req.get("min", 1)
        max_subs = req.get("max", 4)
        required_files = req.get("files", 5)
        ratings = req.get("ratings", [])

        if subdirs > 0:
            complete_folders = 0
            total_sub_files = 0
            all_complete = True
            naming_issues = []

            if not dirs or len(dirs) == 0:
                try:
                    actual_dirs = os.listdir(os.path.dirname(root))
                    dirs = [
                        d
                        for d in actual_dirs
                        if os.path.isdir(os.path.join(os.path.dirname(root), d))
                    ]
                    subdirs = len(dirs)
                except:
                    pass

            for sd in dirs:
                sd_clean = sd.replace(" ", "").replace("-", "").lower()
                has_number = any(
                    n in sd_clean
                    for n in [
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "10",
                        "11",
                        "12",
                        "13",
                        "14",
                        "15",
                        "16",
                    ]
                )

                if not (sd_clean.startswith(prefix.lower()) and has_number):
                    naming_issues.append(f"'{sd}' should be '{prefix} {{number}}'")

                subdir_path = os.path.join(os.path.dirname(root), folder_name, sd)
                try:
                    sub_files = os.listdir(subdir_path)
                except:
                    sub_files = []

                sub_ratings = set()
                for f in sub_files:
                    if os.path.isfile(os.path.join(subdir_path, f)):
                        f_lower = f.lower()
                        for r in ratings:
                            if r.lower() in f_lower:
                                sub_ratings.add(r)

                if len(sub_ratings) == len(ratings):
                    complete_folders += 1

                total_sub_files += len(sub_ratings)

                if len(sub_ratings) < len(ratings):
                    all_complete = False

            status["total_required"] = subdirs * len(ratings)
            status["total_present"] = total_sub_files

            for ni in naming_issues:
                status["naming_issues"].append(ni)

            if subdirs < min_subs:
                status["missing"].append(
                    f"Only {subdirs} subfolder(s), need {min_subs}-{max_subs}"
                )
            elif subdirs > max_subs:
                status["naming_issues"].append(
                    f"Has {subdirs} subfolders, expected max {max_subs}"
                )

            pct = (
                (total_sub_files / (subdirs * len(ratings))) * 100 if subdirs > 0 else 0
            )

            if total_sub_files == 0:
                status["color"] = "red"
                status["missing"].append("All subfolders are empty")
            elif all_complete and subdirs >= min_subs and subdirs <= max_subs:
                status["color"] = "green"
            elif complete_folders == subdirs and subdirs >= min_subs:
                status["color"] = "green"
            elif pct >= 100:
                status["color"] = "green"
            elif pct >= 60:
                status["color"] = "yellow"
            elif pct >= 20:
                status["color"] = "orange"
            else:
                status["color"] = "red"

            status["complete_subfolders"] = complete_folders
            status["total_subfolders"] = subdirs
        else:
            status["color"] = "red"
            status["missing"].append(
                f"Expected {min_subs}-{max_subs} subfolders (e.g., {prefix} 1, {prefix} 2, etc.)"
            )
            status["total_required"] = min_subs * len(ratings)

    elif subdirs > 0:
        status["color"] = "gray"
        status["total_present"] = 0
    else:
        status["color"] = "red"
        status["missing"].append("Folder is empty or unknown type")

    return status


def analyze_course_files(course_path):
    """Analyze files in a course folder with proper validation."""
    is_lab = is_lab_course(course_path)
    folder_type = "Lab" if is_lab else "Course"

    files_info = []
    for root, dirs, files in os.walk(course_path):
        folder_name = os.path.basename(root)

        if root == course_path:
            continue

        has_content = len(files) > 0
        if not has_content and dirs:
            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                for sub_root, sub_dirs, sub_files in os.walk(subdir_path):
                    if sub_files:
                        has_content = True
                        break
                if has_content:
                    break

        if has_content or dirs:
            status = get_folder_status(
                folder_name, files, len(dirs), folder_type, dirs, root
            )
            files_info.append(
                {
                    "folder": folder_name,
                    "files": files,
                    "count": len(files),
                    "subdirs": len(dirs) if dirs else 0,
                    "status": status,
                }
            )
        else:
            status = get_folder_status(folder_name, files, 0, folder_type, [], root)
            files_info.append({"folder": folder_name, "status": status})

    return files_info


def get_completion_status(course_path):
    """Get completion status for a course."""
    missing_folders = []

    for root, dirs, files in os.walk(course_path):
        folder_name = os.path.basename(root)

        # Skip if this is the course root folder
        if root == course_path:
            continue

        # Check if folder has content (files or subdirectories with files)
        has_content = len(files) > 0

        # If no files, check if subdirectories have files
        if not has_content and dirs:
            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                for sub_root, sub_dirs, sub_files in os.walk(subdir_path):
                    if sub_files:
                        has_content = True
                        break
                if has_content:
                    break

        # Only consider it missing if it's truly empty and not in excluded folders
        if (
            not has_content
            and not dirs
            and folder_name not in ["Attendance", "Course Description", "Course Log"]
        ):
            missing_folders.append(folder_name)

    if not missing_folders:
        return "COMPLETED"
    else:
        return f"MISSING: {', '.join(missing_folders)}"


def get_course_short_form(course_name):
    """Convert course name to short form for file naming."""
    # Common course mappings
    course_mappings = {
        "programming fundamentals": "PF",
        "object oriented programming": "OOP",
        "data structures and algorithms": "DSA",
        "database management systems": "DBMS",
        "software engineering": "SE",
        "artificial intelligence": "AI",
        "machine learning": "ML",
        "computer networks": "CN",
        "operating systems": "OS",
        "web development": "WD",
        "mobile app development": "MAD",
        "human computer interaction": "HCI",
        "computer graphics": "CG",
        "digital image processing": "DIP",
        "calculus": "CALC",
        "linear algebra": "LA",
        "discrete mathematics": "DM",
        "statistics": "STAT",
        "physics": "PHY",
        "english": "ENG",
        "islamic studies": "IS",
        "pakistan studies": "PS",
    }

    # Clean the course name
    clean_name = course_name.lower().strip()

    # Remove common suffixes
    clean_name = re.sub(r"\s*\(lab\)$", "", clean_name)
    clean_name = re.sub(r"\s*lab$", "", clean_name)
    clean_name = re.sub(r"\s*\(theory\)$", "", clean_name)
    clean_name = re.sub(r"\s*theory$", "", clean_name)

    # Check for exact matches first
    if clean_name in course_mappings:
        return course_mappings[clean_name]

    # Check for partial matches
    for full_name, short_form in course_mappings.items():
        if full_name in clean_name or clean_name in full_name:
            return short_form

    # If no match found, create abbreviation from words
    words = clean_name.split()
    if len(words) == 1:
        # Single word - take first 3-4 characters
        return words[0][:4].upper()
    elif len(words) <= 3:
        # 2-3 words - take first letter of each
        return "".join(word[0].upper() for word in words if word)
    else:
        # More than 3 words - take first letter of first 3 words
        return "".join(word[0].upper() for word in words[:3] if word)


if __name__ == "__main__":
    app.run(debug=True)
