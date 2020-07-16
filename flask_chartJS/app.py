# 主程式 by flask app
import flask
from flask import request, render_template, jsonify
from flask_restful import Api, Resource
from resources.course import Courses, Course 
import pymysql

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['JSON_AS_ASCII'] = False

api = Api(app)

# home page with API instructions
@app.route('/', methods = ['get'])
def home():
    content = """
    <!doctype html>
    <html lang="en">
    <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">

    <title>Tiffany's Careernet API</title>
     </head>
    <body>
        <div class="jumbotron jumbotron-fluid">
            <div class="container">
                <h1 class="display-4">Welcome to Tiffany's Education API</h1>
                <p class="lead">讓同學們可以透過我的API跟我爬蟲下來的網站資訊互動</p>
                <p class="lead">以青創學院為例 - https://www.careernet.org.tw/</p>
            </div>
        </div>

        <div class="accordion" id="accordionExample">
            <div class="card">
                <div class="card-header" id="headingOne">
                <h2 class="mb-0">
                    <button class="btn btn-link btn-block text-left" type="button" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                    如何進到API首頁
                    </button>
                </h2>
                </div>

                <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordionExample">
                <div class="card-body">
                    路徑：http://0.0.0.0:5000/ 或 http://localhost:5000/ <br>
                    <br>
                    可以將localhost ip換成zerotier ip。<br>
                    目前沒有設置權限。
                </div>
                </div>
            </div>
            <div class="card">
                <div class="card-header" id="headingTwo">
                <h2 class="mb-0">
                    <button class="btn btn-link btn-block text-left collapsed" type="button" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                    全部課程列表的分頁的web method: get, post
                    </button>
                </h2>
                </div>
                <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordionExample">
                <div class="card-body">
                    路徑：http://0.0.0.0:5000/courses <br>
                    <br>
                    使用postman測試： <br>
                    get: 可以讀取所有課程。<br>
                    post: 可以新增課程，可以填入的參數為price, start_date, title, today。<br>
                    ＊price: 費用, start_date: 開課日期, title: 課程名稱, today: 爬蟲日期。<br>
                    <br>
                    如果成功，回傳值為 {"code": 200, "msg": "success"}。<br>
                    如果輸入有誤，回傳值為 {"code": 400, "msg": "error"}。<br>
                </div>
                </div>
            </div>
            <div class="card">
                <div class="card-header" id="headingThree">
                <h2 class="mb-0">
                    <button class="btn btn-link btn-block text-left collapsed" type="button" data-toggle="collapse" data-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                    指定課程列表的分頁的web method: get, delete, patch
                    </button>
                </h2>
                </div>
                <div id="collapseThree" class="collapse" aria-labelledby="headingThree" data-parent="#accordionExample">
                <div class="card-body">
                    路徑：http://0.0.0.0:5000/course/id <br>
                    <br>
                    使用postman測試： <br>
                    get: 可以依據id讀取指定課程。<br>
                    delete: 可以依據id刪除指定課程，提供軟刪除的功能，如果不小心刪除某一門課，仍然可以回復。<br>
                    patch: 可以依據id更新指定課程，可以填入的參數為price, start_date, title, today。<br>
                    ＊price: 費用, start_date: 開課日期, title: 課程名稱, today: 爬蟲日期。<br>
                    <br>
                    如果成功，回傳值為 {"code": 200, "msg": "success"}。<br>
                    如果輸入有誤，回傳值為 {"code": 400, "msg": "error"}。
                </div>
                </div>
            </div>
            <div class="card">
                <div class="card-header" id="headingFour">
                <h2 class="mb-0">
                    <button class="btn btn-link btn-block text-left collapsed" type="button" data-toggle="collapse" data-target="#collapseFour" aria-expanded="false" aria-controls="collapseFour">
                    簡易分析圖表ChartJS
                    </button>
                </h2>
                </div>
                <div id="collapseFour" class="collapse" aria-labelledby="headingFour" data-parent="#accordionExample">
                <div class="card-body">
                    路徑：http://0.0.0.0:5000/charts <br>
                    <br>
                    原始資料： <br>
                    目前課程類別數量比例: http://0.0.0.0:5000/data_pie <br>
                    目前課程類別平均價格: http://0.0.0.0:5000/data_bar <br>
                    目前課程平均價格和類別數量: http://0.0.0.0:5000/data_scatter <br>
                    ＊資料格式: json <br>
                </div>
                </div>
            </div>
        </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return content

# API web methods to all courses
api.add_resource(Courses, "/courses")

# API web methods to one specific course
api.add_resource(Course, "/course/<id>")

# Show all three charts
@app.route('/charts')
def index():
    # By default, Flask looks in the templates folder in the root level of your app.
    return render_template("chartJS.html")

# Show the 1st pie chart's raw data in json format
@app.route('/data_pie')
def data_pie():
    # connect to mysql db
    db = pymysql.connect(
        '192.168.56.123',
        'tiffany',
        'admin123',
        'education',
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # query to mysql db
    sql = """SELECT * FROM education.careernet_flask;"""
    cursor.execute(sql)
    courses = cursor.fetchall()
    db.close()
    # make a list
    category_list = []
    for course in courses:
        category_list.append(course['category'])
    # make a dict
    category_class_count = {}
    unique_category = list(set(category_list))
    for item in unique_category:
        category_class_count[item] = category_list.count(item)
    return jsonify(category_class_count)

# Show the 2nd bar chart's raw data in json format
@app.route('/data_bar')
def data_bar():
    db = pymysql.connect(
        '192.168.56.123',
        'tiffany',
        'admin123',
        'education',
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """SELECT * FROM education.careernet_flask;"""
    cursor.execute(sql)
    courses = cursor.fetchall()
    db.close()
    ### get each course's category into a list
    category_list = []
    for course in courses:
        category_list.append(course['category'])
    ### get an unique count of each category
    category_count_dic = {}
    unique_category = list(set(category_list))
    for item in unique_category:
        category_count_dic[item] = category_list.count(item)
    ### get category's total price
    category_price_dic = {}
    for course in courses:
        if course['price'] == 'NaN':
            course['price'] = course['price'].replace('NaN', '0')
        if course['category'] not in category_price_dic:
            category_price_dic[course['category']] = int(course['price'])
        else:
            category_price_dic[course['category']] += int(course['price'])
    ### get category's average price
    category_ave_price = {}
    for key in category_price_dic:
        if key in category_count_dic:
            ave_price = int(category_price_dic[key] / category_count_dic[key]) 
            category_ave_price[key] = ave_price
    return jsonify(category_ave_price) 

# Show the 3rd line chart's raw data in json format
@app.route('/data_scatter')
def data_scatter():
    db = pymysql.connect(
        '192.168.56.123',
        'tiffany',
        'admin123',
        'education',
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """SELECT * FROM education.careernet_flask;"""
    cursor.execute(sql)
    courses = cursor.fetchall()
    db.close()
    ### get each course's category into a list
    category_list = []
    for course in courses:
        category_list.append(course['category'])
    ### get an unique count of each category
    category_count_dic = {}
    unique_category = list(set(category_list))
    for item in unique_category:
        category_count_dic[item] = category_list.count(item)
    ### get category's total price
    category_price_dic = {}
    for course in courses:
        if course['price'] == 'NaN':
            course['price'] = course['price'].replace('NaN', '0')
        if course['category'] not in category_price_dic:
            category_price_dic[course['category']] = int(course['price'])
        else:
            category_price_dic[course['category']] += int(course['price'])
    ### get category's average price
    category_ave_price = {}
    for key in category_price_dic:
        if key in category_count_dic:
            ave_price = int(category_price_dic[key] / category_count_dic[key]) 
            category_ave_price[key] = ave_price
    ### get pairs of count & average price
    category_count_aveprice = []
    for key in category_ave_price:
        if key in category_count_dic:
            category_count_aveprice.append({'{}_aveprice_x'.format(key): category_ave_price[key], '{}_count_y'.format(key): category_count_dic[key]})
    return jsonify(category_count_aveprice)


if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port = 3333)
    app.run(host = '0.0.0.0')