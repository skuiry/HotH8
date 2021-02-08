from MySQLdb import connect
import time

query = "SELECT * FROM full_menu" #WHERE od_Type <>'Breakfast' AND od_Type <>'Dinner'"
valid_dishes = []
score = []
#connecting to db
cnx = connect(user='sql3391309', password='CVs65SvZpJ', host='sql3.freesqldatabase.com', database='sql3391309')
cursor = cnx.cursor()

def getCalories(dish):
  nutrition = dish[5]
  cals = nutrition[nutrition.find('calories')+12:nutrition.find('su')-4]
  icals = int(cals)
  return icals

def scoreCalculator(StartCalories):
  global score
  for x in valid_dishes:
    cals = getCalories(x)
    dishScore = (1-((cals - StartCalories)/200))
    score.append(dishScore)

def find_valid_dishes(FoodType, StartCalories, EndCalories):
  global valid_dishes
  valid_dishes = []
  specs = ("SELECT * FROM full_menu WHERE od_Type ='%s'" %FoodType)
  cursor.execute(specs)
  for dish in cursor:
    calories = getCalories(dish)
    if (calories >= StartCalories and calories <= EndCalories):
      valid_dishes.append(dish)

def exitProgram():
  cursor.close()
  cnx.close()

i = ""
while (i != "x"):
  i = input("Input food type! (Enter x to exit): ")
  if (i == "x"):
    print("Have fun cooking!")
    exitProgram()
    break;
  foodType = i
  i = input("Input minimum calories(less than 492 cals)! (Enter x to exit): ")
  if (i == "x"):
    print("Have fun cooking!")
    exitProgram()
    break;
  start = i
  i = input("Input maximum calories! (Enter x to exit): ")
  if (i == "x"):
    print("Have fun cooking!")
    exitProgram()
    break;
  end = i;
  find_valid_dishes(foodType, int(start), int(end))
  counter = 0
  for x in valid_dishes:
    scoreCalculator(int(start))
    print("\n" + x[1] + " , score: " + str(score[counter]*100))
    counter = counter + 1 
  time.sleep(1)

