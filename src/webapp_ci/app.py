import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# project root (two levels up)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# create a sqlalchemy object without binding it
db = SQLAlchemy()

# feedback model
class Feedback(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, 'templates'),
        static_folder=os.path.join(BASE_DIR, 'static')
    )
    # load default config
    app.config.from_object('webapp_ci.config')
    # override with testing config if provided
    if test_config:
        app.config.update(test_config)

    # bind db to this app
    db.init_app(app)
    # create tables
    with app.app_context():
        db.create_all()

    @app.route('/', methods=['GET'])
    def index():
        feedback = Feedback.query.all()
        return render_template('index.html', feedback=feedback)

    @app.route('/submit', methods=['POST'])
    def submit():
        comment = request.form.get('comment', '').strip()
        if comment:
            db.session.add(Feedback(comment=comment))
            db.session.commit()
        return redirect(url_for('index'))

    return app

# module‑level app for running & for pytest
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
