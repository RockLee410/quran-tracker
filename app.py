import streamlit as st
from supabase import create_client

# --- QURAN METADATA & HELPER FUNCTIONS ---
SURAH_DATA = [
    (1, "Al-Fatihah", 1, 1), (2, "Al-Baqarah", 2, 49), (3, "Aal-Imran", 50, 76), 
    (4, "An-Nisa", 77, 106), (5, "Al-Ma'idah", 106, 127), (6, "Al-An'am", 128, 150), 
    (7, "Al-A'raf", 151, 176), (8, "Al-Anfal", 177, 186), (9, "At-Tawbah", 187, 207), 
    (10, "Yunus", 208, 221), (11, "Hud", 221, 235), (12, "Yusuf", 235, 248), 
    (13, "Ar-Ra'd", 249, 255), (14, "Ibrahim", 255, 261), (15, "Al-Hijr", 262, 267), 
    (16, "An-Nahl", 267, 281), (17, "Al-Isra", 282, 293), (18, "Al-Kahf", 293, 304), 
    (19, "Maryam", 305, 312), (20, "Taha", 312, 321), (21, "Al-Anbiya", 322, 331), 
    (22, "Al-Hajj", 332, 341), (23, "Al-Mu'minun", 342, 349), (24, "An-Nur", 350, 359), 
    (25, "Al-Furqan", 359, 366), (26, "Ash-Shu'ara", 367, 376), (27, "An-Naml", 377, 385), 
    (28, "Al-Qasas", 385, 396), (29, "Al-Ankabut", 396, 404), (30, "Ar-Rum", 404, 410), 
    (31, "Luqman", 411, 414), (32, "As-Sajdah", 415, 417), (33, "Al-Ahzab", 418, 427), 
    (34, "Saba", 428, 434), (35, "Fatir", 434, 440), (36, "Ya-Sin", 440, 445), 
    (37, "As-Saffat", 446, 452), (38, "Sad", 453, 458), (39, "Az-Zumar", 458, 467), 
    (40, "Ghafir", 467, 476), (41, "Fussilat", 477, 482), (42, "Ash-Shura", 483, 489), 
    (43, "Az-Zukhruf", 489, 495), (44, "Ad-Dukhan", 496, 498), (45, "Al-Jathiyah", 499, 502), 
    (46, "Al-Ahqaf", 502, 506), (47, "Muhammad", 507, 510), (48, "Al-Fath", 511, 515), 
    (49, "Al-Hujurat", 515, 517), (50, "Qaf", 518, 520), (51, "Ad-Zariyat", 520, 523), 
    (52, "At-Tur", 523, 525), (53, "An-Najm", 526, 528), (54, "Al-Qamar", 528, 531), 
    (55, "Ar-Rahman", 531, 534), (56, "Al-Waqi'ah", 534, 537), (57, "Al-Hadid", 537, 541), 
    (58, "Al-Mujadila", 542, 545), (59, "Al-Hashr", 545, 548), (60, "Al-Mumtahanah", 549, 551), 
    (61, "As-Saff", 551, 552), (62, "Al-Jumu'ah", 553, 554), (63, "Al-Munafiqun", 554, 555), 
    (64, "At-Taghabun", 556, 557), (65, "At-Talaq", 558, 559), (66, "At-Tahrim", 560, 561), 
    (67, "Al-Mulk", 562, 564), (68, "Al-Qalam", 564, 566), (69, "Al-Haqqah", 566, 568), 
    (70, "Al-Ma'arij", 568, 570), (71, "Nuh", 570, 571), (72, "Al-Jinn", 572, 573), 
    (73, "Al-Muzzammil", 574, 575), (74, "Al-Muddaththir", 575, 577), (75, "Al-Qiyamah", 577, 578), 
    (76, "Al-Insan", 578, 580), (77, "Al-Mursalat", 580, 581), (78, "An-Naba", 582, 583), 
    (79, "An-Nazi'at", 583, 584), (80, "Abasa", 585, 585), (81, "At-Takwir", 586, 586), 
    (82, "Al-Infitar", 587, 587), (83, "Al-Mutaffifin", 587, 589), (84, "Al-Inshiqaq", 589, 589), 
    (85, "Al-Buruj", 590, 590), (86, "At-Tariq", 591, 591), (87, "Al-A'la", 591, 592), 
    (88, "Al-Ghashiyah", 592, 592), (89, "Al-Fajr", 593, 594), (90, "Al-Balad", 594, 594), 
    (91, "Ash-Shams", 595, 595), (92, "Al-Lail", 595, 596), (93, "Ad-Duha", 596, 596), 
    (94, "Ash-Sharh", 596, 596), (95, "At-Tin", 597, 597), (96, "Al-Alaq", 597, 598), 
    (97, "Al-Qadr", 598, 598), (98, "Al-Bayyinah", 598, 599), (99, "Az-Zalzalah", 599, 599), 
    (100, "Al-Adiyat", 599, 600), (101, "Al-Qari'ah", 600, 600), (102, "At-Takathur", 600, 600), 
    (103, "Al-Asr", 601, 601), (104, "Al-Humazah", 601, 601), (105, "Al-Fil", 601, 601), 
    (106, "Quraish", 602, 602), (107, "Al-Ma'un", 602, 602), (108, "Al-Kawthar", 602, 602), 
    (109, "Al-Kafirun", 603, 603), (110, "An-Nasr", 603, 603), (111, "Al-Masad", 603, 603), 
    (112, "Al-Ikhlas", 604, 604), (113, "Al-Falaq", 604, 604), (114, "An-Nas", 604, 604)
]

def get_juz(page_num):
    juz_starts = [1, 22, 42, 62, 82, 102, 122, 142, 162, 182, 202, 222, 242, 262, 282, 302, 322, 342, 362, 382, 402, 422, 442, 462, 482, 502, 522, 542, 562, 582]
    for i, start in reversed(list(enumerate(juz_starts))):
        if page_num >= start: return i + 1
    return 1

# Connect to Supabase
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)

st.set_page_config(page_title="Quran Progress Tracker", layout="centered")

if "user" not in st.session_state:
    st.session_state["user"] = None

# --- AUTHENTICATION SCREEN ---
if st.session_state["user"] is None:
    st.title("📖 Quran Tracker")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log In"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state["user"] = res.user
                st.rerun()
            except Exception as e:
                st.error("Invalid email or password.")

    with tab2:
        st.subheader("Sign Up")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")
        role = st.selectbox("I am a:", ["student", "teacher", "coordinator"])
        if st.button("Create Account"):
            try:
                res = supabase.auth.sign_up({"email": email, "password": password})
                user_id = res.user.id
                
                # Save profile details
                supabase.table("profiles").insert({
                    "id": user_id, 
                    "email": email, 
                    "role": role
                }).execute()
                
                # Initialize student progress record
                if role == "student":
                    supabase.table("progress").insert({"student_id": user_id, "current_page": 1, "current_juz": 1}).execute()
                
                st.success("Account created successfully! Switch to the Login tab to log in.")
            except Exception as e:
                st.error(f"Error: {e}")

# --- DASHBOARD SCREEN ---
else:
    user = st.session_state["user"]
    
    # Fetch user role from database (Auto-creates missing profile row if needed)
    profile_res = supabase.table("profiles").select("*").eq("id", user.id).execute()
    if not profile_res.data:
        supabase.table("profiles").insert({"id": user.id, "email": user.email, "role": "student"}).execute()
        profile_res = supabase.table("profiles").select("*").eq("id", user.id).execute()
        
    role = profile_res.data[0].get("role", "student")

    st.sidebar.write(f"Logged in as: **{user.email}** ({role.capitalize()})")
    if st.sidebar.button("Log Out"):
        supabase.auth.sign_out()
        st.session_state["user"] = None
        st.rerun()

    st.title(f"📖 {role.capitalize()} Dashboard")

    # --- 1. STUDENT VIEW ---
    if role == "student":
        st.subheader("🗺️ Quran Memorization Map (604 Pages)")
        
        # Fetch status overrides for this student
        status_res = supabase.table("page_status").select("*").eq("student_id", user.id).execute()
        status_map = {row["page_number"]: row["status"] for row in (status_res.data or [])}

        # Color configurations
        color_map = {
            "tested": "#15803d",       # Dark Green
            "memorized": "#4ade80",    # Light Green
            "active": "#facc15",       # Yellow
            "unmemorized": "#374151"   # Gray
        }
        
        text_color_map = {
            "tested": "#ffffff",
            "memorized": "#000000",
            "active": "#000000",
            "unmemorized": "#9ca3af"
        }

        # Legend
        st.markdown("""
        <div style="display: flex; gap: 15px; flex-wrap: wrap; margin-bottom: 15px; font-size: 0.85rem;">
            <span><span style="color:#15803d;">■</span> Dark Green: Memorized & Tested</span>
            <span><span style="color:#4ade80;">■</span> Light Green: Memorized (Untested)</span>
            <span><span style="color:#facc15;">■</span> Yellow: Active Revision</span>
            <span><span style="color:#374151;">■</span> Gray: Not Memorized</span>
        </div>
        """, unsafe_allow_html=True)

        # Juz Page Boundaries (Standard Madani Mushaf)
        juz_starts = [1, 22, 42, 62, 82, 102, 122, 142, 162, 182, 202, 222, 242, 262, 282, 302, 322, 342, 362, 382, 402, 422, 442, 462, 482, 502, 522, 542, 562, 582]

        # Build 30-row layout (1 dedicated row per Juz)
        grid_html = '<div style="max-height: 520px; overflow-y: auto; padding: 10px; background: #111827; border-radius: 8px; display: flex; flex-direction: column; gap: 8px;">'

        for juz_num in range(1, 31):
            start_p = juz_starts[juz_num - 1]
            end_p = (juz_starts[juz_num] - 1) if juz_num < 30 else 604
            
            grid_html += '<div style="display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.03); padding: 5px 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">'
            grid_html += f'<div style="min-width: 55px; font-size: 0.75rem; font-weight: bold; color: #facc15;">Juz {juz_num}</div>'
            grid_html += '<div style="display: flex; flex-wrap: nowrap; overflow-x: auto; gap: 4px; flex-grow: 1; padding: 2px 0;">'
            
            for page in range(start_p, end_p + 1):
                p_status = status_map.get(page, "unmemorized")
                bg_col = color_map[p_status]
                txt_col = text_color_map[p_status]
                
                grid_html += f'<div title="Page {page}: {p_status.capitalize()}" style="background-color: {bg_col}; color: {txt_col}; text-align: center; font-size: 0.65rem; font-weight: bold; border-radius: 3px; min-width: 24px; height: 26px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; user-select: none;">{page}</div>'
                
            grid_html += '</div></div>'

        grid_html += '</div>'
        
        st.markdown(grid_html, unsafe_allow_html=True)
        st.divider()

        # Section 2: Teacher Logged Sessions
        st.subheader("📋 Session History (From Teacher)")
        logs_res = supabase.table("daily_logs").select("*").eq("student_id", user.id).order("log_date", desc=True).execute()
        
        if not logs_res.data:
            st.info("No recorded sessions from your teacher yet.")
        else:
            import pandas as pd
            df_logs = pd.DataFrame(logs_res.data)
            display_df = df_logs[["log_date", "from_surah", "to_surah", "from_page", "to_page", "minutes", "notes"]]
            display_df.columns = ["Date", "From Surah", "To Surah", "Start Page", "End Page", "Mins", "Teacher Notes"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.divider()

        # Section 3: Personal Notes & Goals
        st.subheader("📝 Personal Notes & Goals")
        
        with st.form("add_student_note", clear_on_submit=True):
            new_note = st.text_area("Write a new note or goal:")
            if st.form_submit_button("Save Note"):
                if new_note.strip():
                    supabase.table("student_notes").insert({"student_id": user.id, "content": new_note}).execute()
                    st.success("Note added!")
                    st.rerun()
                else:
                    st.warning("Note cannot be empty.")

        # Display history newest to oldest
        notes_res = supabase.table("student_notes").select("*").eq("student_id", user.id).order("created_at", desc=True).execute()
        
        if notes_res.data:
            st.write("**Saved Notes & Goals:**")
            for note in notes_res.data:
                created_dt = note["created_at"][:16].replace("T", " ")
                st.markdown(f"""
                <div style="background-color: rgba(255,255,255,0.05); border-left: 3px solid #facc15; padding: 10px; margin-bottom: 8px; border-radius: 0 5px 5px 0;">
                    <small style="color: #9ca3af;">{created_dt}</small>
                    <p style="margin: 4px 0 0 0; color: #f3f4f6;">{note['content']}</p>
                </div>
                """, unsafe_allow_html=True)

    # --- 2. TEACHER VIEW ---
    elif role == "teacher":
        st.subheader("👨‍🏫 Student Progress Entry")
        
        # Get assigned students
        students_res = supabase.table("profiles").select("*").eq("role", "student").eq("teacher_id", user.id).execute()
        students = students_res.data

        if not students:
            st.info("No students allocated to you yet.")
        else:
            student_dict = {s["email"]: s["id"] for s in students}
            selected_email = st.selectbox("Select Student:", list(student_dict.keys()))
            selected_id = student_dict[selected_email]

            surah_list = [f"{s[0]}. {s[1]}" for s in SURAH_DATA]

            tab_pages, tab_surah = st.tabs(["📄 Log Page Range", "📖 Log Specific Surah"])

            with tab_pages:
                with st.form("teacher_log_pages"):
                    col1, col2 = st.columns(2)
                    with col1:
                        from_p = st.number_input("From Page", min_value=1, max_value=604, value=1)
                        to_p = st.number_input("To Page", min_value=1, max_value=604, value=1)
                    with col2:
                        session_date = st.date_input("Date")
                        mins = st.number_input("Minutes Spent", min_value=1, value=15)

                    notes = st.text_input("Teacher Feedback / Notes", placeholder="e.g., Excellent Tajweed on verse 10")
                    
                    if st.form_submit_button("Save Session"):
                        # Auto-detect Surah names from page numbers
                        f_surah = next((f"{s[0]}. {s[1]}" for s in SURAH_DATA if s[2] <= from_p <= s[3]), "")
                        t_surah = next((f"{s[0]}. {s[1]}" for s in SURAH_DATA if s[2] <= to_p <= s[3]), f_surah)

                        supabase.table("daily_logs").insert({
                            "student_id": selected_id,
                            "log_date": str(session_date),
                            "from_surah": f_surah,
                            "to_surah": t_surah,
                            "from_page": int(from_p),
                            "to_page": int(to_p),
                            "minutes": int(mins),
                            "notes": notes
                        }).execute()

                        # Automatically update progress table
                        new_juz = get_juz(to_p)
                        supabase.table("progress").upsert({"student_id": selected_id, "current_page": int(to_p), "current_juz": new_juz}).execute()

                        st.success(f"Recorded Page {from_p} to {to_p} for {selected_email}!")
                        st.rerun()

            with tab_surah:
                with st.form("teacher_log_surah"):
                    selected_surah = st.selectbox("Select Surah Completed:", surah_list)
                    s_notes = st.text_input("Notes", key="s_notes")
                    
                    if st.form_submit_button("Log Complete Surah"):
                        surah_rec = next(s for s in SURAH_DATA if f"{s[0]}. {s[1]}" == selected_surah)
                        supabase.table("daily_logs").insert({
                            "student_id": selected_id,
                            "from_surah": selected_surah,
                            "to_surah": selected_surah,
                            "from_page": surah_rec[2],
                            "to_page": surah_rec[3],
                            "notes": s_notes
                        }).execute()
                        
                        st.success(f"Logged Surah {surah_rec[1]} for {selected_email}!")
                        st.rerun()

    # --- 3. COORDINATOR VIEW ---
    elif role == "coordinator":
        st.subheader("👩‍🏫 Allocate Students to Teachers")
        
        teachers_res = supabase.table("profiles").select("*").eq("role", "teacher").execute()
        students_res = supabase.table("profiles").select("*").eq("role", "student").execute()
        
        teachers = teachers_res.data
        students = students_res.data
        
        if not teachers or not students:
            st.warning("Ensure you have created at least one student and one teacher account.")
        else:
            teacher_options = {t["email"]: t["id"] for t in teachers}
            student_options = {s["email"]: s for s in students}
            
            col_a, col_b = st.columns(2)
            with col_a:
                selected_student_email = st.selectbox("Select Student:", list(student_options.keys()))
            with col_b:
                selected_teacher_email = st.selectbox("Assign To Teacher:", list(teacher_options.keys()))
                
            student_obj = student_options[selected_student_email]
            teacher_id = teacher_options[selected_teacher_email]
            
            # Display current assignment status
            current_teacher_id = student_obj.get("teacher_id")
            if current_teacher_id:
                matched_teacher = [t["email"] for t in teachers if t["id"] == current_teacher_id]
                current_t_name = matched_teacher[0] if matched_teacher else "Unknown"
                st.info(f"Currently assigned to: **{current_t_name}**")
            else:
                st.info("Currently unassigned.")
                
            if st.button("Save Allocation"):
                supabase.table("profiles").update({"teacher_id": teacher_id}).eq("id", student_obj["id"]).execute()
                st.success(f"Assigned {selected_student_email} to {selected_teacher_email}!")
                st.rerun()

        st.divider()

        st.subheader("📋 Pending Milestone Tests")
        tests_res = supabase.table("tests").select("*, profiles(email)").eq("status", "pending").execute()
        tests = tests_res.data

        if not tests:
            st.success("No pending milestone tests.")
        else:
            for test in tests:
                student_email = test.get("profiles", {}).get("email", "Student")
                st.write(f"**Student:** {student_email} | **Juz Milestone:** {test['juz_milestone']}")
                score = st.number_input("Test Score (0-100)", min_value=0, max_value=100, key=f"score_{test['id']}")
                notes = st.text_input("Feedback Notes", key=f"notes_{test['id']}")
                
                if st.button("Submit Result", key=f"btn_{test['id']}"):
                    status = "passed" if score >= 60 else "failed"
                    supabase.table("tests").update({"score": score, "notes": notes, "status": status}).eq("id", test['id']).execute()
                    st.success(f"Test recorded as {status.upper()}!")
                    st.rerun()