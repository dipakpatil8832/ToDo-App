from flask import Flask, render_template, request, redirect
import json
from datetime import datetime

app = Flask(__name__)
FILE_NAME = "tasks.json"

def load_tasks():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return []

def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

@app.route("/")
def home():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        tasks = load_tasks()
        new_task = {
            "description": request.form["description"],
            "due_date": request.form["due_date"] if request.form["due_date"] else "N/A",
            "status": "Pending"
        }
        tasks.append(new_task)
        save_tasks(tasks)
        return redirect("/")
    return render_template("add.html")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    tasks = load_tasks()

    if query:
        filtered_tasks = [task for task in tasks if query in task["description"].lower()]
    else:
        filtered_tasks = tasks

    return render_template("index.html", tasks=filtered_tasks, search_query=query)

@app.route("/complete/<int:index>")
def complete_task(index):
    tasks = load_tasks()
    tasks[index]["status"] = "Completed"
    save_tasks(tasks)
    return redirect("/")

@app.route("/delete/<int:index>")
def delete_task(index):
    tasks = load_tasks()
    tasks.pop(index)
    save_tasks(tasks)
    return redirect("/")

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit_task(index):
    tasks = load_tasks()
    task = tasks[index]

    if request.method == "POST":
        task["description"] = request.form["description"]
        task["due_date"] = request.form["due_date"]
        save_tasks(tasks)
        return redirect("/")
    
    return render_template("edit.html", task=task, index=index)

if __name__ == "__main__":
    app.run(debug=True)
