from flask import Flask,render_template,request

app=Flask(__name__)

@app.route('/')
def home():

 return render_template('home.html')

@app.route('/summary',methods=['POST'])

def summary():
  if request.method=='POST':
   summarize=request.form['message']
   return render_template('summary.html',res= summarize)
   
if __name__=="__main__":
  app.run(debug=True)

