import os
import json
import sqlite3
import requests
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import paypalrestsdk
from discord_oauth import DiscordOAuth2Session
import threading
import time

app = Flask(__name__)
app.secret_key = 'votre_secret_key_ici'  # Changez ceci en production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///premium_subscriptions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration Discord OAuth2
DISCORD_CLIENT_ID = "votre_discord_client_id"
DISCORD_CLIENT_SECRET = "votre_discord_client_secret"
DISCORD_REDIRECT_URI = "http://localhost:5000/callback"

# Configuration PayPal
paypalrestsdk.configure({
    "mode": "sandbox",  # Changez en "live" pour la production
    "client_id": "votre_paypal_client_id",
    "client_secret": "votre_paypal_client_secret"
})

db = SQLAlchemy(app)

# Modèles de base de données
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    avatar = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    subscription = db.relationship('Subscription', backref='user', uselist=False)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_type = db.Column(db.String(50), nullable=False)  # 'monthly', 'yearly'
    status = db.Column(db.String(20), default='active')  # 'active', 'cancelled', 'expired'
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    paypal_payment_id = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    paypal_payment_id = db.Column(db.String(100), unique=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Subscription Plans
SUBSCRIPTION_PLANS = {
    'basic_monthly': {
        'name': 'Basic',
        'price': 2.99,
        'duration_days': 30,
        'savings': 0,
        'features': [
            'More tokens and conversations',
            'Extended memory (100 messages)',
            'Email support',
            'Limited character access'
        ]
    },
    'basic_yearly': {
        'name': 'Basic Annual',
        'price': 29.99,
        'duration_days': 365,
        'savings': 17,
        'features': [
            'More tokens and conversations',
            'Extended memory (100 messages)',
            'Email support',
            'Limited character access',
            '2 months free'
        ]
    },
    'pro_monthly': {
        'name': 'Pro',
        'price': 6.99,
        'duration_days': 30,
        'savings': 0,
        'features': [
            'One character unlimited',
            'Extended memory (200 messages)',
            'Priority support',
            'Advanced features',
            'Advanced customization'
        ]
    },
    'pro_yearly': {
        'name': 'Pro Annual',
        'price': 69.99,
        'duration_days': 365,
        'savings': 17,
        'features': [
            'One character unlimited',
            'Extended memory (200 messages)',
            'Priority support',
            'Advanced features',
            'Advanced customization',
            '2 months free'
        ]
    },
    'ultimate_monthly': {
        'name': 'Ultimate',
        'price': 14.99,
        'duration_days': 30,
        'savings': 0,
        'features': [
            'All characters unlocked',
            'Extended memory (500 messages)',
            '24/7 priority support',
            'Premium features',
            'Complete customization',
            'Early access to new features'
        ]
    },
    'ultimate_yearly': {
        'name': 'Ultimate Annual',
        'price': 149.99,
        'duration_days': 365,
        'savings': 17,
        'features': [
            'All characters unlocked',
            'Extended memory (500 messages)',
            '24/7 priority support',
            'Premium features',
            'Complete customization',
            'Early access to new features',
            '2 months free'
        ]
    }
}

# Configuration Discord OAuth2
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"  # Supprimez en production

def token_updater(token):
    session["oauth2_token"] = token

def make_discord_session(token=None, state=None, scope=None):
    return DiscordOAuth2Session(
        DISCORD_CLIENT_ID,
        redirect_uri=DISCORD_REDIRECT_URI,
        token=token,
        state=state,
        scope=scope
    )

@app.route('/')
def index():
    return render_template('index.html', plans=SUBSCRIPTION_PLANS)

@app.route('/premium')
def premium_page():
    return render_template('premium_page.html', plans=SUBSCRIPTION_PLANS)

@app.route('/login')
def login():
    discord = make_discord_session(scope=["identify", "email"])
    authorization_url, state = discord.create_authorization_url()
    session["oauth2_state"] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    discord = make_discord_session(state=session.get("oauth2_state"))
    token = discord.fetch_token(
        "https://discord.com/api/oauth2/token",
        client_secret=DISCORD_CLIENT_SECRET,
        authorization_response=request.url
    )
    session["oauth2_token"] = token
    
    # Récupérer les informations utilisateur
    discord_user = discord.fetch_user()
    
    # Vérifier si l'utilisateur existe déjà
    user = User.query.filter_by(discord_id=str(discord_user.id)).first()
    if not user:
        user = User(
            discord_id=str(discord_user.id),
            username=discord_user.username,
            email=discord_user.email,
            avatar=discord_user.avatar
        )
        db.session.add(user)
        db.session.commit()
    
    session['user_id'] = user.id
    session['discord_id'] = user.discord_id
    session['username'] = user.username
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    subscription = user.subscription if user else None
    
    return render_template('dashboard.html', 
                         user=user, 
                         subscription=subscription,
                         plans=SUBSCRIPTION_PLANS,
                         now=datetime.utcnow())

@app.route('/subscribe/<plan_type>')
def subscribe(plan_type):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if plan_type not in SUBSCRIPTION_PLANS:
        flash('Plan invalide', 'error')
        return redirect(url_for('dashboard'))
    
    plan = SUBSCRIPTION_PLANS[plan_type]
    
    # Créer le paiement PayPal
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": url_for('payment_success', _external=True),
            "cancel_url": url_for('payment_cancel', _external=True)
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": plan['name'],
                    "sku": f"premium_{plan_type}",
                    "price": str(plan['price']),
                    "currency": "EUR",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(plan['price']),
                "currency": "EUR"
            },
            "description": f"Abonnement NeoBot Premium - {plan['name']}"
        }]
    })
    
    if payment.create():
        # Sauvegarder le paiement en base
        db_payment = Payment(
            user_id=session['user_id'],
            paypal_payment_id=payment.id,
            amount=plan['price']
        )
        db.session.add(db_payment)
        db.session.commit()
        
        # Rediriger vers PayPal
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        flash('Erreur lors de la création du paiement', 'error')
        return redirect(url_for('dashboard'))

@app.route('/payment/success')
def payment_success():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    
    if not payment_id or not payer_id:
        flash('Paramètres de paiement manquants', 'error')
        return redirect(url_for('dashboard'))
    
    # Récupérer le paiement en base
    db_payment = Payment.query.filter_by(paypal_payment_id=payment_id).first()
    if not db_payment:
        flash('Paiement non trouvé', 'error')
        return redirect(url_for('dashboard'))
    
    # Exécuter le paiement
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # Mettre à jour le statut du paiement
        db_payment.status = 'completed'
        db.session.commit()
        
        # Créer ou mettre à jour l'abonnement
        user = User.query.get(db_payment.user_id)
        
        # Déterminer le plan basé sur le montant
        if db_payment.amount == 2.99:
            plan_type = 'basic_monthly'
        elif db_payment.amount == 29.99:
            plan_type = 'basic_yearly'
        elif db_payment.amount == 6.99:
            plan_type = 'pro_monthly'
        elif db_payment.amount == 69.99:
            plan_type = 'pro_yearly'
        elif db_payment.amount == 14.99:
            plan_type = 'ultimate_monthly'
        elif db_payment.amount == 149.99:
            plan_type = 'ultimate_yearly'
        else:
            plan_type = 'basic_monthly'  # Plan par défaut
        
        plan = SUBSCRIPTION_PLANS[plan_type]
        
        # Vérifier si l'utilisateur a déjà un abonnement
        subscription = user.subscription
        if subscription:
            # Étendre l'abonnement existant
            if subscription.end_date and subscription.end_date > datetime.utcnow():
                subscription.end_date += timedelta(days=plan['duration_days'])
            else:
                subscription.end_date = datetime.utcnow() + timedelta(days=plan['duration_days'])
        else:
            # Créer un nouvel abonnement
            subscription = Subscription(
                user_id=user.id,
                plan_type=plan_type,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=plan['duration_days']),
                paypal_payment_id=payment_id,
                amount=db_payment.amount
            )
            db.session.add(subscription)
        
        db.session.commit()
        
        flash('Paiement réussi ! Votre abonnement premium est maintenant actif.', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Erreur lors de l\'exécution du paiement', 'error')
        return redirect(url_for('dashboard'))

@app.route('/payment/cancel')
def payment_cancel():
    flash('Paiement annulé', 'info')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# API pour vérifier le statut premium d'un utilisateur Discord
@app.route('/api/premium/<discord_id>')
def check_premium_status(discord_id):
    user = User.query.filter_by(discord_id=discord_id).first()
    if not user or not user.subscription:
        return jsonify({'premium': False, 'message': 'Aucun abonnement trouvé'})
    
    subscription = user.subscription
    if subscription.status == 'active' and subscription.end_date > datetime.utcnow():
        return jsonify({
            'premium': True,
            'plan_type': subscription.plan_type,
            'end_date': subscription.end_date.isoformat(),
            'features': SUBSCRIPTION_PLANS[subscription.plan_type]['features']
        })
    else:
        return jsonify({'premium': False, 'message': 'Abonnement expiré'})

# Interface d'administration
@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or str(user.discord_id) not in ['votre_discord_id_admin']:  # Remplacez par votre ID Discord
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    subscriptions = Subscription.query.all()
    payments = Payment.query.all()
    
    return render_template('admin.html', 
                         users=users, 
                         subscriptions=subscriptions, 
                         payments=payments)

# Fonction pour nettoyer les abonnements expirés
def cleanup_expired_subscriptions():
    while True:
        try:
            with app.app_context():
                expired_subscriptions = Subscription.query.filter(
                    Subscription.end_date < datetime.utcnow(),
                    Subscription.status == 'active'
                ).all()
                
                for subscription in expired_subscriptions:
                    subscription.status = 'expired'
                
                db.session.commit()
                print(f"Nettoyage terminé: {len(expired_subscriptions)} abonnements expirés")
                
        except Exception as e:
            print(f"Erreur lors du nettoyage: {e}")
        
        time.sleep(3600)  # Vérifier toutes les heures

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Démarrer le thread de nettoyage
    cleanup_thread = threading.Thread(target=cleanup_expired_subscriptions, daemon=True)
    cleanup_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
