from urllib import request
import sqlite3
from flask import redirect,url_for,render_template,request,Flask

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "personal.db")


def connect_db():#连接数据库
    conn = sqlite3.connect(db_path)

    conn.row_factory = sqlite3.Row

    return conn

def init_db():#初始化数据库
    conn = connect_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')


    conn.commit()
    conn.close()

app = Flask(__name__)
DATABASE = 'personal.db'



@app.route('/',methods=["GET"])#主界面：按时间顺序显示所有已有的日志
def index():
    conn=connect_db()
    posts = conn.execute("SELECT * FROM posts ORDER BY created_at DESC").fetchall()
    return render_template('index.html', posts=posts)

@app.route("/create",methods=["GET","POST"])#创建新日志
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn = sqlite3.connect("personal.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts(title,content)"
                       " VALUES(?,?)",(title,content))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/view/<int:id>",methods=["GET","POST"])#查看单日志详情
def view(id):
    conn = connect_db()
    post=conn.execute("SELECT * FROM posts WHERE id=?",[id]).fetchone()
    conn.close()

    return render_template("view.html",post=post)




@app.route("/edit/<int:id>",methods=["GET","POST"])#编辑已有日志
def edit(id):
    conn = connect_db()
    post=conn.execute("SELECT * FROM posts WHERE id=?",(id,)).fetchone()
    if request.method == "POST":
        new_title = request.form["title"]
        new_content = request.form["content"]
        if post is None:
            pass
        else:
            conn.execute("UPDATE posts SET title=?, content=? WHERE id=?",(new_title,new_content,id)
                        )
            conn.commit()
            conn.close()
            return redirect(url_for("view",id=id))
    else:
        if post is None:
            pass
        else:
            return render_template("edit.html", post=post)




@app.route("/delete/<int:id>",methods=["POST"])#删除单日志
def delete(id):
    conn = connect_db()
    conn.execute("DELETE FROM posts WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.before_request
def initialize():
    init_db()



if __name__ == "__main__":
    app.run(debug=True)