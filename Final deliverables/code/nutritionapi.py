import requests

url = "https://api.apilayer.com/spoonacular/food/products/search?query=burger"

payload = {}
headers= {
  "apikey": "UTKTN5GEzMK4iyA3IxBavmadHyGBXh02"
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text