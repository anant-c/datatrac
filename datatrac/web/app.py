# web/app.py

from flask import Flask, request, redirect, url_for, send_file, render_template, jsonify
from pathlib import Path
import os

# Import database and manager logic from your core package
from datatrac.core.db import get_db, create_database_tables
from datatrac.core.manager import DataManager

app = Flask(__name__, static_folder="static", template_folder="templates")

# Ensure DB tables on start
with app.app_context():
    create_database_tables()

@app.route("/")
def home():
    """Home/dashboard: list datasets."""
    db = next(get_db())
    manager = DataManager(db)
    datasets = manager.find_all()
    return render_template("index.html", datasets=datasets)

@app.route("/upload", methods=["POST"])
def upload():
    """Upload a dataset file."""
    uploaded_file = request.files.get("file")
    source = request.form.get("source")
    name = uploaded_file.filename if uploaded_file else None
    # Save to a temp directory first
    save_path = Path("uploads") / name
    save_path.parent.mkdir(exist_ok=True)
    uploaded_file.save(str(save_path))
    db = next(get_db())
    manager = DataManager(db)
    dataset = manager.push_dataset(str(save_path), source)
    return redirect(url_for("home"))

@app.route("/download/<file_hash>")
def download(file_hash):
    """Download dataset by hash."""
    db = next(get_db())
    manager = DataManager(db)
    try:
        local_path = manager.download_dataset(file_hash, destination_dir="downloads")
        return send_file(local_path, as_attachment=True)
    except Exception as e:
        return str(e), 404

@app.route("/details/<file_hash>")
def details(file_hash):
    """Show dataset details (with edit link)."""
    db = next(get_db())
    manager = DataManager(db)
    dataset = manager.find_by_hash(file_hash)
    if not dataset:
        return "Not found", 404
    return render_template("details.html", dataset=dataset)

@app.route("/edit/<file_hash>", methods=["POST"])
def edit(file_hash):
    """Edit dataset metadata (name, source, etc)."""
    db = next(get_db())
    manager = DataManager(db)
    dataset = manager.find_by_hash(file_hash)
    if not dataset:
        return "Not found", 404
    # Update allowed fields
    dataset.name = request.form.get("name")
    dataset.source = request.form.get("source")
    db.commit()
    return redirect(url_for("details", file_hash=file_hash))

@app.route("/delete/<file_hash>", methods=["POST"])
def delete(file_hash):
    """Delete dataset."""
    db = next(get_db())
    manager = DataManager(db)
    success = manager.delete_dataset(file_hash)
    return redirect(url_for("home"))

@app.route("/lineage/<file_hash>")
def lineage(file_hash):
    """Show simple lineage visualization."""
    db = next(get_db())
    manager = DataManager(db)
    data = manager.get_lineage(file_hash)
    dataset = manager.find_by_hash(file_hash)
    return render_template("lineage.html", dataset=dataset, lineage=data)

if __name__ == "__main__":
    app.run(debug=True)
