import streamlit as st
import pandas as pd
import sqlite3
import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Caleb University Feedback System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #2c5aa0;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
    
    .welcome-text {
        font-size: 1.2rem;
        color: #333;
        line-height: 1.6;
        text-align: center;
        margin: 2rem 0;
    }
    
    .info-box, .feature-card, .success-box, .admin-section, .footer {
        color: #1a1a1a !important;
        background: #e9ecef !important;
    }
    
    .info-box *, .feature-card *, .success-box *, .admin-section *, .footer * {
        color: #1a1a1a !important;
    }
    
    .main-header, .sub-header {
        color: #1f4e79;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .admin-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .footer {
        text-align: center;
        color: #666;
        margin-top: 3rem;
        padding: 2rem;
        border-top: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
def init_database():
    conn = sqlite3.connect('feedback_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            course_code TEXT,
            feedback_type TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            feedback_text TEXT NOT NULL,
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Pending',
            admin_response TEXT,
            response_date TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO admin_users (username, password_hash, role)
        VALUES ('admin', 'admin123', 'super_admin')
    ''')
    
    conn.commit()
    conn.close()

init_database()

# Session state
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if st.session_state.get('show_success'):
    st.markdown("""
    <div class="success-box" style="background-color: #e8f5e9; border-left: 6px solid #4CAF50; color: #155724; font-size: 1.15rem;">
        <strong>✅ Feedback Submitted Successfully!</strong><br>
        Your feedback has been recorded and will be reviewed by the appropriate department. 
        You will receive a confirmation email shortly.
    </div>
    """, unsafe_allow_html=True)
    st.session_state['show_success'] = False
if st.session_state.get('show_admin_success'):
    st.markdown("""
    <div class="success-box" style="background-color: #e3f2fd; border-left: 6px solid #1976d2; color: #0d2a4d; font-size: 1.1rem;">
        <strong>✅ Submission updated successfully!</strong><br>
        The feedback status and response have been updated.
    </div>
    """, unsafe_allow_html=True)
    st.session_state['show_admin_success'] = False

# Sidebar
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <h2 style='color: white; margin-bottom: 0.5rem;'>🎓 Caleb University</h2>
    <p style='color: #e0e0e0; font-size: 0.9rem; margin: 0;'>Feedback & Grievance System</p>
</div>
""", unsafe_allow_html=True)

# Replace this:
# page = st.sidebar.selectbox(
#     "Select Page",
#     ["🏠 Welcome", "📝 Submit Feedback", "⚙️ Admin Panel", "❓ Help & Support"]
# )

# With radio buttons for navigation:
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Welcome", "📝 Submit Feedback", "⚙️ Admin Panel", "❓ Help & Support"],
    index=0,
    key="main_nav_radio"
)

# Main content
if page == "🏠 Welcome":
    st.markdown('<h1 class="main-header">🎓 Caleb University</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header" style="text-align: center;">Feedback & Grievance Redressal System</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="welcome-text">
        Welcome to Caleb University's comprehensive feedback and grievance redressal system. 
        This platform is designed to provide students with a seamless way to submit feedback, 
        report grievances, and contribute to the continuous improvement of our academic community.
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #1f4e79; margin-bottom: 1rem;">📝 Easy Submission</h3>
            <p>Submit feedback and grievances through our user-friendly interface with comprehensive form validation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #1f4e79; margin-bottom: 1rem;">🔒 Confidential & Secure</h3>
            <p>All submissions are treated with strict confidentiality and stored securely in our database.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #1f4e79; margin-bottom: 1rem;">📊 Real-time Analytics</h3>
            <p>Access comprehensive analytics and insights to understand feedback patterns and trends.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick stats
    try:
        conn = sqlite3.connect('feedback_database.db')
        df = pd.read_sql_query("SELECT * FROM feedback_submissions", conn)
        conn.close()
        
        if not df.empty:
            st.markdown('<h3 class="sub-header" style="text-align: center; margin-top: 3rem;">📈 System Statistics</h3>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(df)}</div>
                    <div class="metric-label">Total Submissions</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                pending_count = len(df[df['status'] == 'Pending'])
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{pending_count}</div>
                    <div class="metric-label">Pending Review</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                high_priority = len(df[df['priority'].isin(['High', 'Urgent'])])
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{high_priority}</div>
                    <div class="metric-label">High Priority</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                dept_count = df['department'].nunique()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{dept_count}</div>
                    <div class="metric-label">Departments</div>
                </div>
                """, unsafe_allow_html=True)
    except:
        pass

elif page == "📝 Submit Feedback":
    st.markdown('<h1 class="main-header">📝 Submit Feedback</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        background: #f5f7fa;
        border-left: 6px solid #1f4e79;
        padding: 1.2rem 1.5rem;
        border-radius: 0.7rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        color: #1a1a1a;
    ">
        <span style="font-size:1.2rem;font-weight:bold;color:#1f4e79;">📋 Important Information:</span>
        <ul style="margin-top:0.7rem;">
            <li>All submissions are confidential and will be reviewed by the appropriate department.</li>
            <li>Please provide accurate and constructive feedback.</li>
            <li>For urgent matters, contact your department head directly.</li>
            <li>You will receive a confirmation email once your submission is processed.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="sub-header">📝 Submit Your Feedback or Grievance</h2>', unsafe_allow_html=True)
        
        with st.form("feedback_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                student_id = st.text_input("Student ID *", placeholder="e.g., CU2023001")
                student_name = st.text_input("Full Name *", placeholder="Enter your full name")
                email = st.text_input("Email Address *", placeholder="your.email@caleb.edu.ng")
                department = st.selectbox(
                    "Department *",
                    ["Select Department", "Computer Science", "Engineering", "Business Administration", 
                     "Arts & Humanities", "Natural Sciences", "Social Sciences", "Education", "Law", "Medicine"]
                )
            
            with col2:
                course_code = st.text_input("Course Code (Optional)", placeholder="e.g., CSC101")
                feedback_type = st.selectbox(
                    "Type of Submission *",
                    ["Select Type", "Feedback", "Grievance", "Suggestion", "Complaint", "Appreciation"]
                )
                category = st.selectbox(
                    "Category *",
                    ["Select Category", "Academic", "Administrative", "Facilities", "Student Services", 
                     "Faculty", "Financial", "Technology", "Other"]
                )
                priority = st.selectbox(
                    "Priority Level *",
                    ["Select Priority", "Low", "Medium", "High", "Urgent"]
                )
            
            feedback_text = st.text_area(
                "Detailed Feedback/Grievance *",
                placeholder="Please provide a detailed description of your feedback or grievance. Be specific and constructive.",
                height=150
            )
            
            submitted = st.form_submit_button("Submit Feedback", type="primary")
            
            if submitted:
                if (student_id and student_name and email and department != "Select Department" and 
                    feedback_type != "Select Type" and category != "Select Category" and 
                    priority != "Select Priority" and feedback_text):
                    
                    if "@" in email and "." in email:
                        try:
                            conn = sqlite3.connect('feedback_database.db')
                            cursor = conn.cursor()
                            
                            cursor.execute('''
                                INSERT INTO feedback_submissions 
                                (student_id, student_name, email, department, course_code, 
                                 feedback_type, category, priority, feedback_text)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (student_id, student_name, email, department, course_code,
                                  feedback_type, category, priority, feedback_text))
                            
                            conn.commit()
                            conn.close()
                            
                            st.session_state['show_success'] = True
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"An error occurred while saving your feedback: {str(e)}")
                    else:
                        st.error("Please enter a valid email address.")
                else:
                    st.error("Please fill in all required fields marked with *.")

elif page == "⚙️ Admin Panel":
    if not st.session_state.admin_logged_in:
        st.markdown('<h1 class="main-header">⚙️ Admin Login</h1>', unsafe_allow_html=True)
        
        with st.form("admin_login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Login")
            
            if login_submitted:
                if username == "admin" and password == "admin123":
                    st.session_state.admin_logged_in = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    else:
        admin_tab = st.selectbox(
            "Admin Section",
            ["Dashboard", "Analytics", "Manage Submissions"]
        )
        if admin_tab == "Dashboard":
            st.markdown('<h1 class="main-header">📊 Feedback Dashboard</h1>', unsafe_allow_html=True)
            try:
                conn = sqlite3.connect('feedback_database.db')
                df = pd.read_sql_query("SELECT * FROM feedback_submissions", conn)
                conn.close()
                if not df.empty:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{len(df)}</div>
                            <div class="metric-label">Total Submissions</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        pending_count = len(df[df['status'] == 'Pending'])
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{pending_count}</div>
                            <div class="metric-label">Pending Review</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        high_priority = len(df[df['priority'].isin(['High', 'Urgent'])])
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{high_priority}</div>
                            <div class="metric-label">High Priority</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col4:
                        recent_submissions = len(df[pd.to_datetime(df['submission_date']) >= (datetime.datetime.now() - datetime.timedelta(days=7))])
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{recent_submissions}</div>
                            <div class="metric-label">This Week</div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('<h2 class="sub-header">📋 Recent Submissions</h2>', unsafe_allow_html=True)
                    recent_df = df.head(10)[['student_id', 'feedback_type', 'category', 'priority', 'status', 'submission_date']]
                    st.dataframe(recent_df, use_container_width=True)
                else:
                    st.markdown("""
                    <div class="info-box">
                        <h3 style="text-align: center;">No feedback submissions found</h3>
                        <p style="text-align: center;">Submit your first feedback using the form!</p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading dashboard data: {str(e)}")
        elif admin_tab == "Analytics":
            st.markdown('<h1 class="main-header">📈 Feedback Analytics</h1>', unsafe_allow_html=True)
            try:
                conn = sqlite3.connect('feedback_database.db')
                df = pd.read_sql_query("SELECT * FROM feedback_submissions", conn)
                conn.close()
                if not df.empty:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("📊 Feedback by Category")
                        category_counts = df['category'].value_counts()
                        fig = px.pie(values=category_counts.values, names=category_counts.index, title="Feedback Distribution by Category")
                        st.plotly_chart(fig, use_container_width=True)
                    with col2:
                        st.subheader("📊 Feedback by Priority")
                        priority_counts = df['priority'].value_counts()
                        fig = px.bar(x=priority_counts.index, y=priority_counts.values, title="Feedback Distribution by Priority")
                        st.plotly_chart(fig, use_container_width=True)
                    col3, col4 = st.columns(2)
                    with col3:
                        st.subheader("📊 Feedback by Type")
                        type_counts = df['feedback_type'].value_counts()
                        fig = px.bar(x=type_counts.index, y=type_counts.values, title="Feedback Distribution by Type")
                        st.plotly_chart(fig, use_container_width=True)
                    with col4:
                        st.subheader("📊 Feedback by Department")
                        dept_counts = df['department'].value_counts()
                        fig = px.bar(x=dept_counts.index, y=dept_counts.values, title="Feedback Distribution by Department")
                        st.plotly_chart(fig, use_container_width=True)
                    st.subheader("📊 Submission Status Distribution")
                    status_counts = df['status'].value_counts()
                    fig = px.pie(values=status_counts.values, names=status_counts.index, title="Submission Status Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.markdown("""
                    <div class="info-box">
                        <h3 style="text-align: center;">No data available for analytics</h3>
                        <p style="text-align: center;">Submit some feedback first!</p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading analytics data: {str(e)}")
        elif admin_tab == "Manage Submissions":
            conn = sqlite3.connect('feedback_database.db')
            df = pd.read_sql_query("SELECT * FROM feedback_submissions", conn)
            conn.close()
            if not df.empty:
                st.markdown('<h2 class="sub-header">📋 Manage Submissions</h2>', unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                with col1:
                    status_filter = st.selectbox("Filter by Status", ["All"] + list(df['status'].unique()))
                with col2:
                    priority_filter = st.selectbox("Filter by Priority", ["All"] + list(df['priority'].unique()))
                with col3:
                    category_filter = st.selectbox("Filter by Category", ["All"] + list(df['category'].unique()))
                filtered_df = df.copy()
                if status_filter != "All":
                    filtered_df = filtered_df[filtered_df['status'] == status_filter]
                if priority_filter != "All":
                    filtered_df = filtered_df[filtered_df['priority'] == priority_filter]
                if category_filter != "All":
                    filtered_df = filtered_df[filtered_df['category'] == category_filter]
                st.dataframe(filtered_df, use_container_width=True)
                st.markdown('<h2 class="sub-header">✍️ Respond to Submissions</h2>', unsafe_allow_html=True)
                submission_id = st.selectbox("Select Submission ID", filtered_df['id'].tolist())
                if submission_id:
                    submission = filtered_df[filtered_df['id'] == submission_id].iloc[0]
                    st.markdown(f"""
                    <div style="
                        background: #f0f4f8;
                        border-left: 6px solid #1f4e79;
                        padding: 1.2rem 1.5rem;
                        border-radius: 0.7rem;
                        margin-bottom: 1.5rem;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                        color: #1a1a1a;
                    ">
                        <h3 style="font-size:1.5rem;font-weight:bold;margin-top:0;color:#1a1a1a;">Submission Details:</h3>
                        <p style="color:#1a1a1a;"><strong>Student:</strong> {submission['student_name']} ({submission['student_id']})</p>
                        <p style="color:#1a1a1a;"><strong>Department:</strong> {submission['department']}</p>
                        <p style="color:#1a1a1a;"><strong>Category:</strong> {submission['category']}</p>
                        <p style="color:#1a1a1a;"><strong>Priority:</strong> {submission['priority']}</p>
                        <p style="color:#1a1a1a;"><strong>Feedback:</strong> {submission['feedback_text']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.form("admin_response"):
                        new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Completed", "Rejected"])
                        admin_response = st.text_area("Admin Response", placeholder="Enter your response to the student...")
                        response_submitted = st.form_submit_button("Update Submission")
                        if response_submitted:
                            conn = sqlite3.connect('feedback_database.db')
                            cursor = conn.cursor()
                            cursor.execute('''
                                UPDATE feedback_submissions 
                                SET status = ?, admin_response = ?, response_date = CURRENT_TIMESTAMP
                                WHERE id = ?
                            ''', (new_status, admin_response, submission_id))
                            conn.commit()
                            conn.close()
                            st.session_state['show_admin_success'] = True
                            st.rerun()
            else:
                st.markdown("""
                <div class="info-box">
                    <h3 style="text-align: center;">No submissions to manage</h3>
                    <p style="text-align: center;">No feedback submissions found in the system.</p>
                </div>
                """, unsafe_allow_html=True)

elif page == "❓ Help & Support":
    st.markdown('<h1 class="main-header">❓ Help & Support</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        background: #f5f7fa;
        border-left: 6px solid #d63384;
        padding: 1.2rem 1.5rem;
        border-radius: 0.7rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        color: #1a1a1a;
    ">
        <span style="font-size:1.2rem;font-weight:bold;color:#d63384;">☎️ Need Help?</span>
        <p style="margin-top:0.7rem;">
            If you need assistance with the feedback system or have questions, please contact:
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #1f4e79; margin-bottom: 1rem;">📧 Contact Information</h3>
            <p><strong>IT Support:</strong><br>
            Email: itsupport@calebuniversity.edu.ng<br>
            Phone: +234-803-123-4567</p>
            <p><strong>Student Affairs:</strong><br>
            Email: studentaffairs@calebuniversity.edu.ng<br>
            Phone: +234-802-234-5678</p>
            <p><strong>Academic Affairs:</strong><br>
            Email: academics@calebuniversity.edu.ng<br>
            Phone: +234-701-345-6789</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #1f4e79; margin-bottom: 1rem;">📋 FAQ</h3>
            <details>
                <summary><strong>How do I submit feedback?</strong></summary>
                <p>Use the 'Submit Feedback' page to fill out the form with your details and feedback.</p>
            </details>
            <details>
                <summary><strong>How long does it take to get a response?</strong></summary>
                <p>Responses are typically provided within 3-5 business days for regular submissions, and within 24 hours for urgent matters.</p>
            </details>
            <details>
                <summary><strong>Is my feedback confidential?</strong></summary>
                <p>Yes, all feedback submissions are treated with strict confidentiality. Only authorized personnel have access to the submissions.</p>
            </details>
            <details>
                <summary><strong>Can I track my submission status?</strong></summary>
                <p>Currently, you can view recent submissions in the Dashboard. We're working on individual tracking features.</p>
            </details>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #1f4e79; margin-bottom: 1rem;">📚 Guidelines for Effective Feedback</h3>
        <ul>
            <li><strong>Be Specific:</strong> Provide concrete examples and details</li>
            <li><strong>Be Constructive:</strong> Suggest solutions when possible</li>
            <li><strong>Be Respectful:</strong> Use professional and courteous language</li>
            <li><strong>Be Timely:</strong> Submit feedback as close to the event as possible</li>
            <li><strong>Be Honest:</strong> Provide accurate and truthful information</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2024 Caleb University Feedback System | Developed for Academic Excellence</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem;">
        🎓 Empowering Students, Enhancing Education
    </p>
</div>
""", unsafe_allow_html=True) 