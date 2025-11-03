# College Assistant Chatbot - Flask Application

A complete college assistant chatbot with GPT-4 integration, dual login system (students & moderators), and analytics dashboard.

## 📁 Project Structure

```
college_bot/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── schema.sql             # MySQL database schema
├── generate-passwords.py  # Password hash generator
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore file
│
├── templates/            # HTML templates folder
│   ├── login.html
│   ├── chat.html
│   ├── admin_dashboard.html
│   ├── analytics.html
│   └── register.html
│
└── static/              # CSS folder
    └── style.css
```

## 🚀 Quick Setup Guide

### Step 1: Install MySQL

**Windows:**
- Download from https://dev.mysql.com/downloads/installer/
- Install MySQL Server and MySQL Workbench

**Mac:**
```bash
brew install mysql
brew services start mysql
```

**Linux:**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
```

### Step 2: Create Project Folder

```bash
# Create and navigate to project folder
mkdir college_bot
cd college_bot
```

### Step 3: Copy All Files

Download all the files I provided and organize them:

- Put `app.py`, `requirements.txt`, `schema.sql`, `generate-passwords.py`, `.env`, `.gitignore` in the **root** folder
- Create a `templates` folder and put all `.html` files inside
- Create a `static` folder and put `style.css` inside

### Step 4: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Setup Database

```bash
# Login to MySQL
mysql -u root -p
# Enter your MySQL root password
```

Then run these commands:
```sql
CREATE DATABASE college_chatbot;
USE college_chatbot;
SOURCE schema.sql;
```

Or if you're on Windows, copy the entire content of `schema.sql` and paste it into MySQL Workbench and execute.

### Step 7: Generate Password Hashes

```bash
python generate-passwords.py
```

Copy the generated password hashes and update them in `schema.sql` file in the INSERT statements, then re-run the SQL inserts.

### Step 8: Configure Environment Variables

Edit the `.env` file:

```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=college_chatbot
SECRET_KEY=generate-this-with-command-below
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(16))"
```

Copy the output and paste it as your SECRET_KEY value.

**Get OpenAI API Key:**
1. Go to https://platform.openai.com/
2. Sign up or login
3. Go to API Keys section
4. Create new secret key
5. Copy and paste it in `.env`

### Step 9: Run the Application

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 10: Open in Browser

Navigate to: `http://localhost:5000`

## 🔐 Login Credentials (Default)

**Student Login:**
- College ID: `21CS105`
- Password: `student123`

**Moderator Login:**
- Moderator ID: `MOD001`
- Password: `admin123`

## 📝 Features

✅ Student chat interface with GPT-4  
✅ Moderator admin dashboard  
✅ CRUD operations for schedules, restaurants, hostels, gyms  
✅ Analytics dashboard  
✅ Chat history logging  
✅ User registration  
✅ Secure password hashing  
✅ No JavaScript (Pure Flask/HTML/CSS)

## 🛠️ Troubleshooting

### Error: "No module named 'flask'"
```bash
# Make sure virtual environment is activated
# Then reinstall
pip install -r requirements.txt
```

### Error: "Can't connect to MySQL server"
```bash
# Check if MySQL is running
# Windows: Open Services and start MySQL
# Mac: brew services start mysql
# Linux: sudo systemctl start mysql
```

### Error: "Table doesn't exist"
```bash
# Re-run the schema
mysql -u root -p college_chatbot < schema.sql
```

### Error: "Invalid password"
Make sure you ran `generate-passwords.py` and updated the hashes in `schema.sql`

## 📊 Usage

### For Students:
1. Login with college ID
2. Ask questions in natural language
3. Get instant responses from GPT-4
4. View chat history

### For Moderators:
1. Login with moderator ID
2. Manage college data (schedules, restaurants, etc.)
3. View analytics
4. Monitor user activity

## 🎓 For Submission

This project demonstrates:
- Full-stack web development
- Database design and management
- API integration (OpenAI GPT-4)
- Authentication and authorization
- CRUD operations
- Security best practices
- MVC architecture

## 📦 What to Submit

1. All code files (.py, .html, .css, .sql)
2. requirements.txt
3. README.md (this file)
4. Screenshots of working application
5. .env.example (copy of .env with dummy values)

## ⚠️ Important Notes

- **Never commit .env file** - It contains secrets
- **GPT-4 costs money** - Monitor your OpenAI usage
- **Use GPT-3.5-turbo** - For cheaper alternative, change model name in app.py line 68
- **Test locally first** - Before any deployment

## 🔄 Next Steps

- Deploy to cloud (Heroku, AWS, DigitalOcean)
- Add more features (file uploads, voice input)
- Improve UI/UX
- Add rate limiting
- Implement caching

## 📞 Support

If you face issues:
1. Check the error message in terminal
2. Verify all files are in correct folders
3. Ensure MySQL is running
4. Check .env file has correct values
5. Make sure virtual environment is activated

Good luck! 🚀
