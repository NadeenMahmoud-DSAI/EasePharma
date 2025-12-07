from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1 style="color: red; font-size: 50px;">IT WORKS!</h1>'

if __name__ == '__main__':
    print("--- SERVER STARTED ON PORT 6000 ---")
    app.run(port=6000)