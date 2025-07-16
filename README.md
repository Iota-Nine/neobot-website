# 🧠 NeoBot - AI Discord Bot with Premium System

Un bot Discord intelligent avec système de paiement premium intégré et interface web unifiée.

## 🚀 Fonctionnalités

### 🤖 Bot Discord
- **IA Conversationnelle** : Réponses intelligentes et contextuelles
- **Mémoire Émotionnelle** : Système de mémoire avancé
- **Personas Multiples** : Différents styles de personnalité
- **Modération Automatique** : Système de modération intelligent
- **Statistiques** : Suivi des interactions utilisateur

### 💎 Système Premium
- **Authentification Discord** : Connexion sécurisée OAuth2
- **Plans d'abonnement** : Basic, Pro, Ultimate
- **Paiements PayPal** : Intégration complète
- **Dashboard utilisateur** : Gestion des abonnements
- **Interface admin** : Gestion complète

### 🎮 Interface Web Unifiée
- **Console temps réel** : Monitoring des utilisateurs et logs
- **Design moderne** : Interface sombre et élégante
- **Navigation fluide** : Entre console et système premium
- **Responsive** : Compatible mobile et desktop

## 📁 Structure du Projet

```
📁 NeoBot/
├── 🤖 bot.py                    # Bot Discord principal
├── 🎮 hud.html                  # Interface console
├── 🌐 unified_web_server.py     # Serveur web unifié
├── 📁 payement/                 # Système premium
│   ├── 💎 premium_system.py     # Application Flask
│   ├── 🎨 templates/            # Templates HTML
│   └── 📊 static/               # Fichiers statiques
├── 📁 users/                    # Données utilisateurs
├── 📁 logs/                     # Fichiers de logs
├── 🔧 config.json               # Configuration
├── 🚀 start_unified_system.bat  # Script de démarrage
└── 📖 README_UNIFIED_SYSTEM.md  # Documentation détaillée
```

## ⚡ Démarrage Rapide

### 1. Prérequis
- Python 3.8+
- Compte Discord Developer
- Compte PayPal Business (pour les paiements)

### 2. Installation
```bash
# Cloner le repository
git clone https://github.com/votre-username/neobot.git
cd neobot

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration
1. **Copier le fichier de configuration** :
   ```bash
   cp config.example.json config.json
   ```

2. **Configurer les credentials** dans `config.json` :
   - Discord Client ID et Secret
   - PayPal Client ID et Secret
   - Clé secrète Flask

3. **Configurer le bot Discord** :
   - Créer une application sur Discord Developer Portal
   - Ajouter les permissions nécessaires
   - Configurer les intents

### 4. Démarrage
```bash
# Option 1: Script batch (Windows)
start_unified_system.bat

# Option 2: Python direct
python unified_web_server.py
```

## 🌐 URLs

- **Console NeoBot** : `http://localhost:5000`
- **Système Premium** : `http://localhost:5000/premium`
- **Dashboard Admin** : `http://localhost:5000/premium/admin`

## 🎯 Plans d'Abonnement

| Plan | Prix | Fonctionnalités |
|------|------|-----------------|
| **Basic** | 2.99€/mois | Plus de tokens, mémoire étendue |
| **Pro** | 6.99€/mois | 1 personnage illimité, support prioritaire |
| **Ultimate** | 14.99€/mois | Tous les personnages, support 24/7 |

## 🔧 Configuration Avancée

### Variables d'environnement
```bash
# Discord
DISCORD_CLIENT_ID=your_client_id
DISCORD_CLIENT_SECRET=your_client_secret

# PayPal
PAYPAL_CLIENT_ID=your_paypal_id
PAYPAL_CLIENT_SECRET=your_paypal_secret

# Flask
SECRET_KEY=your_secret_key
```

### Base de données
Le système utilise SQLite par défaut. Pour la production :
```python
# PostgreSQL
DATABASE_URL=postgresql://user:pass@localhost/neobot
```

## 🚀 Déploiement

### Heroku
```bash
# Procfile
web: python unified_web_server.py

# requirements.txt
Flask==2.3.3
flask-sqlalchemy==3.0.5
requests==2.31.0
paypalrestsdk==1.13.1
```

### Railway/Render
- Connectez votre repository GitHub
- Configurez les variables d'environnement
- Déployez automatiquement

### VPS
```bash
# Installer les dépendances
sudo apt update
sudo apt install python3 python3-pip nginx

# Configurer Nginx
sudo nano /etc/nginx/sites-available/neobot
```

## 🔒 Sécurité

- ✅ **HTTPS obligatoire** en production
- ✅ **Variables d'environnement** pour les secrets
- ✅ **Validation PayPal** des paiements
- ✅ **Authentification Discord** sécurisée
- ✅ **Protection CSRF** activée

## 📊 Monitoring

- 📈 **Logs temps réel** dans la console
- 👥 **Statistiques utilisateurs** automatiques
- 💳 **Suivi des paiements** dans l'admin
- ⏰ **Notifications** d'expiration d'abonnement

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- 📧 **Email** : support@neobot.com
- 💬 **Discord** : [Serveur NeoBot](https://discord.gg/neobot)
- 📖 **Documentation** : [Wiki](https://github.com/votre-username/neobot/wiki)

---

**🎯 Système complet prêt pour la production !**

⭐ **N'oubliez pas de mettre une étoile si ce projet vous plaît !** 