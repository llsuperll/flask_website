from flask import Blueprint, render_template, request, flash, jsonify, redirect, abort
from flask_login import login_required, current_user
from data.notes import Note
from data import db_session
from forms.news import NewsForm
from data.news import News
import json
import os
from geocode import get_ll_spn, get_map

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
        if note.user_id == current_user.id:
            db_sess.delete(note)
            db_sess.commit()
    return jsonify({})


@view.route("/news")
@login_required
def news_check():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != 1))
    else:
        news = db_sess.query(News).filter(News.is_private != 1)
    return render_template("news.html", news=news, user=current_user)


@view.route("/news-add", methods=["GET", "POST"])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/news')
    return render_template('news_action.html', title='Добавление новости',
                           form=form, user=current_user, act="Add news")


@view.route('/edit-news/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == news_id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == news_id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/news')
        else:
            abort(404)
    return render_template('news_action.html',
                           title='Редактирование новости',
                           form=form, user=current_user, act="Edit news"
                           )


@view.route('/news_delete/<int:news_id>', methods=['GET', 'POST'])
@login_required
def news_delete(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == news_id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/news')


@view.route('/maps', methods=['GET', 'POST'])
@login_required
def maps():
    try:
        os.remove("static/img/map.png")
    except OSError:
        pass
    address = "адрес/место"
    if request.method == "POST":
        try:
            address = request.form.get("address")
            ll, spn = get_ll_spn(address)
            ll_spn = f"ll={ll}&spn={spn}"
            point_param = f"pt={ll}"
            get_map(ll_spn, "map", add_params=point_param)
        except Exception:
            redirect("/maps")
            flash("Неверные данные", category="error")
    return render_template("ya_maps.html", user=current_user, place=address)
