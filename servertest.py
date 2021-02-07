from MySQLdb import connect

cnx = connect(user='sql3391309', password='CVs65SvZpJ', host='sql3.freesqldatabase.com', database='sql3391309')
cursor = cnx.cursor()

query = "SELECT * FROM full_menu WHERE od_Type <>'Breakfast' AND od_Type <>'Dinner'"

cursor.execute(query)
for (Type, Name, Recipe, Ingredients, N, Time) in cursor:
    print("%s dish is named %s!" %(Type, Name))

cursor.close()
cnx.close()

