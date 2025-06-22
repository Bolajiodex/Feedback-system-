import sqlite3

# Sample data for 20 feedback submissions
sample_data = [
    ("CU2023001", "Jane Doe", "jane.doe@caleb.edu.ng", "Computer Science", "CSC101", "Feedback", "Academic", "High", "The course content is very engaging!"),
    ("CU2023002", "John Smith", "john.smith@caleb.edu.ng", "Engineering", "ENG201", "Grievance", "Facilities", "Urgent", "The air conditioning is not working."),
    ("CU2023003", "Mary Johnson", "mary.johnson@caleb.edu.ng", "Business Administration", "BUS101", "Suggestion", "Academic", "Medium", "Add more case studies to the curriculum."),
    ("CU2023004", "Ahmed Musa", "ahmed.musa@caleb.edu.ng", "Natural Sciences", "BIO110", "Feedback", "Student Services", "Low", "The library staff are very helpful."),
    ("CU2023005", "Chinwe Okafor", "chinwe.okafor@caleb.edu.ng", "Law", "LAW101", "Complaint", "Administrative", "High", "Delays in processing transcripts."),
    ("CU2023006", "Samuel Adeyemi", "samuel.adeyemi@caleb.edu.ng", "Computer Science", "CSC202", "Appreciation", "Faculty", "Medium", "Thanks for the coding bootcamp."),
    ("CU2023007", "Grace Uche", "grace.uche@caleb.edu.ng", "Social Sciences", "SOC101", "Feedback", "Academic", "Low", "Lectures are well organized."),
    ("CU2023008", "Peter Obi", "peter.obi@caleb.edu.ng", "Engineering", "ENG102", "Suggestion", "Facilities", "Medium", "More power outlets in the labs, please."),
    ("CU2023009", "Aisha Bello", "aisha.bello@caleb.edu.ng", "Medicine", "MED101", "Grievance", "Student Services", "High", "Clinic wait times are too long."),
    ("CU2023010", "David Mark", "david.mark@caleb.edu.ng", "Education", "EDU101", "Feedback", "Academic", "Medium", "Enjoying the new teaching methods."),
    ("CU2023011", "Blessing Eze", "blessing.eze@caleb.edu.ng", "Arts & Humanities", "ART101", "Complaint", "Facilities", "Urgent", "The studio needs better lighting."),
    ("CU2023012", "Musa Ibrahim", "musa.ibrahim@caleb.edu.ng", "Natural Sciences", "CHE101", "Suggestion", "Academic", "Low", "More practical sessions, please."),
    ("CU2023013", "Ifeanyi Nwosu", "ifeanyi.nwosu@caleb.edu.ng", "Law", "LAW201", "Feedback", "Administrative", "Medium", "Registration process was smooth."),
    ("CU2023014", "Fatima Sani", "fatima.sani@caleb.edu.ng", "Business Administration", "BUS202", "Grievance", "Financial", "High", "Scholarship disbursement is delayed."),
    ("CU2023015", "Chinedu Okeke", "chinedu.okeke@caleb.edu.ng", "Computer Science", "CSC303", "Feedback", "Technology", "Medium", "WiFi is much improved this semester."),
    ("CU2023016", "Esther Paul", "esther.paul@caleb.edu.ng", "Social Sciences", "SOC202", "Suggestion", "Student Services", "Low", "More career counseling sessions."),
    ("CU2023017", "Michael James", "michael.james@caleb.edu.ng", "Engineering", "ENG203", "Feedback", "Facilities", "High", "Labs are clean and well-equipped."),
    ("CU2023018", "Ngozi Umeh", "ngozi.umeh@caleb.edu.ng", "Education", "EDU202", "Complaint", "Academic", "Medium", "Some classes are overcrowded."),
    ("CU2023019", "Sola Adebayo", "sola.adebayo@caleb.edu.ng", "Medicine", "MED202", "Grievance", "Administrative", "High", "Exam schedules are not communicated early."),
    ("CU2023020", "Ruth Okon", "ruth.okon@caleb.edu.ng", "Arts & Humanities", "ART202", "Appreciation", "Faculty", "Low", "Lecturers are very supportive."),
]

# Connect to the database
conn = sqlite3.connect('feedback_database.db')
cursor = conn.cursor()

# Insert each sample record
for record in sample_data:
    cursor.execute('''
        INSERT INTO feedback_submissions 
        (student_id, student_name, email, department, course_code, feedback_type, category, priority, feedback_text)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', record)

conn.commit()
conn.close()

print("20 sample feedback records inserted successfully!") 