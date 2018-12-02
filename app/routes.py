from app import app
from flask import render_template


@app.route('/')
@app.route('/index.html')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
