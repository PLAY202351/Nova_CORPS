from flask import Flask, render_template, request, session, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Ollama API configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# MySQL configuration
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE', 'college_chatbot')
    )

# Helper function to fetch context from database
def get_college_context():
    """Fetch all college information to provide context to LLM"""
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    context = {
        'schedule': [],
        'restaurants': [],
        'hostels': [],
        'gyms': []
    }
    
    cursor.execute("SELECT * FROM schedule")
    context['schedule'] = cursor.fetchall()
    
    cursor.execute("SELECT * FROM restaurants")
    context['restaurants'] = cursor.fetchall()
    
    cursor.execute("SELECT * FROM hostels")
    context['hostels'] = cursor.fetchall()
    
    cursor.execute("SELECT * FROM gyms")
    context['gyms'] = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return context

# Format context for LLM
def format_context_for_llm(context):
    """Convert database context into a readable format"""
    formatted = "College Information:\n\n"
    
    formatted += "CLASS SCHEDULE:\n"
    for item in context['schedule']:
        formatted += f"- {item['course']}: {item['day']} at {item['time']} in {item['room']}\n"
    
    formatted += "\nRESTAURANTS NEARBY:\n"
    for item in context['restaurants']:
        formatted += f"- {item['name']} ({item['cuisine']}): {item['address']}, Rating: {item['rating']}★\n"
    
    formatted += "\nHOSTELS:\n"
    for item in context['hostels']:
        formatted += f"- {item['name']}: {item['address']}, Capacity: {item['capacity']}\n"
    
    formatted += "\nGYMS:\n"
    for item in context['gyms']:
        formatted += f"- {item['name']}: {item['address']}, Features: {item['features']}\n"
    
    return formatted

# Call Ollama API
def get_ollama_response(prompt):
    """Get response from Ollama running locally"""
    try:
        payload = {
            "model": "mistral",  # or "llama2" if you prefer
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7,
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', 'Sorry, I could not generate a response.')
        else:
            return f"Error: Ollama API returned status {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama. Make sure Ollama is running (ollama serve)"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_type = request.form.get('login_type')
        
        if login_type == 'student':
            college_id = request.form.get('college_id')
            password = request.form.get('password')
            
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE college_id = %s", (college_id,))
            user = cursor.fetchone()
            cursor.close()
            db.close()
            
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_type'] = 'student'
                return redirect(url_for('chat'))
            else:
                flash('Invalid college ID or password', 'error')
        
        elif login_type == 'moderator':
            mod_id = request.form.get('mod_id')
            password = request.form.get('password')
            
            print(f"DEBUG: Attempting moderator login with ID: {mod_id}")
            
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            
            # Check if moderators table has data
            cursor.execute("SELECT COUNT(*) as count FROM moderators")
            count = cursor.fetchone()['count']
            print(f"DEBUG: Total moderators in DB: {count}")
            
            # Try to fetch moderator
            cursor.execute("SELECT * FROM moderators WHERE mod_id = %s", (mod_id,))
            moderator = cursor.fetchone()
            
            print(f"DEBUG: Moderator found: {moderator is not None}")
            
            if moderator:
                print(f"DEBUG: Moderator data: {moderator}")
                print(f"DEBUG: Checking password hash...")
                password_match = check_password_hash(moderator['password_hash'], password)
                print(f"DEBUG: Password matches: {password_match}")
                
                if password_match:
                    session['moderator_id'] = moderator['id']
                    session['moderator_name'] = moderator['name']
                    session['user_type'] = 'moderator'
                    cursor.close()
                    db.close()
                    print(f"DEBUG: Login successful!")
                    return redirect(url_for('admin_dashboard'))
                else:
                    print(f"DEBUG: Password mismatch")
                    flash('Invalid moderator ID or password', 'error')
            else:
                print(f"DEBUG: Moderator ID '{mod_id}' not found in database")
                # Show all moderator IDs for debugging
                cursor.execute("SELECT mod_id FROM moderators")
                all_mods = cursor.fetchall()
                print(f"DEBUG: Available moderator IDs: {all_mods}")
                flash('Invalid moderator ID or password', 'error')
            
            cursor.close()
            db.close()
    
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session or session.get('user_type') != 'student':
        return redirect(url_for('login'))
    
    messages = []
    
    if request.method == 'POST':
        question = request.form.get('question')
        print(f"DEBUG: Received question: {question}")
        
        if question:
            context = get_college_context()
            context_text = format_context_for_llm(context)
            
            print("DEBUG: Calling Ollama Local LLM...")
            
            # Create prompt with context
            prompt = f"""You are a friendly and helpful college assistant chatbot. 
Your role is to help students with information about their schedule, nearby restaurants, 
hostels, gyms, and general college queries. Always greet users warmly and provide 
detailed, friendly responses. Use emojis occasionally to make conversations engaging.

Here is the current college information you have access to:
{context_text}

When students ask about schedules, restaurants, hostels, or gyms, use this information 
to provide accurate answers. If you don't have specific information, politely let them know 
and suggest they contact the college office.

Student Question: {question}

Please provide a helpful response:"""
            
            answer = get_ollama_response(prompt)
            print(f"DEBUG: Got answer: {answer[:100]}...")
            
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO chat_logs (user_id, question, answer) VALUES (%s, %s, %s)",
                (session['user_id'], question, answer)
            )
            db.commit()
            cursor.close()
            db.close()
            print("DEBUG: Saved to database")
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT question, answer, created_at FROM chat_logs WHERE user_id = %s ORDER BY created_at ASC",
        (session['user_id'],)
    )
    messages = cursor.fetchall()
    cursor.close()
    db.close()
    
    return render_template('chat.html', messages=messages, user_name=session['user_name'])

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'moderator_id' not in session or session.get('user_type') != 'moderator':
        return redirect(url_for('login'))
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_schedule':
            cursor.execute(
                "INSERT INTO schedule (course, day, time, room) VALUES (%s, %s, %s, %s)",
                (request.form.get('course'), request.form.get('day'), 
                 request.form.get('time'), request.form.get('room'))
            )
            db.commit()
            flash('Schedule added successfully', 'success')
        
        elif action == 'add_restaurant':
            cursor.execute(
                "INSERT INTO restaurants (name, cuisine, address, rating) VALUES (%s, %s, %s, %s)",
                (request.form.get('name'), request.form.get('cuisine'), 
                 request.form.get('address'), request.form.get('rating'))
            )
            db.commit()
            flash('Restaurant added successfully', 'success')
        
        elif action == 'add_hostel':
            cursor.execute(
                "INSERT INTO hostels (name, address, capacity) VALUES (%s, %s, %s)",
                (request.form.get('name'), request.form.get('address'), 
                 request.form.get('capacity'))
            )
            db.commit()
            flash('Hostel added successfully', 'success')
        
        elif action == 'add_gym':
            cursor.execute(
                "INSERT INTO gyms (name, address, features) VALUES (%s, %s, %s)",
                (request.form.get('name'), request.form.get('address'), 
                 request.form.get('features'))
            )
            db.commit()
            flash('Gym added successfully', 'success')
        
        elif action.startswith('delete_'):
            table = action.replace('delete_', '')
            cursor.execute(f"DELETE FROM {table} WHERE id = %s", (request.form.get('id'),))
            db.commit()
            flash(f'{table.title()} deleted successfully', 'success')
    
    cursor.execute("SELECT * FROM schedule ORDER BY day, time")
    schedules = cursor.fetchall()
    
    cursor.execute("SELECT * FROM restaurants ORDER BY rating DESC")
    restaurants = cursor.fetchall()
    
    cursor.execute("SELECT * FROM hostels ORDER BY name")
    hostels = cursor.fetchall()
    
    cursor.execute("SELECT * FROM gyms ORDER BY name")
    gyms = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return render_template(
        'admin_dashboard.html',
        moderator_name=session['moderator_name'],
        schedules=schedules,
        restaurants=restaurants,
        hostels=hostels,
        gyms=gyms
    )

@app.route('/analytics')
def analytics():
    if 'moderator_id' not in session or session.get('user_type') != 'moderator':
        return redirect(url_for('login'))
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT COUNT(*) as total FROM chat_logs")
    total_chats = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(DISTINCT user_id) as active FROM chat_logs")
    active_users = cursor.fetchone()['active']
    
    cursor.execute("""
        SELECT question, COUNT(*) as freq 
        FROM chat_logs 
        GROUP BY question 
        ORDER BY freq DESC 
        LIMIT 5
    """)
    top_questions = cursor.fetchall()
    
    cursor.execute("""
        SELECT u.name, u.college_id, COUNT(c.id) as chat_count
        FROM users u
        JOIN chat_logs c ON u.id = c.user_id
        GROUP BY u.id
        ORDER BY chat_count DESC
        LIMIT 5
    """)
    top_users = cursor.fetchall()
    
    cursor.execute("""
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM chat_logs
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY DATE(created_at)
        ORDER BY date DESC
    """)
    daily_stats = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return render_template(
        'analytics.html',
        moderator_name=session['moderator_name'],
        total_chats=total_chats,
        active_users=active_users,
        top_questions=top_questions,
        top_users=top_users,
        daily_stats=daily_stats
    )

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        college_id = request.form.get('college_id')
        password = request.form.get('password')
        
        password_hash = generate_password_hash(password)
        
        db = get_db_connection()
        cursor = db.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (name, college_id, password_hash) VALUES (%s, %s, %s)",
                (name, college_id, password_hash)
            )
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('College ID already exists', 'error')
        finally:
            cursor.close()
            db.close()
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)