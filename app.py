import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker = db.Column(db.String(100), nullable=False)
    project = db.Column(db.String(100), nullable=False)
    activity = db.Column(db.String(80), unique=True, nullable=False)
    hours = db.Column(db.Integer)
    date = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<{self.id} {self.worker} {self.project} {self.activity} {self.hours} {self.date} {self.created_at}>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-new-record', methods=('GET', 'POST'))
def add_new_record():
    if request.method == 'POST':
        worker = request.form['worker']
        project = request.form['project']
        activity = request.form['activity']
        hours = request.form['hours']
        date = request.form['date']
        record = Operation(worker=worker, project=project, activity=activity, hours=hours, date=date)
        db.session.add(record)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/report')
def report():
    return render_template('report.html')


@app.route('/worker-report', methods=('GET', 'POST'))
def worker_report():
    if request.method == 'POST':
        all_query = Operation.query.all()
        month = request.form['monthrange']
        worker_searched = request.form['worker']

        results = []
        if worker_searched is not None:
            for i in all_query:
                if worker_searched == i.worker and month[5:] == i.date[5:7]:
                    results.append(i)
        return render_template('report_table.html', results=results)
    return render_template('worker_report.html')


@app.route('/activity-report', methods=('GET', 'POST'))
def activity_report():
    if request.method == 'POST':
        all_query = Operation.query.all()
        month = request.form['monthrange']
        activity_searched = request.form['activity']

        results = []
        if activity_searched is not None:
            for i in all_query:
                if activity_searched == i.activity and month[5:] == i.date[5:7]:
                    results.append(i)
        return render_template('report_table.html', results=results)
    return render_template('activity_report.html')


@app.route('/project-report', methods=('GET', 'POST'))
def project_report():
    if request.method == 'POST':
        all_query = Operation.query.all()
        month = request.form['monthrange']
        project_searched = request.form['project']

        results = []
        if project_searched is not None:
            for i in all_query:
                if project_searched == i.activity and month[5:] == i.date[5:7]:
                    results.append(i)
        return render_template('report_table.html', results=results)
    return render_template('project_report.html')


@app.route('/all-records')
def all_records():
    all_query = Operation.query.all()
    return render_template('report_table.html', results=all_query)


if __name__ == '__main__':
    app.run()
