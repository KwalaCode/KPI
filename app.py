from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import pandas as pd
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)

# Configuration de la base de données
DATABASE = 'kpi_logistiques.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/saisie', methods=['GET', 'POST'])
def saisie():
    if request.method == 'POST':
        date = request.form['date']
        temps_livraison = request.form['temps_livraison']
        taux_service = request.form['taux_service']
        niveau_stock = request.form['niveau_stock']
        
        db = get_db()
        db.execute('INSERT INTO kpi (date, temps_livraison, taux_service, niveau_stock) VALUES (?, ?, ?, ?)',
                   [date, temps_livraison, taux_service, niveau_stock])
        db.commit()
        return jsonify({"success": True})
    return render_template('saisie.html')

@app.route('/import', methods=['POST'])
def import_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        df = pd.read_csv(file)
        db = get_db()
        df.to_sql('kpi', db, if_exists='append', index=False)
        return jsonify({"success": True})

@app.route('/visualisation')
def visualisation():
    db = get_db()
    kpis = db.execute('SELECT * FROM kpi ORDER BY date').fetchall()
    return render_template('visualisation.html', kpis=kpis)

@app.route('/generer_rapport')
def generer_rapport():
    db = get_db()
    kpis = db.execute('SELECT * FROM kpi ORDER BY date').fetchall()
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Générer le contenu du PDF ici
    p.drawString(100, 750, "Rapport KPI Logistiques")
    y = 700
    for kpi in kpis:
        p.drawString(100, y, f"Date: {kpi['date']}, Temps de livraison: {kpi['temps_livraison']}, Taux de service: {kpi['taux_service']}, Niveau de stock: {kpi['niveau_stock']}")
        y -= 20
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='rapport_kpi.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

