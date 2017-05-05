from app import *
from app.apis.post import *
from app.apis.get import *



@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
