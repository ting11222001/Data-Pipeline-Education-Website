import pymysql

db = pymysql.connect(
    '192.168.56.123',
    'tiffany',
    'admin123',
    'education',
)
cursor = db.cursor(pymysql.cursors.DictCursor)

# careernet_flask：this table has mock data
sql = """SELECT * FROM education.careernet_flask;"""
cursor.execute(sql)
courses = cursor.fetchall()
db.close()

# courses is a list
# each course is a dictionary

print(courses[0]['category'], courses[0]['price'])

### get each course's category into a list
category_list = []
for course in courses:
    category_list.append(course['category'])
# print(category_list)
# print(list(set(category_list)))

### get an unique count of each category
category_count_dic = {}
unique_category = list(set(category_list))
for item in unique_category:
    # print("{}: ".format(item), category_list.count(item))
    category_count_dic[item] = category_list.count(item)
# print(category_count_dic)


### get category's total price
category_price_dic = {}
for course in courses:
    if course['price'] == 'NaN':
        course['price'] = course['price'].replace('NaN', '0')
    if course['category'] not in category_price_dic:
        category_price_dic[course['category']] = int(course['price'])
    else:
        category_price_dic[course['category']] += int(course['price'])
# print(category_price_dic)

### get category's average price
category_ave_price = {}
for key in category_price_dic:
    if key in category_count_dic:
        ave_price = int(category_price_dic[key] / category_count_dic[key]) 
        category_ave_price[key] = ave_price
# print(category_ave_price)        

### get pairs of count & average price
category_count_aveprice = []
for key in category_ave_price:
    if key in category_count_dic:
        category_count_aveprice.append({'{}_aveprice_x'.format(key): category_ave_price[key], '{}_count_y'.format(key): category_count_dic[key]})
print(category_count_aveprice)

# data: [{x:xx, y:xx}, {x:xx, y:xx}...]
# [{'{}_price_x'.format(key): category_ave_price[key], '{}_count_y'.format(key): category_count_dic[key]}]