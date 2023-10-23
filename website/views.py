from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask import flash
from . import db
from .models import Note
from . import views
# import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'], endpoint='home', strict_slashes=False)
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            return redirect(url_for('views.home')) 
            

    return render_template("home.html", user=current_user)


@views.route('/delete-note/<int:note_id>', methods=['GET'])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='success')
        else:
            flash("You don't have permission to delete this note.", category='error')
    else:
        flash('Note not found.', category='error')
    
    return redirect(url_for('views.home'))