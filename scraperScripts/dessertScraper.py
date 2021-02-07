import json, requests, html, numpy as np
import csv
from bs4 import BeautifulSoup


url = "https://www.eatyourselfskinny.com/category/recipes/desserts/"
dish_urls = []
req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')
dishes = soup.find_all('div', class_= 'post-square')
for dish in dishes:
        dish_urls.append(dish.find('a')['href'])

desserts = []
dish_urls.pop(4)
for dish in dish_urls:
#look at each dish's recipe and nutrients
    req = requests.get(dish)
    soup = BeautifulSoup(req.text, 'html.parser')
    script = soup.find('script', class_='yoast-schema-graph')
    script_tag_contents = script.string
    try:
        recipeInfo = json.loads(script_tag_contents).get('@graph')[4]
        recipeName = recipeInfo.get('name')
        print(recipeName)
        totalTime = (recipeInfo.get('totalTime'))
        if (totalTime):
            totalTime = totalTime[2:-1]
        else:
            totalTime = 0
        ingredients = recipeInfo.get('recipeIngredient') #an array of ingredients
        nutrition = recipeInfo.get('nutrition') #dictionary of nutrition facts
        nutrition.pop('@type')
        stepDict = recipeInfo.get('recipeInstructions')
        steps = [] #an array of directions
        for step in stepDict:
            steps.append(step.get('text'))
        temp = {
            "Type" : "Dessert",
            "Name" : recipeName,
            "Ingredients" : ingredients,
            "Total Time" : totalTime,
            "Recipe" : steps,
            "Nutritional Info" : nutrition,
            }
        desserts.append(temp)
    except:
        print("SKIPPED")

with open('dessert.csv', mode='w') as csv_file:
    fieldnames = ['Type', 'Name', 'Ingredients', 'Total Time', 'Recipe', 'Nutritional Info']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for food in desserts:
        writer.writerow(food)
