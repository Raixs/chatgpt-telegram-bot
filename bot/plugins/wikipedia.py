import requests
from typing import Dict
from .plugin import Plugin


class WikipediaPlugin(Plugin):
    """
    A plugin to retrieve summaries from Wikipedia based on a given search term.
    """

    def get_source_name(self) -> str:
        return "Wikipedia"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "get_wikipedia_summary",
            "description": "Get the summary of a Wikipedia article based on a search term.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term for Wikipedia article"}
                },
                "required": ["query"],
            },
        }]

    async def execute(self, function_name, **kwargs) -> Dict:
        if function_name == 'get_wikipedia_summary':
            query = kwargs['query']
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                return {'error': 'An unexpected error occurred: ' + str(e)}

