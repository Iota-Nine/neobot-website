# 💳 Système de Paiement NeoBot Premium

## 🚀 Démarrage Rapide

1. **Double-cliquez sur `start.bat`** pour démarrer le système
2. **Ouvrez votre navigateur** sur `http://localhost:5000`
3. **Configurez les clés** dans `premium_config.json` avant utilisation

## 📁 Structure des Fichiers

```
payement/
├── start.bat                    # Script de démarrage principal
├── premium_system.py            # Serveur web Flask
├── premium_integration.py       # Intégration avec le bot Discord
├── premium_config.json          # Configuration du système
├── requirements_premium.txt     # Dépendances Python
├── README.md                   # Ce fichier
├── README_PREMIUM_SYSTEM.md    # Documentation complète
└── templates/                  # Templates HTML
    ├── index.html              # Page d'accueil
    ├── dashboard.html          # Tableau de bord utilisateur
    └── admin.html             # Interface d'administration
```

## ⚙️ Configuration

### 1. Discord OAuth2
1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Créez une nouvelle application
3. Dans "OAuth2" > "General", copiez Client ID et Client Secret
4. Dans "OAuth2" > "Redirects", ajoutez : `http://localhost:5000/callback`

### 2. PayPal Business
1. Créez un compte PayPal Business
2. Allez dans "Outils" > "API"
3. Créez une application pour obtenir Client ID et Secret
4. Utilisez les clés Sandbox pour les tests

### 3. Configuration du Système
Ouvrez `premium_config.json` et remplacez :
```json
{
    "discord": {
        "client_id": "VOTRE_DISCORD_CLIENT_ID",
        "client_secret": "VOTRE_DISCORD_CLIENT_SECRET"
    },
    "paypal": {
        "client_id": "VOTRE_PAYPAL_CLIENT_ID",
        "client_secret": "VOTRE_PAYPAL_CLIENT_SECRET"
    },
    "admin_users": ["VOTRE_DISCORD_ID"]
}
```

## 🎯 Fonctionnalités

### Pour les Utilisateurs
- ✅ Connexion sécurisée via Discord
- ✅ Choix d'abonnement (Mensuel/Annuel)
- ✅ Paiement sécurisé via PayPal
- ✅ Tableau de bord personnel
- ✅ Historique des paiements

### Pour l'Administrateur
- ✅ Interface d'administration complète
- ✅ Gestion des utilisateurs
- ✅ Gestion des abonnements
- ✅ Statistiques de revenus
- ✅ Historique des paiements

### Intégration Bot Discord
- ✅ Vérification automatique du statut premium
- ✅ Limitation des fonctionnalités selon l'abonnement
- ✅ Messages d'encouragement pour l'upgrade

## 💰 Plans d'Abonnement

| Plan | Prix | Mémoire | Fonctionnalités |
|------|------|---------|-----------------|
| **Mensuel** | 9.99€/mois | 200 messages | Accès illimité, Support prioritaire |
| **Annuel** | 99.99€/an | 500 messages | Accès illimité, Support prioritaire, 2 mois gratuits |

## 🔧 Utilisation

### Démarrage
```bash
# Option 1: Script automatique
start.bat

# Option 2: Manuel
pip install -r requirements_premium.txt
python premium_system.py
```

### Accès Web
- **Site principal** : http://localhost:5000
- **Administration** : http://localhost:5000/admin

### Intégration Bot
```python
from premium_integration import PremiumIntegration

premium = PremiumIntegration()
is_premium = premium.is_premium_user(str(message.author.id))
```

## 🛡️ Sécurité

- **OAuth2 Discord** pour l'authentification
- **PayPal** pour les paiements sécurisés
- **Validation** côté serveur
- **Sessions** sécurisées

## 📊 API

### Vérification Premium
```
GET /api/premium/{discord_id}
```

Réponse :
```json
{
    "premium": true,
    "plan_type": "monthly",
    "end_date": "2024-01-01T00:00:00",
    "features": ["Accès illimité..."]
}
```

## 🚨 Dépannage

### Erreur Python
- Installez Python 3.8+ depuis https://python.org
- Vérifiez que Python est dans le PATH

### Erreur Discord
- Vérifiez les clés OAuth2 dans `premium_config.json`
- Assurez-vous que l'URL de redirection est configurée

### Erreur PayPal
- Vérifiez les clés API PayPal
- Utilisez les clés Sandbox pour les tests

### Erreur Base de Données
- Le fichier `premium_subscriptions.db` sera créé automatiquement
- Vérifiez les permissions d'écriture

## 📞 Support

Pour toute question :
1. Consultez `README_PREMIUM_SYSTEM.md` pour la documentation complète
2. Vérifiez les logs du serveur
3. Contactez l'administrateur

---

**🎉 Le système est prêt à générer des revenus avec NeoBot !** 