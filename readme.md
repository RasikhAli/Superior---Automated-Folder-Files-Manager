# Superior - Automated Folder & File Manager

This is a Flask-based web application designed for managing academic folders and files dynamically. It allows users to create structured directories, rename files, and analyze folder contents to ensure organized academic material management.

## Features
- **Create Structured Folders:** Generate organized folders for courses and labs automatically.
- **Rename Files Intelligently:** Standardize file names based on predefined naming conventions.
- **Analyze Folder Contents:** Identify missing or misplaced files and highlight status.
- **User-Friendly Web Interface:** Interact easily through a clean and responsive UI.

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
    "base_path": "D:/Fall 24/SE/1A/PF",
    "type": "Course",
    "session": "Fall 24",
    "dept": "SE",
    "section": "1A",
    "course": "Object Oriented Programming (Lab)"
  }
  ```
- **Response:**
  - Success: `{ "message": "Folders created successfully." }`
  - Failure: `{ "error": "Invalid base path provided." }`

### **2. Rename Files**
- **URL:** `/rename-files`
- **Method:** `POST`
- **Request Payload:**
  ```json
  {
    "base_path": "D:/Fall 24/SE/1A/PF",
    "session": "Fall 24"
  }
  ```
- **Response:**
  ```json
  {
    "renamed_files": ["file1.pdf", "file2.docx"]
  }
  ```

### **3. List Folder Contents**
- **URL:** `/list-folders`
- **Method:** `POST`
- **Request Payload:**
  ```json
  {
    "base_path": "D:/Fall 24/SE/1A/PF"
  }
  ```
- **Response:** Returns folder structure and file details.

## Folder & File Structure

### **Course Folder Structure**
```
📂 Course Name (e.g., Object Oriented Programming)
 ├── 📁 Assignments
 │    ├── 📁 Assignment 1
 │    ├── 📁 Assignment 2
 ├── 📁 Quizzes
 │    ├── 📁 Quiz 1
 │    ├── 📁 Quiz 2
 ├── 📁 Attendance
 ├── 📁 Final Term
 ├── 📁 Mid Term
```

### **Lab Folder Structure**
```
📂 Lab Name (e.g., Object Oriented Programming Lab)
 ├── 📁 Tasks
 │    ├── 📁 Task 1
 │    ├── 📁 Task 2
 ├── 📁 Lab Modules
 ├── 📁 Final Term
```

## Naming Conventions

Files follow the structured naming pattern:

```
{session}-{dept}-{section}-{course}-{type}{number}-{rating}
```

### **Example Filenames**
- `Fall24-SE-1A-PF-Assignment1-Best.pdf`
- `Fall24-SE-1A-PF-Quiz2-Average.docx`
- `Fall24-SE-1A-PF-MidTerm-Worst.pptx`

## Web Interface

### **Folder Creation**
- Enter base path, course details, and session.
- Click "Create Folders" to generate the structured directory.

### **File Renaming**
- Enter the base folder path and session.
- Click "Rename Files" to standardize filenames.

### **File & Folder Status**
- The app highlights missing or misplaced files:
  - 🔴 **Red:** Missing files.
  - 🟢 **Green:** Properly structured folders.
  - 🟡 **Yellow:** Incomplete or unoptimized folders.

## Technologies Used
- **Flask** – Backend web framework.
- **Python** – Core programming language.
- **HTML, CSS, jQuery** – Web frontend.
- **AJAX** – Asynchronous request handling.

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