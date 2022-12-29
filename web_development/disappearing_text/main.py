import time,threading,datetime, keyboard
from flask import Flask, render_template
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)
status = 100
style = 'text-input'
extra_style = ''
timer_start = True
year = datetime.date.today().year

@app.context_processor
def manage_content():
    return {'status': status,'style': style,'extra_style':extra_style} 

@app.route('/')
def index():
    return render_template('index.html',year=year)

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_timebar).start()
    threading.Thread(target=check_key_press).start()

def check_key_press():
    global status
    global extra_style
    with app.app_context():
        while timer_start:
            key = keyboard.read_key()
            if key:
                status = 100
                extra_style = ''
                turbo.push(turbo.replace(render_template('timebar.html'), 'timebar'))

def update_timebar():
    global status
    if keyboard.read_event():
        status -= 10
        timer_start = True

    with app.app_context():
        global extra_style
        
        while timer_start:
            status -= 10
            if status < 30:
                extra_style = 'bg-danger'
            if status < 0:
                status = 100
                extra_style = ''
                turbo.push(turbo.replace(render_template('textarea.html'), 'textarea'))
    
            time.sleep(1)
            turbo.push(turbo.replace(render_template('timebar.html'), 'timebar'))

if __name__ == '__main__':
    app.run(debug=True)
