import os
import requests
from typing import Dict
from .plugin import Plugin

class GithubPlugin(Plugin):
    """
    A plugin to interact with GitHub via API
    """

    def get_source_name(self) -> str:
        return "GitHub"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "get_notifications",
            "description": "Get GitHub notifications",
            "parameters": {
                "type": "object",
                "properties": {
                    "participating": {"type": "boolean", "description": "If true, it shows only notifications in which the user is directly participating or mentioned.", "default": False}
                },
            },
        }]

    async def execute(self, function_name, **kwargs) -> Dict:
        if function_name == 'get_notifications':
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                return {"error": "GitHub token not found in environment variables"}
            
            headers = {'Authorization': f'token {token}'}
            params = {'participating': kwargs.get("participating", False)}

            try:
                response = requests.get('https://api.github.com/notifications', headers=headers, params=params)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                return {'error': f'An error occurred: {e}'}
