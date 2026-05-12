import os
import requests
from flask import Flask, render_template_string, request, redirect

API_URL = os.environ.get("API_URL", "http://api:8080")
app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Node Registry</title></head>
<body>
    <h1>Node Registry</h1>

    <h2>Health</h2>
    <p>Status: {{ health.status }} | DB: {{ health.db }} | Active nodes: {{ health.nodes_count }}</p>

    <h2>Nodes</h2>
    <table border="1">
        <tr><th>Name</th><th>Host</th><th>Port</th><th>Status</th></tr>
        {% for node in nodes %}
        <tr><td>{{ node.name }}</td><td>{{ node.host }}</td><td>{{ node.port }}</td><td>{{ node.status }}</td></tr>
        {% endfor %}
    </table>

    <h2>Register Node</h2>
    <form method="post" action="/register">
        Name: <input name="name"> Host: <input name="host"> Port: <input name="port" value="8080">
        <input type="submit" value="Register">
    </form>

    <h2>Delete Node</h2>
    <form method="post" action="/delete">
        Name: <input name="name">
        <input type="submit" value="Delete">
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    health = requests.get(f"{API_URL}/health").json()
    nodes = requests.get(f"{API_URL}/api/nodes").json()
    return render_template_string(TEMPLATE, health=health, nodes=nodes)

@app.route("/register", methods=["POST"])
def register():
    requests.post(f"{API_URL}/api/nodes", json={
        "name": request.form["name"],
        "host": request.form["host"],
        "port": int(request.form["port"]),
    })
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    requests.delete(f"{API_URL}/api/nodes/{request.form['name']}")
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501)