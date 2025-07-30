from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from app.models import Record
from app import db
from app.utils import json_validation

import json

bp = Blueprint('main', __name__)

@bp.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No selected file')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and file.filename.endswith('.json'):
            try:
                data = json.load(file)
                if not isinstance(data, list):
                    flash('JSON file should contain an array of objects')
                    return redirect(request.url)
                
                errors = json_validation(data)
                
                if errors:
                    for error in errors:
                        flash(error)
                    return redirect(request.url)
                
                for item in data:
                    record = Record(
                        name = item['name'],
                        date = datetime.strptime(item['date'], '%Y-%m-%d_%H:%M')
                    )
                    db.session.add(record)
                db.session.commit()
                flash('Data successfully uploaded to db')
                return redirect(url_for('main.records'))
            
            except json.JSONDecodeError:
                flash('Invalid JSON file')
                return redirect(request.url)

    return render_template('index.html')

@bp.route('/records')
def records():
    records = Record.query.all()
    return render_template('records.html', records=records)

@bp.route('/api/records')
def api_records():
    records = Record.query.order_by(Record.date.desc()).all()
    records_data = [{
        'name': record.name,
        'date': record.date.strftime('%Y-%m-%d %H:%M')
    } for record in records]
    return jsonify(records_data)