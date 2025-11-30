# Mermaid Diagrams for Intelligent Study Planner

This file contains all diagrams from the report in Mermaid format. These diagrams can be rendered in:
- GitHub (native support)
- VS Code (with Mermaid extension)
- Online editors: [Mermaid Live Editor](https://mermaid.live/)
- Documentation tools like MkDocs, GitBook, etc.

---

## 1. System Architecture Diagram

This diagram visualizes the system architecture showing frontend, backend, services, and database layers.

```mermaid
graph TB
    subgraph Frontend["Frontend (React + Vite)"]
        Dashboard[Dashboard Page]
        Subjects[Subjects Page]
        Assignments[Assignments Page]
        Exams[Exams Page]
        GeneratePlan[Generate Plan Page]
        ViewPlan[View Plan Page]
        Settings[Settings Page]
        Notifications[Notification System]
        Calendar[Calendar Component]
    end

    subgraph Backend["Backend (FastAPI)"]
        API[API Router]
        SubjectsAPI[Subjects Router]
        AssignmentsAPI[Assignments Router]
        ExamsAPI[Exams Router]
        PlannerAPI[Planner Router]
        NotificationsAPI[Notifications Router]
        MLAPI[ML Router]
    end

    subgraph Services["Services Layer"]
        RulesEngine[Rules Engine]
        ClashDetector[Clash Detector]
        Scheduler[Scheduler]
        MLModel[ML Model Service]
        ReminderService[Reminder Service]
    end

    subgraph Database["SQLite Database"]
        SubjectsDB[(Subjects Table)]
        AssignmentsDB[(Assignments Table)]
        ExamsDB[(Exams Table)]
        StudyPlansDB[(StudyPlans Table)]
        NotificationsDB[(Notifications Table)]
        RemindersDB[(Reminders Table)]
    end

    Dashboard --> API
    Subjects --> API
    Assignments --> API
    Exams --> API
    GeneratePlan --> API
    ViewPlan --> API
    Settings --> API
    Notifications --> API
    Calendar --> API

    API --> SubjectsAPI
    API --> AssignmentsAPI
    API --> ExamsAPI
    API --> PlannerAPI
    API --> NotificationsAPI
    API --> MLAPI

    SubjectsAPI --> SubjectsDB
    AssignmentsAPI --> AssignmentsDB
    ExamsAPI --> ExamsDB
    PlannerAPI --> StudyPlansDB
    NotificationsAPI --> NotificationsDB

    SubjectsAPI --> RulesEngine
    AssignmentsAPI --> ClashDetector
    AssignmentsAPI --> ReminderService
    ExamsAPI --> MLModel
    ExamsAPI --> ClashDetector
    ExamsAPI --> ReminderService
    PlannerAPI --> Scheduler
    PlannerAPI --> ClashDetector
    PlannerAPI --> ReminderService
    Scheduler --> RulesEngine
    Scheduler --> ClashDetector
    MLAPI --> MLModel

    style Frontend fill:#e1f5ff
    style Backend fill:#fff4e1
    style Services fill:#f0ffe1
    style Database fill:#ffe1f5
```

---

## 2. Study Plan Generation Flow Diagram

This flowchart illustrates how study plans are generated with automatic clash detection and rearrangement.

```mermaid
flowchart TD
    Start([Start]) --> Request[User requests plan generation]
    Request --> GetData[Get all assignments and exams]
    GetData --> DetectClashes[Detect clashes]
    
    DetectClashes --> ClashCheck{Clashes detected?}
    
    ClashCheck -->|Yes| Rearrange[Automatically rearrange]
    Rearrange --> AdjustPriorities[Adjust priorities]
    AdjustPriorities --> AddBuffer[Add buffer hours]
    AddBuffer --> SpreadDays[Spread across days]
    
    SpreadDays --> ApplyRules[Apply rule-based logic]
    ClashCheck -->|No| ApplyRules
    
    ApplyRules --> DifficultyRules[Difficulty rules]
    ApplyRules --> DeadlineRules[Deadline rules]
    ApplyRules --> PriorityRules[Priority rules]
    
    DifficultyRules --> CalculateML[Calculate ML predictions]
    DeadlineRules --> CalculateML
    PriorityRules --> CalculateML
    
    CalculateML --> MLNote[For exams: Use past_score,<br/>difficulty, chapters, days_left]
    
    MLNote --> CalculateHours[Calculate total hours needed]
    CalculateHours --> CheckHours{Hours > Available hours?}
    
    CheckHours -->|Yes| Compress[Compress schedule]
    Compress --> ProportionalReduction[Proportional reduction]
    ProportionalReduction --> Sort[Sort by priority and deadline]
    
    CheckHours -->|No| Sort
    
    Sort --> AllocateSlots[Allocate time slots]
    AllocateSlots --> BeforeDue[Assignments before due dates]
    AllocateSlots --> BeforeExam[Exams before exam dates]
    AllocateSlots --> DistributeEvenly[Distribute evenly]
    
    BeforeDue --> GenerateReminders[Generate automatic reminders]
    BeforeExam --> GenerateReminders
    DistributeEvenly --> GenerateReminders
    
    GenerateReminders --> ReminderNote[Assignments due in 3 days<br/>Exams in 7 days<br/>Urgent: Exams in 3 days]
    
    ReminderNote --> SaveDB[Save study plan to database]
    SaveDB --> Return[Return plan to user]
    Return --> End([End])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style Rearrange fill:#FFE4B5
    style DetectClashes fill:#E0E0E0
    style CalculateML fill:#B0E0E6
    style GenerateReminders fill:#FFE4B5
```

---

## 3. Database Schema Diagram (ER Diagram)

This ER diagram shows the database structure and relationships between all tables.

```mermaid
erDiagram
    Subjects {
        INTEGER id PK
        VARCHAR name
        VARCHAR difficulty
        FLOAT recommended_hours
        TEXT past_assignments
        TEXT questionnaire_results
        DATETIME created_at
    }
    
    Assignments {
        INTEGER id PK
        VARCHAR name
        VARCHAR subject_name FK
        VARCHAR due_date
        FLOAT estimated_hours
        VARCHAR difficulty
        VARCHAR priority
        VARCHAR status
        DATETIME created_at
    }
    
    Exams {
        INTEGER id PK
        VARCHAR name
        VARCHAR subject_name FK
        VARCHAR exam_date
        VARCHAR difficulty
        FLOAT past_score
        INTEGER chapters
        FLOAT recommended_hours
        VARCHAR priority
        DATETIME created_at
    }
    
    StudyPlans {
        INTEGER id PK
        INTEGER item_id
        VARCHAR item_type
        VARCHAR item_name
        VARCHAR day
        VARCHAR date
        VARCHAR time_slot
        FLOAT hours
        VARCHAR category
        DATETIME created_at
    }
    
    Notifications {
        INTEGER id PK
        VARCHAR type
        VARCHAR title
        TEXT message
        VARCHAR item_type
        VARCHAR item_ids
        BOOLEAN is_read
        DATETIME created_at
    }
    
    Reminders {
        INTEGER id PK
        INTEGER subject_id FK
        TEXT message
        VARCHAR reminder_date
        BOOLEAN is_read
        DATETIME created_at
    }
    
    Subjects ||--o{ Assignments : "subject_name"
    Subjects ||--o{ Exams : "subject_name"
    Assignments ||--o{ StudyPlans : "item_id"
    Exams ||--o{ StudyPlans : "item_id"
    Subjects ||--o{ Reminders : "subject_id"
```

**Notes:**
- Assignments and Exams are linked to Subjects via `subject_name` (not FK constraint)
- Exams use ML-predicted `recommended_hours`
- StudyPlans `item_type` and `category` are either "assignment" or "exam"

---

## 4. Clash Detection and Rearrangement Flow

This flowchart details the clash detection and automatic rearrangement process.

```mermaid
flowchart TD
    Start([Start]) --> Receive[Receive assignments and exams]
    
    Receive --> ClashDetection["Clash Detection"]
    
    subgraph ClashDetection["Clash Detection"]
        CheckExamOverlaps[Check Exam-Exam overlaps]
        CheckExamOverlaps --> ExamSameDate{Same exam date?}
        
        ExamSameDate -->|Yes| MarkExamClash[Mark as clash]
        MarkExamClash --> IncreasePriority[Increase priority to 'high']
        IncreasePriority --> AddBuffer20[Add 20% buffer hours]
        AddBuffer20 --> SpreadPrep[Spread preparation across days]
        SpreadPrep --> ExamRearrangement[Automatic rearrangement]
        
        ExamSameDate -->|No| CheckAssignOverlaps
        ExamRearrangement --> CheckAssignOverlaps[Check Assignment-Assignment overlaps]
        
        CheckAssignOverlaps --> AssignSameDay{Same/within 1 day due date?}
        
        AssignSameDay -->|Yes| MarkAssignClash[Mark as clash]
        MarkAssignClash --> SortBySize[Sort by size largest first]
        SortBySize --> PrioritizeLargest[Prioritize largest urgent]
        PrioritizeLargest --> SetOthersHigh[Set others to high priority]
        SetOthersHigh --> AssignRearrangement[Automatic rearrangement]
        
        AssignSameDay -->|No| CheckAssignExam
        AssignRearrangement --> CheckAssignExam[Check Assignment-Exam conflicts]
        
        CheckAssignExam --> SameWithinDay{Same/within 1 day date?}
        
        SameWithinDay -->|Yes| MarkConflict[Mark as conflict]
        MarkConflict --> SetAssignUrgent[Set assignment to urgent]
        SetAssignUrgent --> SetExamHigh[Set exam to high priority]
        SetExamHigh --> StartEarlier[Start exam prep earlier]
        StartEarlier --> ConflictRearrangement[Automatic rearrangement]
        
        SameWithinDay -->|No| NotificationGen
        ConflictRearrangement --> NotificationGen
    end
    
    ClashDetection --> NotificationGen["Notification Generation"]
    
    subgraph NotificationGen["Notification Generation"]
        CreateNotifications[Create clash notifications]
        CreateNotifications --> StoreDB[Store in database]
    end
    
    NotificationGen --> RearrangementResults["Rearrangement Results"]
    
    subgraph RearrangementResults["Rearrangement Results"]
        ReturnAdjusted[Return adjusted items]
        ReturnAdjusted --> ReturnMessages[Return clash messages]
    end
    
    RearrangementResults --> Continue[Continue to scheduling]
    Continue --> End([End])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style ExamRearrangement fill:#FFE4B5
    style AssignRearrangement fill:#FFE4B5
    style ConflictRearrangement fill:#FFE4B5
    style ClashDetection fill:#E0E0E0
```

---

## 5. ML Model Prediction Flow

This diagram shows how the ML model predicts study hours based on exam features.

```mermaid
flowchart LR
    subgraph MLService["ML Model Service"]
        TrainModel[Load/Train Model]
        Model[Linear Regression]
        Predict[Predict Hours]
    end
    
    subgraph TrainingData["Training Data"]
        CSVFile[(CSV File)]
    end
    
    UserCreatesExam[User Creates Exam] -->|Input: past_score,<br/>difficulty, chapters,<br/>days_left| Predict
    
    Predict --> Model
    
    Model -->|Load training data| CSVFile
    CSVFile -->|Features: past_score,<br/>difficulty_level,<br/>chapters, days_left| Model
    
    Model -->|Model exists?| CheckModel{Model exists?}
    CheckModel -->|No| TrainModel
    TrainModel -->|Train Linear Regression| Model
    CheckModel -->|Yes| Predict
    
    Model -->|Predicted hours<br/>minimum 1 hour| Predict
    Predict -->|Use predicted hours<br/>for scheduling| StudyPlanGen[Study Plan Generation]
    
    style MLService fill:#E1F5FF
    style TrainingData fill:#FFE1F5
    style Model fill:#B0E0E6
    style Predict fill:#FFE4B5
```

**ML Model Details:**
- **Features:**
  - `past_score` (0-100)
  - `difficulty_level` (0,1,2)
  - `chapters` (integer)
  - `days_left` (integer)
- **Output:**
  - `recommended_hours` (float, minimum 1 hour)

---

## How to Use These Mermaid Diagrams

### GitHub
Simply paste the code blocks into any `.md` file in your GitHub repository. GitHub will automatically render them.

### VS Code
1. Install the "Markdown Preview Mermaid Support" extension
2. Open the markdown file
3. Use the preview feature to see rendered diagrams

### Online Editors
1. Go to [Mermaid Live Editor](https://mermaid.live/)
2. Copy any diagram code
3. Paste into the editor
4. Export as PNG, SVG, or copy the link

### Documentation Tools
- **MkDocs**: Use `mkdocs-mermaid2-plugin`
- **GitBook**: Native support
- **Docusaurus**: Use `@docusaurus/theme-mermaid`
- **Notion**: Copy rendered images
- **Confluence**: Use Mermaid macro

---

## Diagram Summary

1. **System Architecture Diagram**: Shows the complete system architecture with frontend, backend, services, and database layers
2. **Study Plan Generation Flow**: Illustrates the step-by-step process of generating study plans with clash detection and ML predictions
3. **Database Schema (ER Diagram)**: Displays all database tables and their relationships
4. **Clash Detection Flow**: Details the automatic clash detection and rearrangement algorithm
5. **ML Model Prediction Flow**: Shows how the machine learning model predicts study hours

All diagrams have been converted from PlantUML to Mermaid format for better compatibility with modern documentation platforms and tools.

