# Superior - Automated Folder & File Manager

This is a Flask-based web application designed for managing academic folders and files dynamically. It allows users to create structured directories, rename files intelligently, and generate comprehensive teacher reports for organized academic material management.

## Features
- **Create Structured Folders:** Generate organized folders for courses and labs automatically with teacher hierarchy
- **Rename Files Intelligently:** Standardize file names based on predefined naming conventions with automatic backup
- **Teacher Reports:** Generate detailed completion status and file analysis reports
- **User-Friendly Web Interface:** Clean, responsive UI with dark/light theme toggle
- **Automatic Backup:** Creates zip backups before file operations
- **Dynamic Session Management:** Supports multiple academic sessions from 2015 onwards

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/RasikhAli/Superior---Automated-Folder-Files-Manager.git
cd Superior---Automated-Folder-Files-Manager
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Application
Open your browser and go to:  
[http://127.0.0.1:5000](http://127.0.0.1:5000)

## API Endpoints

### **1. Create Folders**
- **URL:** `/create-folders`
- **Method:** `POST`
- **Request Payload:**
  ```json
  {
    "base_path": "E:/Superior - Data/Spring-25/To Upload/",
    "type": "Course",
    "session": "Spring 25",
    "dept": "SE",
    "section": "1A",
    "course": "Object Oriented Programming",
    "title": "Mr.",
    "teacher_name": "Rasikh Ali"
  }
  ```
- **Response:**
  - Success: `{ "message": "Course folder structure created at [path]" }`
  - Failure: `{ "error": "Invalid base path provided." }`

### **2. Rename Files**
- **URL:** `/rename-files`
- **Method:** `POST`
- **Request Payload:**
  ```json
  {
    "base_path": "E:/Superior - Data/Spring-25/To Upload/Mr. Rasikh Ali/Spring 25"
  }
  ```
- **Response:**
  ```json
  {
    "renamed_files": [
      {"original": "old_file.pdf", "new": "S25-SE-1A-OOP-Assignment1-Best.pdf"}
    ]
  }
  ```

### **3. Teacher Reports**
- **URL:** `/generate-teacher-report`
- **Method:** `POST`
- **Request Payload:**
  ```json
  {
    "base_path": "E:/Superior - Data/Spring-25/To Upload/",
    "report_type": "1",
    "teacher_filter": "Mr. Rasikh Ali",
    "session_filter": "Spring 25"
  }
  ```

### **4. Get Dynamic Data**
- **Sessions:** `GET /get-sessions`
- **Titles:** `GET /get-titles`
- **Teachers:** `POST /get-teachers`

## Folder & File Structure

### **Complete Hierarchy**
```
📂 Base Path (e.g., E:/Superior - Data/Spring-25/To Upload/)
 └── 📁 Teacher (e.g., Mr. Rasikh Ali)
     └── 📁 Session (e.g., Spring 25)
         └── 📁 Department (SE/CS/AI/DS)
             └── 📁 Semester (Semester 1/2/3/4/5/6/7/8)
                 └── 📁 Section (1A/1B/2A/2B)
                     └── 📁 Course (Object Oriented Programming)
```

### **Course Folder Structure**
```
📂 Course Name (e.g., Object Oriented Programming)
 ├── 📁 Assignment
 │    ├── 📁 Assignment 1
 │    ├── 📁 Assignment 2
 │    ├── 📁 Assignment 3
 │    └── 📁 Assignment 4
 ├── 📁 Quiz
 │    ├── 📁 Quiz 1
 │    ├── 📁 Quiz 2
 │    ├── 📁 Quiz 3
 │    └── 📁 Quiz 4
 ├── 📁 Attendance
 ├── 📁 Course Description
 ├── 📁 Course Log
 ├── 📁 Course Module
 ├── 📁 Final Term
 ├── 📁 Mid Term
 └── 📁 Result
```

### **Lab Folder Structure**
```
📂 Lab Name (e.g., Object Oriented Programming Lab)
 ├── 📁 Task
 │    ├── 📁 Task 1
 │    ├── 📁 Task 2
 │    └── ... (up to Task 14)
 ├── 📁 Attendance
 ├── 📁 Course Description
 ├── 📁 Course Log
 ├── 📁 Lab Module
 ├── 📁 Final Term
 └── 📁 Result
```

## Naming Conventions

Files follow the structured naming pattern:

```
{session}-{dept}-{section}-{course_short}-{type}{number}-{rating}
```

### **Example Filenames**
- `S25-SE-1A-OOP-Assignment1-Best.pdf`
- `F24-CS-2B-DS-Quiz2-Average.docx`
- `S25-AI-1A-ML-Task5-Worst.pptx`
- `F24-SE-1A-OOP-Mid-Term-Paper-Best.pdf`

### **Special File Types**
- **Result Files:** `S25-SE-1A-OOP-Result-Marksheet.xlsx`
- **Course Materials:** `S25-SE-1A-OOP-Course-Module.pdf`
- **Attendance:** `S25-SE-1A-OOP-Attendance.xlsx`

## Web Interface Features

### **Folder Creation**
- Enter base path, course details, session, and teacher information
- Automatic folder hierarchy generation
- Support for both Course and Lab structures

### **File Renaming**
- Batch rename files with automatic backup creation
- Support for session-specific or teacher-wide renaming
- Real-time progress feedback

### **Teacher Reports**
- **Detailed File Info:** Shows file counts and folder status
- **Completion Status:** Overall completion assessment
- Filter by teacher and session
- Export-ready format

### **File & Folder Status**
- 🔴 **Red:** Missing files or empty folders
- 🟢 **Green:** Complete and properly structured
- 🟡 **Yellow:** Incomplete or needs attention

## Technologies Used
- **Flask** – Backend web framework
- **Python** – Core programming language
- **HTML, CSS, Bootstrap** – Responsive web frontend
- **jQuery & AJAX** – Dynamic content loading
- **Font Awesome** – Icons and UI elements

## Key Features

### **Automatic Backup System**
- Creates timestamped zip backups before any file operations
- Stored in parent directory for safety

### **Intelligent File Detection**
- Automatically detects Course vs Lab folder types
- Smart rating assignment (Best/Average/Worst)
- Course short form generation

### **Dynamic Session Support**
- Generates sessions from 2015 to current year
- Supports both Fall and Spring semesters

## Contributing

1. **Fork the repository**
2. **Create a feature branch**  
   ```bash
   git checkout -b feature/my-feature
   ```
3. **Commit your changes**  
   ```bash
   git commit -m "Added new feature"
   ```
4. **Push the branch**  
   ```bash
   git push origin feature/my-feature
   ```
5. **Open a pull request** 🎉

## License
This project is licensed under the MIT License.
