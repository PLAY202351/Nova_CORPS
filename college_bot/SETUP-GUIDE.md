# COMPLETE FILE LIST FOR COLLEGE CHATBOT PROJECT

## FOLDER STRUCTURE TO CREATE:

```
college_bot/                    ← Create this main folder
│
├── app.py                      ← Download file #1
├── requirements.txt            ← Download file #2  
├── schema.sql                  ← Download file #3
├── generate-passwords.py       ← Download file #4
├── .env                        ← Download file #5 (then edit with your keys)
├── .gitignore                  ← Download file #6
├── README.md                   ← Download file #7 (setup instructions)
│
├── templates/                  ← Create this folder manually
│   ├── login.html              ← Download file #8
│   ├── chat.html               ← Download file #9
│   ├── admin_dashboard.html    ← Download file #10
│   ├── analytics.html          ← Download file #11
│   └── register.html           ← Download file #12
│
└── static/                     ← Create this folder manually
    └── style.css               ← Download file #13
```

## FILES YOU NEED TO DOWNLOAD:

All files have been created above. Here's what each file does:

### Root Directory Files:

1. **app.py** - Main Flask application with all routes and GPT-4 integration
2. **requirements.txt** - Python packages to install
3. **schema.sql** - MySQL database schema with tables
4. **generate-passwords.py** - Script to generate password hashes
5. **.env** - Environment variables (YOU MUST EDIT THIS WITH YOUR API KEYS)
6. **.gitignore** - Files to ignore in Git
7. **README.md** - Complete setup instructions

### templates/ Folder:

8. **login.html** - Login page for students and moderators
9. **chat.html** - Student chat interface
10. **admin_dashboard.html** - Moderator dashboard (NEED TO CREATE THIS - SEE BELOW)
11. **analytics.html** - Analytics page (NEED TO CREATE THIS - SEE BELOW)
12. **register.html** - User registration page (NEED TO CREATE THIS - SEE BELOW)

### static/ Folder:

13. **style.css** - All CSS styling (NEED TO CREATE THIS - SEE BELOW)

---

## STEPS TO SET UP IN VS CODE:

### 1. Create Folders
```
college_bot/
college_bot/templates/
college_bot/static/
```

### 2. Download Files
- Download all 13 files I created above
- Place them in correct folders as shown in structure

### 3. Install MySQL
- Windows: https://dev.mysql.com/downloads/installer/
- Mac: `brew install mysql`
- Linux: `sudo apt install mysql-server`

### 4. Setup Virtual Environment
Open terminal in VS Code:
```bash
cd college_bot
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
```

### 5. Setup Database
```bash
mysql -u root -p
CREATE DATABASE college_chatbot;
USE college_chatbot;
SOURCE schema.sql;
exit
```

### 6. Generate Password Hashes
```bash
python generate-passwords.py
```
Copy the output and update the INSERT statements in schema.sql

### 7. Edit .env File
Add your real values:
```
OPENAI_API_KEY=sk-your-key-here
MYSQL_PASSWORD=your-mysql-password
SECRET_KEY=run: python -c "import secrets; print(secrets.token_hex(16))"
```

### 8. Run Application
```bash
python app.py
```

### 9. Open Browser
Go to: http://localhost:5000

---

## LOGIN CREDENTIALS (Default):

**Student:**
- College ID: 21CS105
- Password: student123

**Moderator:**
- Mod ID: MOD001  
- Password: admin123

---

## WHAT YOU NEED:

1. ✅ Python 3.8+ installed
2. ✅ MySQL installed and running
3. ✅ OpenAI API key (get from platform.openai.com)
4. ✅ VS Code (or any code editor)
5. ✅ All 13 files downloaded

---

## IF YOU GET ERRORS:

**"No module named 'flask'"**
→ Activate virtual environment: `venv\Scripts\activate`

**"Can't connect to MySQL"**
→ Start MySQL service

**"Invalid password"**  
→ Run generate-passwords.py and update schema.sql

**"OpenAI API error"**
→ Check API key in .env file

---

Read README.md for full detailed instructions!
