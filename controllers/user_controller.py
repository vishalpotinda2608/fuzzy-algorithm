from main import app


@app.route('/user')
def hello_home():
   return 'user Controller'
