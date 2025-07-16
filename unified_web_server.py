import os
import sys
from flask import Flask, render_template_string, send_from_directory, redirect, url_for
import threading
import time

# Ajouter le dossier payement au path
sys.path.append('payement')

# Importer le système premium
from payement.premium_system import app as premium_app

# Créer l'application principale
app = Flask(__name__)
app.secret_key = 'votre_secret_key_ici'

# Lire le contenu du hud.html
with open('hud.html', 'r', encoding='utf-8') as f:
    hud_content = f.read()

@app.route('/')
def index():
    """Page principale - Console NeoBot"""
    return hud_content

@app.route('/premium')
def premium():
    """Rediriger vers le système premium"""
    return redirect('/premium/')

# Monter l'application premium sur /premium/
app.register_blueprint(premium_app, url_prefix='/premium')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Servir les fichiers statiques"""
    return send_from_directory('payement/static', filename)

@app.route('/favicon.ico')
def favicon():
    """Favicon"""
    return '', 204

if __name__ == '__main__':
    print("🚀 Démarrage du serveur web unifié NeoBot...")
    print("📊 Console: http://localhost:5000")
    print("💎 Premium: http://localhost:5000/premium")
    print("🔧 Admin: http://localhost:5000/premium/admin")
    print("\n" + "="*50)
    
    # Démarrer le serveur
    app.run(host='0.0.0.0', port=5000, debug=True) 