import os
import requests
from typing import Dict
from .plugin import Plugin

class SmmryPlugin(Plugin):
    """
    A plugin to summarize webpages using SMMRY.
    """

    def __init__(self):
        smmry_api_key = os.getenv('SMMRY_API_KEY')
        if not smmry_api_key:
            raise ValueError('SMMRY_API_KEY environment variable must be set to use SmmryPlugin')
        self.api_key = smmry_api_key

    def get_source_name(self) -> str:
        return "SMMRY"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "summarize_webpage",
            "description": "Summarize a webpage based on a URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The webpage URL to summarize"},
                    "length": {"type": "integer", "description": "Number of sentences in summary"}
                },
                "required": ["url"]
            },
        }]

    async def execute(self, function_name, **kwargs) -> Dict:
        if function_name == 'summarize_webpage':
            url = kwargs['url']
            length = kwargs.get('length', 7)  # default to 7 sentences

            params = {
                'SM_API_KEY': self.api_key,
                'SM_URL': url,
                'SM_LENGTH': length
            }

            response = requests.get('https://api.smmry.com', params=params)
            return response.json()
