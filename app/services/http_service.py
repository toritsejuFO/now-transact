import requests

class HttpService:
    def get(url, query):
        response = requests.get(url, params=query, timeout=(1, 1))
        response.raise_for_status()
        return response.json()
