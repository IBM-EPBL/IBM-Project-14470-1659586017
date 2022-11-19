import requests

with  open("./static/images/burger.jpeg","rb")  as f:
    file=f.read()

url="https://api.spoonacular.com/food/images/analyze"

API_KEY = "c6b26a53ad36401c969cff947ee122d7"

res = requests.get(url,params={"imageUrl":"https://media-cldnry.s-nbcnews.com/image/upload/newscms/2019_21/2870431/190524-classic-american-cheeseburger-ew-207p.jpg","apiKey":API_KEY})
print(res,res.content)