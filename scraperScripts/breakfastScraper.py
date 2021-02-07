import json, requests, html, numpy as np
import csv
from bs4 import BeautifulSoup

pages = np.arange(2,6,1)
print(list(pages))
url = "https://www.eatyourselfskinny.com/category/recipes/breakfast/"
dish_urls = []
req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')
dishes = soup.find_all('div', class_= 'post-square')
for dish in dishes:
        dish_urls.append(dish.find('a')['href'])
for page in pages:
    req = requests.get(url + "page/" + str(page) + "/")
    soup = BeautifulSoup(req.text, 'html.parser') 
    dishes = soup.find_all('div', class_= 'post-square') #gets all the dishes
    for dish in dishes:
        dish_urls.append(dish.find('a')['href'])

breakfast = []
for x in range(0,33):
#look at each dish's recipe and nutrients
    req = requests.get(dish_urls[x])
    soup = BeautifulSoup(req.text, 'html.parser')
    script = soup.find('script', class_='yoast-schema-graph')
    script_tag_contents = script.string
    recipeInfo = json.loads(script_tag_contents).get('@graph')[4]
    recipeName = recipeInfo.get('name')
    print(recipeName)
    totalTime = (recipeInfo.get('totalTime'))[2:-1]
    ingredients = recipeInfo.get('recipeIngredient') #an array of ingredients
    nutrition = recipeInfo.get('nutrition') #dictionary of nutrition facts
    nutrition.pop('@type')
    stepDict = recipeInfo.get('recipeInstructions')
    steps = [] #an array of directions
    for step in stepDict:
        steps.append(step.get('text'))
    temp = {
        "Type" : "Breakfast",
        "Name" : recipeName,
        "Ingredients" : ingredients,
        "Total Time" : totalTime,
        "Recipe" : steps,
        "Nutritional Info" : nutrition,
        }
    breakfast.append(temp)

with open('breakfast.csv', mode='w') as csv_file:
    fieldnames = ['Type', 'Name', 'Ingredients', 'Total Time', 'Recipe', 'Nutritional Info']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for food in breakfast:
        writer.writerow(food)
