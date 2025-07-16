# 🚀 Système Premium NeoBot

## 📋 Vue d'ensemble

Ce système permet de gérer les abonnements premium pour NeoBot avec :
- **Interface web moderne** pour les utilisateurs
- **Connexion Discord OAuth2** pour l'authentification
- **Paiements PayPal** sécurisés
- **Interface d'administration** complète
- **Intégration avec le bot Discord** existant

## 🛠️ Installation

### 1. Prérequis
- Python 3.8+
- Compte Discord Developer
- Compte PayPal Business

### 2. Installation des dépendances
```bash
pip install -r requirements_premium.txt
```

### 3. Configuration

#### Configuration Discord OAuth2
1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Créez une nouvelle application
3. Dans "OAuth2" > "General", notez le Client ID et Client Secret
4. Dans "OAuth2" > "Redirects", ajoutez : `http://localhost:5000/callback`

#### Configuration PayPal
1. Créez un compte PayPal Business
2. Allez dans "Outils" > "API"
3. Créez une application pour obtenir Client ID et Secret
4. En mode développement, utilisez les clés Sandbox

#### Configuration du système
1. Ouvrez `premium_config.json`
2. Remplacez toutes les valeurs `VOTRE_*` par vos vraies clés
3. Ajoutez votre ID Discord dans `admin_users`

## 🚀 Démarrage

### Option 1 : Script automatique
```bash
start_premium_system.bat
```

### Option 2 : Manuel
```bash
python premium_system.py
```

Le serveur sera accessible sur : `http://localhost:5000`

## 📱 Utilisation

### Pour les utilisateurs
1. **Accès au site** : `http://localhost:5000`
2. **Connexion Discord** : Cliquez sur "Se connecter avec Discord"
3. **Choix d'abonnement** : Mensuel (9.99€) ou Annuel (99.99€)
4. **Paiement PayPal** : Redirection automatique vers PayPal
5. **Activation** : L'abonnement est automatiquement activé

### Pour l'administrateur
1. **Accès admin** : `http://localhost:5000/admin`
2. **Gestion utilisateurs** : Voir tous les utilisateurs et leurs statuts
3. **Gestion abonnements** : Étendre, annuler les abonnements
4. **Suivi paiements** : Historique complet des transactions

## 🔧 Intégration avec le bot Discord

### 1. Import du module
```python
from premium_integration import PremiumIntegration

# Initialiser
premium = PremiumIntegration()
```

### 2. Vérification du statut premium
```python
# Dans votre fonction on_message
async def on_message(message):
    if message.author == client.user:
        return
    
    # Vérifier le statut premium
    is_premium = premium.is_premium_user(str(message.author.id))
    memory_limit = premium.get_memory_limit(str(message.author.id))
    
    # Vérifier l'accès au personnage
    persona_type = "LEWD"  # ou autre
    can_access = premium.can_access_persona(str(message.author.id), persona_type)
    
    if not can_access:
        premium_msg = premium.get_premium_message(str(message.author.id))
        await message.channel.send(premium_msg)
        return
    
    # Continuer le traitement normal...
```

### 3. Fonctionnalités disponibles
- `is_premium_user(discord_id)` : Vérifie si l'utilisateur est premium
- `get_memory_limit(discord_id)` : Retourne la limite de mémoire
- `can_access_persona(discord_id, persona_type)` : Vérifie l'accès au personnage
- `get_premium_message(discord_id)` : Message d'encouragement premium

## 💰 Plans d'abonnement

### Premium Mensuel (9.99€/mois)
- Accès illimité à tous les personnages
- Mémoire étendue (200 messages)
- Support prioritaire
- Fonctionnalités avancées

### Premium Annuel (99.99€/an)
- Accès illimité à tous les personnages
- Mémoire étendue (500 messages)
- Support prioritaire
- Fonctionnalités avancées
- 2 mois gratuits

## 🗄️ Base de données

Le système utilise SQLite avec les tables :
- `user` : Informations utilisateurs Discord
- `subscription` : Abonnements et leurs statuts
- `payment` : Historique des paiements PayPal

## 🔒 Sécurité

- **OAuth2 Discord** pour l'authentification sécurisée
- **PayPal** pour les paiements sécurisés
- **Session Flask** pour la gestion des sessions
- **Validation** des paiements côté serveur

## 📊 API Endpoints

### Vérification du statut premium
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

### Erreur de connexion Discord
- Vérifiez que le Client ID et Secret sont corrects
- Assurez-vous que l'URL de redirection est configurée

### Erreur PayPal
- Vérifiez les clés API PayPal
- En mode développement, utilisez les clés Sandbox

### Erreur de base de données
- Vérifiez que le fichier `premium_subscriptions.db` est créé
- Vérifiez les permissions d'écriture

## 🔄 Mise à jour

Pour mettre à jour le système :
1. Arrêtez le serveur
2. Sauvegardez la base de données
3. Mettez à jour les fichiers
4. Redémarrez le serveur

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs du serveur
2. Consultez la documentation Discord/PayPal
3. Contactez l'administrateur

---

**Note** : Ce système est conçu pour fonctionner en parallèle avec votre bot Discord existant. Il ne remplace pas le bot, il l'améliore avec des fonctionnalités premium. 