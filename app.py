from flask import Flask, render_template,url_for,request,redirect

from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	content = db.Column(db.String(200),nullable=False)
	date_created = db.Column(db.DateTime,default=datetime.utcnow)

	def __repr__(self):
		return '<Assignment %r>' % self.id

	

@app.route('/',methods=['POST','GET'])
def index():
	if request.method == 'POST':
		assign_content = request.form['content']
		new_assign = Todo(content=assign_content)
		try:
			db.session.add(new_assign)
			db.session.commit()
			return redirect('/')
		except:
			return 'There was an issue adding the assignmnet'	
	else:
		assignments = Todo.query.order_by(Todo.date_created).all()	
		return render_template('index.html',assignments=assignments)



@app.route('/delete/<int:id>')
def delete(id):
	assignment_to_delete = Todo.query.get_or_404(id)

	try:
		db.session.delete(assignment_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return 'There was an issue in deleting the assignment'


if __name__ == '__main__':
		app.run(debug=True)	