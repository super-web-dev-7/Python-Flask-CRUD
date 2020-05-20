import logging.config
import os
from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import settings
import requests
import json

application = Flask(__name__)
Bootstrap(application)


def configure(app):
    app.config['SERVER_HOST'] = settings.SERVER_HOST
    app.config['SERVER_PORT'] = settings.SERVER_PORT
    app.config['API_URL'] = settings.API_URL


@application.route('/')
def home():
    response = requests.get(settings.API_URL + '/getSpeakers')
    print("______________________________________", response)
    speakers = response.json()
    return render_template("index.html", speakers=speakers)


@application.route('/add-speaker', methods=['GET'])
def add_speaker_page():
    return render_template("add_speaker.html")


@application.route('/edit-speaker/<id>', methods=['GET'])
def edit_speaker_page(id):
    response = requests.get(settings.API_URL + '/getSpeaker?id=' + id)
    speaker = response.json()
    return render_template("edit_speaker.html", speaker=speaker)


@application.route('/delete-speaker/<id>', methods=['GET'])
def delete_speaker_page(id):
    response = requests.get(settings.API_URL + '/getSpeaker?id=' + id)
    speaker = response.json()
    return render_template("delete_speaker.html", speaker=speaker)

@application.route('/view-speaker/<id>', methods=['GET'])
def view_speaker_page(id):
    response = requests.get(settings.API_URL + '/getSpeaker?id=' + id)
    speaker = response.json()
    return render_template("view_speaker.html", speaker=speaker)

@application.route('/speaker/new', methods=['POST'])
def add_speaker():
    # Get item from the POST body
    req_data = {
        'name': request.form['name'],
        'current_city': request.form['current_city'],
        'current_state': request.form['current_state'],
        'email': request.form['email'],
        'bio': request.form['bio'],
        'speaker_rate': request.form['speaker_rate']
    }
    response = requests.post(settings.API_URL + '/createSpeaker', json=json.dumps(req_data))
    return redirect(url_for('home'))

@application.route('/speaker/update/<id>', methods=['POST'])
def update_speaker(id):
    # Get item from the POST body
    req_data = {
        'name': request.form['name'],
        'current_city': request.form['current_city'],
        'current_state': request.form['current_state'],
        'email': request.form['email'],
        'bio': request.form['bio'],
        'speaker_rate': request.form['speaker_rate']
    }
    response = requests.put(settings.API_URL + '/updateSpeaker?id=' + id, json=json.dumps(req_data))
    return redirect(url_for('home'))

@application.route('/speaker/delete/<id>', methods=['POST'])
def delete_speaker(id):
    response = requests.delete(settings.API_URL + '/deleteSpeaker?id=' + id)
    if response.status_code == 200:
        return redirect(url_for('home'))


# running app
def main():
    configure(application)
    print(' ----->>>>  Application running in development server')
    application.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT, debug=settings.FLASK_DEBUG)


if __name__ == '__main__':
    main()
