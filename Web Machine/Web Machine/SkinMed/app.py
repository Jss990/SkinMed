from flask import Flask, render_template, redirect, url_for

from routes.Login.login import login_bp
from routes.redirections import redirections_bp

app = Flask(__name__)

app.secret_key = 'holalolaolaola'

app.register_blueprint(login_bp)
app.register_blueprint(redirections_bp)


@app.route('/')
def index():

    return redirect(url_for('Redirections.loginn'))

if __name__ == '__main__':

    app.run(debug=True)