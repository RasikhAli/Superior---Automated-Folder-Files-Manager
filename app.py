from flask import Flask, render_template, request, jsonify
import random
import os
import re
import shutil

app = Flask(__name__)

# Keywords for detecting file ratings
rating_keywords = {
    'best': 'Best',
    'be': 'Best',
    'avg': 'Average',
    'av': 'Average',
    'wo': 'Worst',
    'wor': 'Worst',
    'worst': 'Worst',
    'sol': 'Solution',
    'solution': 'Solution',
    'ques': 'Question',
    'question': 'Question'
}

# Default folder structure for Course
course_structure = {
    'Assignment': ['Assignment 1', 'Assignment 2', 'Assignment 3', 'Assignment 4'],
    'Quiz': ['Quiz 1', 'Quiz 2', 'Quiz 3', 'Quiz 4'],
    'Attendance': [],
    'Course Description': [],
    'Course Log': [],
    'Course Module': [],
    'Final Term': [],
    'Mid Term': [],
    'Result': []
}

# Default folder structure for Lab
lab_structure = {
    'Task': ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5', 'Task 6', 'Task 7', 'Task 8', 'Task 9', 'Task 10', 'Task 11', 'Task 12', 'Task 13', 'Task 14'],
    # 'Attendance': [],
    'Course Description': [],
    'Course Log': [],
    'Lab Module': [],
    'Final Term': [],
    'Result': []
}

# Format mapping for file naming
format_mapping = {
    'Course': {
        'Assignment': '{session}-{dept}-{section}-{course}-Assignment{number}-{rating}',
        'Quiz': '{session}-{dept}-{section}-{course}-Quiz{number}-{rating}',
        'Attendance': '{session}-{dept}-{section}-{course}-Attendance',
        'Course Description': '{session}-{dept}-{section}-{course}-CourseDescription-Form',
        'Course Log': '{session}-{dept}-{section}-{course}-Course-Log',
        'Course Module': '{session}-{dept}-{section}-{course}-Course-Module',
        'Mid Term': '{session}-{dept}-{section}-{course}-Mid-Term-Paper-{rating}',
        'Final Term': '{session}-{dept}-{section}-{course}-Final-Term-Paper-{rating}',
        'Result': '{session}-{dept}-{section}-{course}-Result'
    },
    'Lab': {
        'Task': '{session}-{dept}-{section}-{course}-Task{number}-{rating}',
        # 'Attendance': '{session}-{dept}-{section}-{course}-Attendance',
        'Course Description': '{session}-{dept}-{section}-{course}-CourseDescription-Form',
        'Course Log': '{session}-{dept}-{section}-{course}-Course-Log',
        'Lab Module': '{session}-{dept}-{section}-{course}-Lab-Module',
        'Final Term': '{session}-{dept}-{section}-{course}-Final-Term-Paper-{rating}',
        'Result': '{session}-{dept}-{section}-{course}-Result'
    }
}

def create_folders(base_path, folder_structure):
    """Create folders based on the provided structure."""
    for folder, subfolders in folder_structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        for subfolder in subfolders:
            os.makedirs(os.path.join(folder_path, subfolder), exist_ok=True)

@app.route('/create-folders', methods=['POST'])
def create_folders_route():
    """Endpoint to create folders dynamically."""
    data = request.json
    base_path = data.get('base_path')
    session_folder = data.get('session')
    dept_folder = data.get('dept')
    section_folder = data.get('section')
    course_folder = data.get('course')
    folder_type = data.get('type')  # "Course" or "Lab"

    if not base_path or not os.path.isdir(base_path):
        return jsonify({'error': 'Invalid base path provided'}), 400

    folder_structure = course_structure if folder_type == 'Course' else lab_structure
    final_path = base_path+'\\'+session_folder+'\\'+dept_folder+'\\'+'Semester '+section_folder[0]+'\\'+section_folder+'\\'+course_folder
    create_folders(final_path, folder_structure)

    return jsonify({'message': f"{folder_type} folder structure created at {base_path}"}), 200

@app.route('/rename-files', methods=['POST'])
def rename_files_route():
    """Endpoint to rename files based on the naming convention."""
    data = request.json
    base_path = data.get('base_path')

    if not base_path or not os.path.isdir(base_path):
        return jsonify({'error': 'Invalid base path provided'}), 400

    # Extract session (e.g., "Fall 24" → "F24")
    session_match = re.search(r'(Fall|Spring) (\d{2})', base_path, re.IGNORECASE)
    if session_match:
        session = session_match.group(1)[0].upper() + session_match.group(2)
    else:
        return jsonify({'error': 'Session folder not found in base path'}), 400

    renamed_files = []

    # Walk through department folders
    for dept_folder in os.listdir(base_path):
        dept_path = os.path.join(base_path, dept_folder)
        if os.path.isdir(dept_path) and dept_folder in ['AI', 'DS', 'SE', 'CS']:
            # Walk through semester folders
            for semester_folder in os.listdir(dept_path):
                semester_path = os.path.join(dept_path, semester_folder)
                if os.path.isdir(semester_path) and semester_folder.lower().startswith("semester"):
                    # Walk through section folders
                    for section_folder in os.listdir(semester_path):
                        section_path = os.path.join(semester_path, section_folder)
                        if os.path.isdir(section_path):
                            # Walk through course folders
                            for course_folder in os.listdir(section_path):
                                course_path = os.path.join(section_path, course_folder)
                                if os.path.isdir(course_path):
                                    # Define a list of stop words to skip
                                    stop_words = {"for", "and", "the", "of", "in", "on", "at", "by", "to", "with", "a", "an"}

                                    # Remove text after '(' and trim the course folder
                                    course_folder_cleaned = re.split(r'\s*\(', course_folder)[0]

                                    # Extract short form of course
                                    course_short = ''.join(
                                        word[0].upper() for word in re.findall(r'\b\w+\b', course_folder_cleaned) if word.lower() not in stop_words
                                    )

                                    # Debugging: Print the short form for verification
                                    print(f"Course Folder: {course_folder}, Short Form: {course_short}")

                                    # Detect if it's a Lab or Course
                                    folder_type = detect_folder_type(course_path)

                                    # Rename files using the new short form
                                    renamed_files.extend(rename_files(
                                        course_path,
                                        session,
                                        dept_folder,
                                        semester_folder,
                                        section_folder,
                                        course_short,
                                        folder_type
                                    ))


    return jsonify({'renamed_files': renamed_files}), 200

def detect_folder_type(course_path):
    """Determine if a folder represents a Lab or a Course."""
    for root, dirs, files in os.walk(course_path):
        # Look for Lab-specific folders
        if any(folder in dirs for folder in ['Task', 'Lab Module']):
            return 'Lab'
        
        # Look for typical Course-specific folders
        if any(folder in dirs for folder in ['Assignment', 'Quiz', 'Final Term', 'Mid Term']):
            return 'Course'
    return 'Course'  # Default to Course if unclear

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

        if file_type.startswith('Task') or file_type.startswith('Assignment') or file_type.startswith('Quiz') or file_type.startswith('Final') or file_type.startswith('Mid'):
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
                    new_question_name = f"{session}-{dept}-{section}-{course}-{cleaned_file_type}-{matched_type}.txt"
                    new_question_path = os.path.join(root, new_question_name)
                    
                    try:
                        os.rename(question_file, new_question_path)
                        renamed_files.append({'original': question_file, 'new': new_question_path})
                        print(f"Renamed file: {new_question_path}")
                    except Exception as e:
                        print(f"Error renaming file: {e}")
                else:
                    print(f"Skipped (no match): {file}")


            # If no solution file exists, create one from the "best" file
            if not solution_file:
                print("Solution file is missing, attempting to create one.")
                best_file_path = None

                # Search for the "best" file dynamically using rating_keywords
                for file in files:
                    file_lower = file.lower()
                    
                    # Check if the file matches the "best" category
                    if any(keyword in file_lower for keyword in ['best', 'be']):  # Keywords for "best" in rating_keywords
                        best_file_path = os.path.join(root, file)
                        break  # Stop once a "best" file is found

                if best_file_path:
                    new_solution_path = os.path.join(
                        root,
                        f"{session}-{dept}-{section}-{course}-{cleaned_file_type}-Solution{os.path.splitext(best_file_path)[-1]}"
                    )
                    try:
                        shutil.copy(best_file_path, new_solution_path)
                        renamed_files.append({'original': best_file_path, 'new': new_solution_path})
                        print(f"Created solution file: {new_solution_path}")
                    except Exception as e:
                        print(f"Error copying file to create solution: {e}")
                else:
                    print("No 'best' file found to create a solution file.")
        
        # Handle Lab Module or Course Module
        if file_type in ['Lab Module', 'Course Module']:
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
                        session=session,
                        dept=dept,
                        section=section,
                        course=course
                    )
                    
                    # Create file paths
                    new_file_path = os.path.join(root, new_name + os.path.splitext(file)[-1])
                    old_file_path = os.path.join(root, file)
                    
                    # Rename the file
                    os.rename(old_file_path, new_file_path)
                    renamed_files.append({'original': old_file_path, 'new': new_file_path})
                
                except KeyError as e:
                    print(f"Error: Format for '{folder_type} - {file_type}' not found in mapping.")
                except Exception as e:
                    print(f"Error renaming file '{file}': {e}")


        # Handle specific cases for Result sub-files
        elif file_type == 'Result':
            for file in files:
                file_lower = file.lower()
                # Skip already renamed files
                if file.startswith(session):
                    continue
                if 'marksheet' in file_lower or 'mark' in file_lower or 'ms' in file_lower:
                    new_name = f"{session}-{dept}-{section}-{course}-Result-Marksheet{os.path.splitext(file)[-1]}"
                elif 'gradesheet' in file_lower or 'grade' in file_lower or 'gs' in file_lower:
                    new_name = f"{session}-{dept}-{section}-{course}-Result-Gradesheet{os.path.splitext(file)[-1]}"
                elif 'clo attainment' in file_lower or 'clo' in file_lower:
                    new_name = f"{session}-{dept}-{section}-{course}-Result-CLO-Attainment{os.path.splitext(file)[-1]}"
                else:
                    continue  # Skip unrelated files

                # Rename the file
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_name)
                try:
                    os.rename(old_path, new_path)
                    renamed_files.append({'original': old_path, 'new': new_path})
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
                    session=session,
                    dept=dept,
                    section=section,
                    course=course
                )
                new_path = os.path.join(root, new_name + os.path.splitext(file)[-1])
                old_path = os.path.join(root, file)

                try:
                    os.rename(old_path, new_path)
                    renamed_files.append({'original': old_path, 'new': new_path})
                except Exception as e:
                    print(f"Error renaming file '{file}': {e}")




        # Ensure the function only applies to Tasks, Assignments, and Quizzes
        if folder_type == 'Lab' and file_type.startswith('Task'):
            number_match = re.search(r"Task\\s*(\\d+)", file_type, re.IGNORECASE)
            if number_match:
                number = number_match.group(1)
                format_string = format_mapping[folder_type]['Task']
            else:
                continue
        elif folder_type == 'Course' and file_type.startswith(('Assignment', 'Quiz')):
            number_match = re.search(r"(Assignment|Quiz)\\s*(\\d+)", file_type, re.IGNORECASE)
            if number_match:
                number = number_match.group(2)
                format_string = format_mapping[folder_type][number_match.group(1)]
            else:
                continue
        else:
            continue

        # Gather existing ratings in the folder
        existing_ratings = set()
        for file in files:
            _, rating = extract_task_details(file)
            if rating != 'Unknown':
                existing_ratings.add(rating)

        for file in files:
            # Skip already renamed files
            if file.startswith(session):
                continue

            file_path = os.path.join(root, file)
            _, rating = extract_task_details(file)

            # Assign random rating if 'Unknown' and ensure it's unique
            if rating == 'Unknown':
                possible_ratings = {'Best', 'Average', 'Worst'} - existing_ratings
                if possible_ratings:
                    rating = random.choice(list(possible_ratings))
                    existing_ratings.add(rating)
                else:
                    rating = random.choice(['Best', 'Average', 'Worst'])

            try:
                new_name = format_string.format(
                    session=session,
                    dept=dept,
                    section=section,
                    course=course,
                    number=number,
                    rating=rating
                )
                new_file_path = os.path.join(root, new_name + os.path.splitext(file)[-1])

                os.rename(file_path, new_file_path)
                renamed_files.append({'original': file_path, 'new': new_file_path})
            except Exception as e:
                print(f"Error renaming file '{file}': {e}")

        

    return renamed_files








def extract_task_details(filename):
    print(f"Extracting details from: {filename}")
    
    # Extract task number (if any). Default to 'Unknown' if no digits found.
    task_number = ''.join(filter(str.isdigit, filename)) or 'Unknown'
    
    # If no task number, we might want to assign a default task number, e.g., '1' for simplicity
    if task_number == 'Unknown':
        task_number = '1'  # Assign a default task number if none is found
    
    # Extract rating (if any). Check against the defined keywords
    rating = 'Unknown'
    for keyword, mapped_rating in rating_keywords.items():
        if keyword in filename.lower():
            rating = mapped_rating
            print(f"Matched rating '{rating}' for keyword '{keyword}' in file '{filename}'")
    
    if task_number == 'Unknown':
        print(f"No task number found in '{filename}'")
    return task_number, rating


@app.route('/list-folders', methods=['POST'])
def list_folders():
    data = request.json
    base_path = data.get('base_path')

    if not base_path or not os.path.isdir(base_path):
        return jsonify({'error': 'Invalid base path provided'}), 400

    folder_structure = {}
    for root, dirs, files in os.walk(base_path):
        relative_path = os.path.relpath(root, base_path)
        task_status = {}
        if 'Task' in root:  # Check for tasks
            for file in files:
                _, rating = extract_task_details(file)
                if rating != 'Unknown':
                    task_status[rating] = True
            # Compute missing ratings
            missing_ratings = {'Best', 'Average', 'Worst'} - set(task_status.keys())
            task_status['missing'] = list(missing_ratings)
        folder_structure[relative_path] = {
            'folders': dirs,
            'files': files,
            'task_status': task_status if task_status else None
        }

    return jsonify({'folder_structure': folder_structure}), 200




@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
