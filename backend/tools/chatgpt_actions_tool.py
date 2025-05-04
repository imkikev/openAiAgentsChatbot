# Define the function to fetch ChatGPT IPs white using the function tool
from agents import function_tool
import requests

@function_tool
def get_chatgpt_actions() -> str:
    """Fetches and returns the list of ChatGPT IP whitelist prefixes from the official API."""
    url = "https://openai.com/chatgpt-actions.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        prefixes = data.get("prefixes", [])
        ip_list = [prefix.get("ipv4Prefix", "Unknown") for prefix in prefixes]
        return "Here are the ChatGPT IP whitelist prefixes:\n" + "\n".join(ip_list)
    except requests.RequestException as e:
        return f"An error occurred while fetching IP prefixes: {e}"