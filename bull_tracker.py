#app.py

from flask import Flask, request #import main Flask class and request object
from flask_ask import Ask, statement
import backend

app = Flask(__name__) #create the Flask app

@app.route('/bull-tracker', methods=['GET', 'POST']) # allow both get and post
def form_example():
	if request.method == 'POST': #this block is only entered when the form is submitted
		route = request.form.get('route')
		stop = request.form['stop']
		#return('''<h1>The route value is: {}</h1>
		#	<h1>The stop value is: {}</h1>'''.format(route, stop))

		message = backend.process_request(route,stop)
		return('''<h3>{}</h3>'''.format(message))

	else:

		return '''<form method="POST">
		              Route: <input type="text" name="route"><br>
		              Stop: <input type="text" name="stop"><br>
		              <input type="submit" value="Submit"><br>
		          </form>'''

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000