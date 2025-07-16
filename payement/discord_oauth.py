import requests
import secrets
import urllib.parse

class DiscordOAuth2Session:
    def __init__(self, client_id, redirect_uri, token=None, state=None, scope=None):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.token = token
        self.state = state or secrets.token_urlsafe(32)
        self.scope = scope or ["identify", "email"]
    
    def create_authorization_url(self):
        """Crée l'URL d'autorisation Discord"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': ' '.join(self.scope),
            'state': self.state
        }
        
        url = "https://discord.com/api/oauth2/authorize"
        authorization_url = f"{url}?{urllib.parse.urlencode(params)}"
        
        return authorization_url, self.state
    
    def fetch_token(self, token_url, client_secret, authorization_response):
        """Récupère le token d'accès"""
        from urllib.parse import urlparse, parse_qs
        
        # Extraire le code de l'URL de réponse
        parsed_url = urlparse(authorization_response)
        query_params = parse_qs(parsed_url.query)
        
        code = query_params.get('code', [None])[0]
        state = query_params.get('state', [None])[0]
        
        if not code:
            raise ValueError("Code d'autorisation manquant")
        
        # Échanger le code contre un token
        data = {
            'client_id': self.client_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(token_url, data=data, headers=headers)
        
        if response.status_code == 200:
            self.token = response.json()
            return self.token
        else:
            raise Exception(f"Erreur lors de l'échange du token: {response.text}")
    
    def fetch_user(self):
        """Récupère les informations de l'utilisateur"""
        if not self.token:
            raise ValueError("Token d'accès manquant")
        
        headers = {
            'Authorization': f"Bearer {self.token['access_token']}"
        }
        
        response = requests.get('https://discord.com/api/users/@me', headers=headers)
        
        if response.status_code == 200:
            return DiscordUser(response.json())
        else:
            raise Exception(f"Erreur lors de la récupération des données utilisateur: {response.text}")

class DiscordUser:
    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.avatar = user_data.get('avatar')
        self.discriminator = user_data.get('discriminator')
    
    @property
    def avatar_url(self):
        if self.avatar:
            return f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png"
        return None 