from flask import Flask, render_template, request, redirect, url_for
from models import db, Note

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)


@app.route('/')
def home():
    notes = Note.query.all()
    return render_template('index.html', notes=notes)


@app.route('/note/<int:note_id>')
def note_detail(note_id):
    note = Note.query.get(note_id)
    return render_template('note_detail.html', note=note)


@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        new_note = Note(title=title, content=content, category=category)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_note.html')


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get(note_id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        note.category = request.form['category']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_note.html', note=note)


@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    note = Note.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
