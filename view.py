from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from data.notes import Note
from data import db_session
import json

view = Blueprint("view", __name__)


@view.route("/", methods=["GET", "POST"])
@login_required
def homepage():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 3:
            flash("Заметка слишком короткая")
        else:
            new_note = Note()
            new_note.data = note
            new_note.user_id = current_user.id
            db_sess = db_session.create_session()
            db_sess.add(new_note)
            db_sess.commit()
            flash("Заметка успешно добавлена!", category="success")
    return render_template("home.html", user=current_user)


@view.route("/delete-note", methods=["POST"])
def delete_note():
    data = json.loads(request.data)
    note_id = data["noteId"]
    db_sess = db_session.create_session()
    note = db_sess.query(Note).get(note_id)
    if note:
        print(1)
        if note.user_id == current_user.id:
            db_sess.delete(note)
            db_sess.commit()
    return jsonify({})
