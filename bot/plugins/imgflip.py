import os
import json
import requests
from typing import Dict
from .plugin import Plugin

class ImgflipPlugin(Plugin):
    """
    A plugin to create memes using the Imgflip API.
    """

    def __init__(self):
        imgflip_username = os.getenv('IMGFLIP_USERNAME')
        imgflip_password = os.getenv('IMGFLIP_PASSWORD')
        if not imgflip_username or not imgflip_password:
            raise ValueError('IMGFLIP_USERNAME and IMGFLIP_PASSWORD environment variables must be set to use ImgflipPlugin')
        self.username = imgflip_username
        self.password = imgflip_password

    def get_source_name(self) -> str:
        return "Imgflip"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "create_meme",
            "description": "Create a meme with top and bottom text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "template_id": {"type": "string", "description": "ID of the meme template."},
                    "text0": {"type": "string", "description": "Text for the top part of the meme."},
                    "text1": {"type": "string", "description": "Text for the bottom part of the meme."},
                },
                "required": ["template_id", "text0", "text1"]
            }
        }]

    async def execute(self, function_name, **kwargs) -> Dict:
        if function_name == 'create_meme':
            payload = {
                "template_id": kwargs['template_id'],
                "username": self.username,
                "password": self.password,
                "text0": kwargs['text0'],
                "text1": kwargs['text1']
            }

            try:
                response = requests.post("https://api.imgflip.com/caption_image", params=payload)
                response.raise_for_status()
                result = json.loads(response.text)

                if result['success']:
                    return {'url': result['data']['url']}
                else:
                    return {'error': f"Error creating meme: {result['error_message']}"}

            except requests.RequestException as e:
                return {'error': 'An unexpected error occurred: ' + str(e)}
