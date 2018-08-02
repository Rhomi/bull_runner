#app.py

from flask import Flask, jsonify, request #import main Flask class and request object

app = Flask(__name__) #create the Flask app

@app.route('/query-example')
def query_example():
	# usage 1: our application will continue to run if the language key doesn't exist in the URL.
	#request.args.get('language')
	# usage 2: the app will return a 400 error if language key doesn't exist in the URL.
	#request.args['language']
	# I recommend using request.args.get() because of how easy it is for the user to modify the URL.
	language = request.args.get('language') #if key doesn't exist, returns None
	# In the second usage, it returns a 400, bad request.
	return('The language value is: {}'.format(language))

@app.route('/form-example', methods=['GET', 'POST']) # allow both get and post
def form_example():
	if request.method == 'POST': #this block is only entered when the form is submitted
		language = request.form.get('language')
		framework = request.form['framework']
		return('''<h1>The language value is: {}</h1>
			<h1>The framework value is: {}</h1>'''.format(language, framework))

	return '''<form method="POST">
	              Language: <input type="text" name="language"><br>
	              Framework: <input type="text" name="framework"><br>
	              <input type="submit" value="Submit"><br>
	          </form>'''

@app.route('/json-example', methods=['POST'])
def json_example():
    req_data = request.get_json()
    print(req_data)
    if 'and' in req_data: # gotta improve this logic

	    split_point = query.index('and')
	    
	    route = req_data[:split_point]
	    stop = req_data[split_point+1:]
	    print(jsonify(route=route, stop = stop))
	    return(jsonify(route=route, stop = stop))

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000