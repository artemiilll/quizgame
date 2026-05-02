
import sqlite3
from flask import *
from random import randint
import db_scripts as db
import os

folder = os.getcwd()

app = Flask(__name__, template_folder=folder, static_folder=folder)
app.config['SECRET_KEY'] = 'VeryStrongKey'

def get_question_after(question_id=0, quiz_id=1):
    db.open()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id '''
    db.cursor.execute(query, [question_id, quiz_id])
    result = db.cursor.fetchone()
    db.close()
    return result

def index():
    
    if request.method == 'POST':
        session['username'] = request.form.get('name', 'Игрок')

    quizes = db.show('quiz')
    
    return render_template('start.html', quizes=quizes, username=session.get('username', 'Гость'))

def test():
    if 'counter' not in session:
        session['counter'] = 0
        
    if 'quiz_id' in request.args:
        session['quiz'] = int(request.args.get('quiz_id'))
        session['last_question'] = 0
        session['counter'] = 0
    
    if 'quiz' not in session:
        return redirect(url_for('index'))
    
    result = get_question_after(session['last_question'], session['quiz'])
    
    if result is None:
        return redirect(url_for('result'))
    
    
    question_id = result[0]
    question_text = result[1]
    answer = result[2]
    wrong1 = result[3]
    wrong2 = result[4]
    wrong3 = result[5]
    
    session['last_question'] = question_id
    session['counter'] += 1
    
  
    variants = [answer, wrong1, wrong2, wrong3]
    
    
    return render_template('test.html', 
                           q_num=session['counter'], 
                           q_text=question_text, 
                           variants=variants)

def result():

    session['counter'] = 0
    return render_template('result.html')

def counter():
    if 'counter' not in session:
        session['counter'] = 0
    session['counter'] += 1
    return '<h1>' + str(session['counter']) + '</h1>'


app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/test', 'test', test, methods=['GET'])
app.add_url_rule('/result', 'result', result, methods=['GET'])

if __name__ == "__main__":
    app.run(host=('0.0.0.0'))