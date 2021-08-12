from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livro.sqlite3'
db = SQLAlchemy(app)

class Livro(db.Model):
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   titulo = db.Column(db.String(150), nullable=False)
   autor = db.Column(db.String(150), nullable=False)
   capa = db.Column(db.String(300), nullable=False)
   sinopse = db.Column(db.String(900), nullable=False)
   link = db.Column(db.String(500), nullable=False)

   def __init__(self, titulo, autor, capa, sinopse, link):
      self.titulo = titulo
      self.autor = autor
      self.capa = capa
      self.sinopse = sinopse
      self.link = link

@app.route('/')
def index():
   livros = Livro.query.all()
   return render_template('index.html', livros=livros)

@app.route('/contato')
def contato():
   return render_template('contato.html')   

@app.route('/<id>')
def livro_pelo_id(id):
   livro = Livro.query.get(id)
   return render_template('index.html', livro=livro)

@app.route('/new', methods=['GET', 'POST'])
def new():
   if request.method == 'POST':
      livro = Livro(
         request.form['titulo'],
         request.form['autor'],
         request.form['capa'],
         request.form['sinopse'],
         request.form['link']
      )
      db.session.add(livro)
      db.session.commit()
      return redirect('/#playlist')
   return render_template('new.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
   livro = Livro.query.get(id)
   if request.method == "POST":
      livro.titulo = request.form['titulo']
      livro.autor = request.form['autor']
      livro.capa = request.form['capa']
      livro.sinopse = request.form['sinopse']
      livro.link = request.form['link']
      db.session.commit()
      return redirect('/#playlist')
   return render_template('edit.html', livro=livro)

@app.route('/delete/<id>')
def delete(id):
   livro = Livro.query.get(id)
   db.session.delete(livro)
   db.session.commit()
   return redirect('/#playlist')

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    livro = Livro.query.filter_by(titulo=request.form['search']).all()
    return render_template('index.html', livro=livro)   

if __name__ == '__main__':
   db.create_all()
   app.run(debug=True, port=3000)