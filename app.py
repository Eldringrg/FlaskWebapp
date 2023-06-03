from flask import Flask,render_template,request

from model2 import myfunc1

app=Flask(__name__)

@app.route('/')
def home():

 return render_template('home.html')

@app.route('/summary',methods=['POST'])

def summary():
  if request.method=='POST':
   summarize=request.form['message']
   res = myfunc1(summarize)
   return render_template('summary.html',res= res)
   
if __name__=="__main__":
  app.run(debug=True)

