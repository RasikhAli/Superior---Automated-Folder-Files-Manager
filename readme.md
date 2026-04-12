# Superior - Automated Folder & File Manager

This is a Flask-based web application designed for managing academic folders and files dynamically. It allows users to create structured directories, rename files intelligently, and generate comprehensive teacher reports for organized academic material management.

## 🎨 Color Theme & Design System

### Primary Brand Colors

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| **Primary Purple** | `#6C1C74` | Primary buttons, headers, accent bars, brand elements |
| **Deep Purple** | `#4A1050` | Gradient endpoints, hover states |
| **Hover Purple** | `#521557` | Button hover states |

### Secondary & Accent Colors

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| **Crimson Alert** | `#D72924` | Danger states, critical alerts |
| **Gold Accent** | `#BC9354` | Premium highlights, special indicators |
| **Deep Background** | `#0a040b` | Dark mode base |
| **Surface Dark** | `#120815` | Card backgrounds, modals |
| **Slate Light** | `#cbd5e1` | Light mode text |
| **Slate Dark** | `#334155` | Light mode backgrounds |

### Status Colors

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| **Emerald Success** | `#10b981` | Success states, verified status (Green - 100% complete) |
| **Amber Warning** | `#f59e0b` | Warning states, pending (Yellow - 50-60% complete) |
| **Rose Danger** | `#ef4444` | Error states, duplicates (Red - 0% or missing) |
| **Blue Info** | `#3b82f6` | Informational states |
| **Gold Accent** | `#BC9354` | Partial completion (Orange - 20% complete) |

### UI Theme Variables

**Light Mode:**
- Background: `#f8fafc`
- Surface: `#ffffff`
- Border: `#e2e8f0`

**Dark Mode (Default):**
- `--bg-dark`: `#09090b`
- `--bg-card`: `#18181b`
- `--bg-hover`: `#27272a`
- `--text-main`: `#f4f4f5`
- `--text-muted`: `#a1a1aa`

## Features
- **Create Structured Folders:** Generate organized folders for courses and labs automatically with teacher hierarchy
- **Rename Files Intelligently:** Standardize file names based on predefined naming conventions with automatic backup
- **Teacher Reports:** Generate detailed completion status and file analysis reports with color-coded status
- **User-Friendly Web Interface:** Clean, responsive UI with dark/light theme toggle
- **Automatic Backup:** Creates zip backups before file operations
- **Dynamic Session Management:** Supports multiple academic sessions from 2015 onwards
- **Smart Detection:** Automatically detects Lab vs Course folder types
- **Detailed Validation:** Checks file counts, naming conventions, and completion percentages

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
- **URL:** `/teacher-report`
- **Method:** `POST`
- **Request Payload:**
  ```json
  {
    "base_path": "E:/Superior - Data/Spring-25/To Upload/",
    "report_type": 1,
    "teachers": ["Mr. Rasikh Ali"],
    "sessions": ["Spring 25"]
  }
  ```
- **Response:** Returns detailed report with folder status, color coding, missing files, and naming issues

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
 ├── 📁 Assignment (1-4 subfolders)
 │    ├── 📁 Assignment 1 (5 files required)
 │    ├── 📁 Assignment 2 (5 files required)
 │    ├── 📁 Assignment 3 (5 files required)
 │    └── 📁 Assignment 4 (5 files required)
 ├── 📁 Quiz OR Quizs OR Quizes (1-4 subfolders)
 │    ├── 📁 Quiz 1 (5 files required)
 │    ├── 📁 Quiz 2 (5 files required)
 │    ├── 📁 Quiz 3 (5 files required)
 │    └── 📁 Quiz 4 (5 files required)
 ├── 📁 Attendance (1 file required)
 ├── 📁 Course Description (1 file required)
 ├── 📁 Course Log (1 file required)
 ├── 📁 Course Module OR Course Outline (1 file required)
 ├── 📁 Final Term (5 files required)
 ├── 📁 Mid Term (5 files required)
 └── 📁 Result (3 files required)
```

### **Lab Folder Structure**
```
📂 Lab Name (e.g., Object Oriented Programming Lab)
 ├── 📁 Task (14-16 subfolders)
 │    ├── 📁 Task 1 (5 files required)
 │    ├── 📁 Task 2 (5 files required)
 │    └── ... (up to Task 14-16)
 ├── 📁 Attendance (1 file required)
 ├── 📁 Course Description (1 file required)
 ├── 📁 Course Log (1 file required)
 ├── 📁 Lab Module (1 file required)
 ├── 📁 Final Term (5 files required)
 └── 📁 Result (3 files required)
```

## Teacher Reports - Validation Logic

### **1. Lab vs Course Detection**

The system automatically detects whether a folder is a **Lab** or **Course** by checking the folder names inside the course directory:

```
┌─────────────────────────────────────────────────────────────┐
│  LAB Detection (returns True)                               │
├─────────────────────────────────────────────────────────────┤
│  • Folder named "Task" exists                               │
│  • Folder named "Lab Module" exists                         │
│                                                             │
│  → All folders validated using Lab structure               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  COURSE Detection (returns False)                           │
├─────────────────────────────────────────────────────────────┤
│  • Folder named "Assignment" or "Assignments" exists        │
│  • Folder named "Quiz", "Quizs", or "Quizes" exists         │
│  • Folder named "Mid Term" exists                           │
│                                                             │
│  → All folders validated using Course structure            │
└─────────────────────────────────────────────────────────────┘
```

### **2. Single File Folders (1 file required)**

These folders require exactly **1 file** with proper naming:

| Folder Name | Required Naming Keywords | Lab | Course |
|-------------|-------------------------|-----|--------|
| Course Description | `CourseDescription` | ✓ | ✓ |
| Course Log | `Course-Log` | ✓ | ✓ |
| Course Module | `Course-Module` | - | ✓ |
| Course Outline | `Course-Outline`, `Course-Module` | - | ✓ |
| Lab Module | `Lab-Module` | ✓ | - |
| Attendance | `Attendance` | ✓ | ✓ |

**Status Logic:**
- **0 files:** RED - Missing required file
- **1 file with correct naming:** GREEN - Complete
- **1 file with incorrect naming:** ORANGE - Naming convention not followed
- **More than 1 file:** ORANGE - Expected only 1 file

### **3. Result Folder (3 files required)**

The Result folder requires exactly **3 files** with specific naming:

```
Result/
├── 📄 {session}-{dept}-{section}-{course}-Result-Marksheet.ext
├── 📄 {session}-{dept}-{section}-{course}-Result-Gradesheet.ext
└── 📄 {session}-{dept}-{section}-{course}-Result-CLO-Attainment.ext
```

**Status Logic:**
- **0 files:** RED - All result files missing
- **1-2 files:** Color based on percentage
  - 20%: ORANGE
  - 50-60%: YELLOW
  - 100%: GREEN
- **Missing files displayed:** Shows which specific files are missing (Marksheet/Gradesheet/CLO-Attainment)

### **4. Final Term & Mid Term Folders (5 files required)**

These folders require **all 5 files** for complete status:

```
Final Term/  (or Mid Term/)
├── 📄 {session}-{dept}-{section}-{course}-Final-Term-Paper-Question.ext
├── 📄 {session}-{dept}-{section}-{course}-Final-Term-Paper-Solution.ext
├── 📄 {session}-{dept}-{section}-{course}-Final-Term-Paper-Best.ext
├── 📄 {session}-{dept}-{section}-{course}-Final-Term-Paper-Average.ext
└── 📄 {session}-{dept}-{section}-{course}-Final-Term-Paper-Worst.ext
```

**Important:** Having only "question" file counts as **RED/Missing** because all 5 files are required.

**Status Logic:**
- **0 files:** RED - No files
- **Only Question file present:** RED - Missing Solution, Best, Average, Worst
- **1-4 files:** Color based on percentage:
  - <20%: RED
  - 20%: ORANGE
  - 50-60%: YELLOW
  - 100% (all 5): GREEN
- **Missing ratings displayed:** Shows which specific ratings are missing

### **5. Task/Assignment/Quiz Folders - Container vs Individual Subfolders**

The system distinguishes between **container folders** (Task, Assignment, Quiz) and **individual subfolders** (Task 1, Assignment 1, Quiz 1). Each has different validation rules:

---

#### **A. Individual Subfolders (Task 1, Assignment 1, Quiz 1, etc.)**

Each numbered subfolder inside Task/Assignment/Quiz requires **5 files**:

```
Task 1/                    Assignment 1/              Quiz 1/
├── 📄 ...Question.ext     ├── 📄 ...Question.ext     ├── 📄 ...Question.ext
├── 📄 ...Solution.ext    ├── 📄 ...Solution.ext    ├── 📄 ...Solution.ext
├── 📄 ...Best.ext         ├── 📄 ...Best.ext         ├── 📄 ...Best.ext
├── 📄 ...Average.ext     ├── 📄 ...Average.ext     ├── 📄 ...Average.ext
└── 📄 ...Worst.ext       └── 📄 ...Worst.ext       └── 📄 ...Worst.ext
```

**Naming Pattern:** `Task {number}` (with space), e.g., `Task 1`, `Task 2`, `Task 14`

**Validation:**
- Each subfolder needs all 5 files (Question, Solution, Best, Average, Worst)
- Having only 1 file (e.g., just Question) counts as **RED** - missing 4 files
- 1-2 files: RED
- 3 files: ORANGE (60%)
- 4 files: YELLOW (80%)
- 5 files: GREEN (100%)

**Status Display:**
- Shows: "X/Y complete" (complete subfolders count)
- Lists missing files for incomplete subfolders

---

#### **B. Container Folders (Task, Assignment, Quiz)**

The parent folder that contains numbered subfolders:

| Container | Required Subfolders | Individual Validation |
|-----------|---------------------|----------------------|
| **Task** | 14-16 subfolders (Task 1 to Task 14-16) | Each needs 5 files |
| **Assignment** | 1-4 subfolders (Assignment 1 to Assignment 4) | Each needs 5 files |
| **Quiz** | 1-4 subfolders (Quiz 1 to Quiz 4) | Each needs 5 files |

**Task Container (Lab):**
```
Task/                          ← Container folder
├── 📁 Task 1 (5 files)        ← Individual subfolder
├── 📁 Task 2 (5 files)
├── 📁 Task 3 (5 files)
├── ...
└── 📁 Task 14 (5 files)       ← Can have up to Task 16
```

**Validation:**
- **No subfolders:** RED - Expected subfolders
- **<14 (for Task) or <1 (for A/Q):** RED - Below minimum
- **14-16 (Task) or 1-4 (A/Q):** Check if each subfolder is complete
- **All subfolders have 5 files:** GREEN

**Status Display:**
- Shows: "X/Y complete subfolder(s)"
- Shows: "Only X subfolder(s), need 14-16" if incomplete

---

### **6. Color Coding System**

The Teacher Reports use the following color coding based on **percentage of files present**:

```
┌────────────────────────────────────────────────────────────────────┐
│                        COLOR STATUS CHART                          │
├──────────────┬────────────────────┬─────────────────────────────────┤
│   🟢 GREEN   │ #10b981 (Emerald)  │ 100% completion                │
├──────────────┼────────────────────┼─────────────────────────────────┤
│   🟡 YELLOW  │ #f59e0b (Amber)    │ 50-60% completion              │
├──────────────┼────────────────────┼─────────────────────────────────┤
│   🟠 ORANGE  │ #BC9354 (Gold)     │ 20% completion                 │
├──────────────┼────────────────────┼─────────────────────────────────┤
│   🔴 RED     │ #ef4444 (Rose)     │ 0% completion                  │
├──────────────┼────────────────────┼─────────────────────────────────┤
│   ⬜ GRAY    │ #334155 (Slate)    │ Subfolder containers           │
└──────────────┴────────────────────┴─────────────────────────────────┘
```

**Percentage Calculation:**
```python
percentage = (total_present_files / total_required_files) * 100

# Example for Final Term with 3 files out of 5:
percentage = (3 / 5) * 100 = 60% → YELLOW
```

**For Individual Subfolders (Task 1, Assignment 1, Quiz 1):**
- 5 files (Question, Solution, Best, Average, Worst): GREEN (100%)
- 4 files: YELLOW (80%)
- 3 files: ORANGE (60%)
- 1-2 files: RED (20-40%)
- 0 files: RED (0%)

**For Container Folders (Task, Assignment, Quiz):**
- All subfolders complete with all files: GREEN
- >60% of files present: YELLOW
- 20-60% of files present: ORANGE
- <20% of files present: RED

### **7. Naming Convention Validation**

The system checks if subfolders follow proper naming conventions:

| Folder Type | Expected Pattern | Examples |
|-------------|-----------------|----------|
| Task (Container) | `Task` | `Task` |
| Task (Individual) | `Task {number}` (with space) | `Task 1`, `Task 5`, `Task 14` |
| Assignment (Container) | `Assignment` | `Assignment` |
| Assignment (Individual) | `Assignment {number}` | `Assignment 1`, `Assignment 3` |
| Quiz (Container) | `Quiz`, `Quizs`, `Quizes` | `Quiz` |
| Quiz (Individual) | `Quiz {number}` | `Quiz 1`, `Quiz 4` |

**Important:** The system specifically looks for `Task {number}` with a space (e.g., "Task 1"), not "Task1" or "Task-1" in the individual subfolder detection.

**If naming convention is not followed:**
- A warning is displayed: "⚠ 'FolderName' should be 'Prefix {number}'"

### **8. Report Output Structure**

The teacher report returns detailed JSON with the following structure:

```json
{
  "teacher": "Mr. Rasikh Ali",
  "course_info": "Spring 25/SE/Semester 1/1A/Object Oriented Programming",
  "files": [
    {
      "folder": "Attendance",
      "files": ["S25-SE-1A-OOP-Attendance.xlsx"],
      "count": 1,
      "subdirs": 0,
      "status": {
        "color": "green",
        "percentage": 100,
        "missing": [],
        "naming_issues": [],
        "total_required": 1,
        "total_present": 1
      }
    },
    {
      "folder": "Final Term",
      "files": ["Question.pdf", "Best.pdf"],
      "count": 2,
      "subdirs": 0,
      "status": {
        "color": "orange",
        "percentage": 40,
        "missing": ["Missing: Solution", "Missing: Average", "Missing: Worst"],
        "naming_issues": [],
        "total_required": 5,
        "total_present": 2
      }
    },
    {
      "folder": "Task",
      "files": [],
      "count": 0,
      "subdirs": 10,
      "status": {
        "color": "orange",
        "percentage": 25,
        "missing": ["Some Task folders have incomplete files"],
        "naming_issues": ["Subfolder 'Task5' may not follow naming convention"],
        "total_required": 70,
        "total_present": 35
      }
    }
  ]
}
```

## Naming Conventions

Files follow the structured naming pattern:

```
{session}-{dept}-{section}-{course_short}-{type}{number}-{rating}.{ext}
```

### **Session Format**
- Spring: `S` + last 2 digits of year (e.g., `S25` for Spring 2025)
- Fall: `F` + last 2 digits of year (e.g., `F24` for Fall 2024)

### **Department Codes**
- `AI` - Artificial Intelligence
- `DS` - Data Science
- `SE` - Software Engineering
- `CS` - Computer Science

### **Example Filenames**
- **Assignment:** `S25-SE-1A-OOP-Assignment1-Best.pdf`
- **Quiz:** `F24-CS-2B-DS-Quiz2-Average.docx`
- **Task (Lab):** `S25-AI-1A-ML-Task5-Worst.pptx`
- **Mid Term:** `F24-SE-1A-OOP-Mid-Term-Paper-Best.pdf`
- **Final Term:** `S25-CS-1B-DSA-Final-Term-Paper-Question.pdf`

### **Special File Types**
- **Result Files:** 
  - `S25-SE-1A-OOP-Result-Marksheet.xlsx`
  - `S25-SE-1A-OOP-Result-Gradesheet.xlsx`
  - `S25-SE-1A-OOP-Result-CLO-Attainment.xlsx`
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
- Auto-detection of file ratings (Question, Solution, Best, Average, Worst)

### **Teacher Reports**
- **Detailed File Info (Report Type 1):** Shows file counts, folder status, color coding, missing files, and naming issues
- **Completion Status (Report Type 2):** Overall completion assessment
- Filter by teacher and session
- Export-ready format
- Progress percentage display
- Missing file details
- Naming convention warnings

### **File & Folder Status Display**
The report displays:
- 🔴 **Red (Rose Danger `#ef4444`):** 0-19% files (all missing or only question file present)
- 🟠 **Orange (Gold Accent `#BC9354`):** 20% files (few files present)
- 🟡 **Yellow (Amber Warning `#f59e0b`):** 50-60% files (about half complete)
- 🟢 **Green (Emerald Success `#10b981`):** 100% files (complete)
- ⬜ **Gray (Slate Dark `#334155`):** Container folders with subfolders

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
- Automatically detects Course vs Lab folder types by analyzing folder structure
- Smart rating assignment (Best/Average/Worst/Question/Solution)
- Course short form generation from full course names

### **Dynamic Session Support**
- Generates sessions from 2015 to current year
- Supports both Fall and Spring semesters

### **Comprehensive Validation**
- File count validation per folder
- Naming convention checking
- Subfolder count validation
- Percentage-based color coding
- Missing file reporting
- Naming issue warnings

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