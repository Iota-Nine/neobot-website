import requests
import json
from datetime import datetime
import sqlite3

class PremiumIntegration:
    def __init__(self, premium_api_url="http://localhost:5000"):
        self.premium_api_url = premium_api_url
        self.db_path = "premium_subscriptions.db"
    
    def check_premium_status(self, discord_id):
        """Vérifie le statut premium d'un utilisateur Discord"""
        try:
            response = requests.get(f"{self.premium_api_url}/api/premium/{discord_id}")
            if response.status_code == 200:
                return response.json()
            else:
                return {"premium": False, "message": "Erreur API"}
        except Exception as e:
            print(f"Erreur lors de la vérification premium: {e}")
            return {"premium": False, "message": "Erreur de connexion"}
    
    def is_premium_user(self, discord_id):
        """Vérifie si un utilisateur a un abonnement premium actif"""
        status = self.check_premium_status(discord_id)
        return status.get("premium", False)
    
    def get_premium_features(self, discord_id):
        """Récupère les fonctionnalités premium d'un utilisateur"""
        status = self.check_premium_status(discord_id)
        if status.get("premium", False):
            return status.get("features", [])
        return []
    
    def get_memory_limit(self, discord_id):
        """Retourne la limite de mémoire selon le statut premium"""
        if self.is_premium_user(discord_id):
            # Vérifier le type de plan
            status = self.check_premium_status(discord_id)
            plan_type = status.get("plan_type", "monthly")
            
            if plan_type == "yearly":
                return 500  # Limite étendue pour l'abonnement annuel
            else:
                return 200  # Limite étendue pour l'abonnement mensuel
        else:
            return 50  # Limite gratuite
    
    def can_access_persona(self, discord_id, persona_type):
        """Vérifie si un utilisateur peut accéder à un personnage spécifique"""
        if self.is_premium_user(discord_id):
            return True  # Accès illimité pour les utilisateurs premium
        
        # Liste des personnages gratuits
        free_personas = ["NORMAL", "DEFAULT"]
        return persona_type in free_personas
    
    def get_premium_message(self, discord_id):
        """Retourne un message pour encourager l'upgrade premium"""
        if not self.is_premium_user(discord_id):
            return (
                "🌟 **Upgrade Premium !**\n"
                "Débloquez toutes les fonctionnalités avec NeoBot Premium :\n"
                "• Accès à tous les personnages\n"
                "• Mémoire étendue (200-500 messages)\n"
                "• Support prioritaire\n"
                "• Fonctionnalités avancées\n\n"
                "💳 **Abonnements disponibles :**\n"
                "• Mensuel : 9.99€/mois\n"
                "• Annuel : 99.99€/an (2 mois gratuits)\n\n"
                "🔗 **Lien d'inscription :** http://localhost:5000"
            )
        return None

# Fonction pour intégrer avec le bot existant
def integrate_with_bot():
    """Intègre le système premium avec le bot Discord existant"""
    
    # Exemple d'utilisation dans le bot
    premium = PremiumIntegration()
    
    # Dans la fonction on_message du bot, vous pouvez ajouter :
    """
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        # Vérifier le statut premium
        is_premium = premium.is_premium_user(str(message.author.id))
        memory_limit = premium.get_memory_limit(str(message.author.id))
        
        # Vérifier l'accès au personnage
        persona_type = "NORMAL"  # ou récupérer depuis le message
        can_access = premium.can_access_persona(str(message.author.id), persona_type)
        
        if not can_access:
            premium_msg = premium.get_premium_message(str(message.author.id))
            await message.channel.send(premium_msg)
            return
        
        # Continuer avec le traitement normal du message
        # ...
    """
    
    return premium

# Exemple d'utilisation
if __name__ == "__main__":
    premium = PremiumIntegration()
    
    # Test avec un ID Discord
    test_discord_id = "123456789"
    
    print(f"Statut premium: {premium.is_premium_user(test_discord_id)}")
    print(f"Limite mémoire: {premium.get_memory_limit(test_discord_id)}")
    print(f"Peut accéder à LEWD: {premium.can_access_persona(test_discord_id, 'LEWD')}")
    
    message = premium.get_premium_message(test_discord_id)
    if message:
        print("Message premium:", message) 