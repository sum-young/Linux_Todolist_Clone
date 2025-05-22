from flask import Flask, render_template, request, redirect, url_for
todolist = Flask(__name__)


@todolist.route('/')
def page():
    return render_template("testcal.html")

if __name__ == '__main__':
    todolist.run(host='127.0.0.1', port=5500)