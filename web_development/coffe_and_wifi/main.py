from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap
import pandas

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
form_values = {'Cafe Name':'','Image':'','Location':'','Open':'','Close':'','Coffee':'☕️','Wifi':'✘','Power':'✘'}
cafe_name = None
csv_data = None
csv_row_index = None

def read_csv(file,searched_detail = '', searched_value = ''):
    global csv_row_index
    data = pandas.read_csv(file)
    list_of_rows = []

    for row_index in range(0,len(data)):
        row = data.iloc[row_index]
        if searched_detail in row and searched_value == row[searched_detail]:
            csv_row_index = row_index
            return [row,data]
        
        list_of_rows.append(row)
    
    return list_of_rows

@app.route("/")
def home():
    return render_template("index.html",cafes=read_csv('cafe-data.csv'),values=form_values)

@app.route('/delete', methods=['GET','POST'])
def delete_from_databas():
    global csv_data
        
    df = csv_data
    df.set_index('Cafe Name', inplace=True)
    df_s = df.drop(cafe_name)
    df_s.to_csv('cafe-data.csv')

    return redirect(url_for('home'))

@app.route('/add_to_database', methods=['GET','POST'])
def add_to_database():
    df = pandas.DataFrame({'Cafe Name':request.form.get('name'),'Image':request.form.get('image-url'),
                           'Location':request.form.get('location-url'),'Open':request.form.get('open'),
                           'Close':request.form.get('close'),'Coffee':request.form.get('coffee-rating'),
                           'Wifi':request.form.get('wifi-rating'),'Power':request.form.get('power-rating'),
                           'Power':request.form.get('power-rating') }, index=[1])
    df.to_csv('cafe-data.csv',mode='a',header=False,index=False)

    return redirect(url_for('home'))

@app.route('/change_database', methods=['GET','POST'])
def change_database():
    global csv_data

    csv_data.loc[csv_row_index,'Cafe Name'] = request.form.get('name')
    csv_data.loc[csv_row_index,'Image'] = request.form.get('image-url')
    csv_data.loc[csv_row_index,'Location'] = request.form.get('location-url')
    csv_data.loc[csv_row_index,'Open'] = request.form.get('open')
    csv_data.loc[csv_row_index,'Close'] = request.form.get('close')
    csv_data.loc[csv_row_index,'Coffee'] = request.form.get('coffee-rating')
    csv_data.loc[csv_row_index,'Wifi'] = request.form.get('wifi-rating')
    csv_data.loc[csv_row_index,'Power'] = request.form.get('power-rating')
    
    csv_data.to_csv('cafe-data.csv', index=False)

    return redirect(url_for('home'))


def reset_form_values(name='',image='',location='',open='',close='',coffee='☕️',wifi='✘',power='✘'):
    form_values['Cafe Name'] = name
    form_values['Image'] = image
    form_values['Location'] = location
    form_values['Open'] = open
    form_values['Close'] = close
    form_values['Coffee'] = coffee
    form_values['Wifi'] = wifi
    form_values['Power'] = power

@app.route('/add_form', methods=['GET','POST'])
def add_form():
    reset_form_values()
    return render_template('add.html',submit_value='Add',submit_action='add_to_database', delete_status='disabled',values=form_values)

@app.route('/<cafe>/edit',methods=['GET', 'POST'])
def edit_form(cafe):
    global cafe_name
    global csv_data
    
    cafe_name = cafe
    csv_file = read_csv('cafe-data.csv',searched_detail='Cafe Name',searched_value=cafe_name)
    csv_row = csv_file[0]
    csv_data = csv_file[1]
    reset_form_values(name=csv_row['Cafe Name'],image=csv_row['Image'],location=csv_row['Location'],
                      open=csv_row['Open'],close=csv_row['Close'],coffee=csv_row['Coffee'],
                      wifi=csv_row['Wifi'],power=csv_row['Power'])

    return render_template('add.html', submit_value='Edit', submit_action='change_database', delete_status='',values=form_values)

if __name__ == '__main__':
    app.run(debug=True)
