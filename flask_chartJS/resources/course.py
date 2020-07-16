from flask_restful import Resource, reqparse
import pymysql
# 讓成功的資料看起來像Json
# 使用Flask的jsonify模組: jsonify不僅會將內容轉換為json，而且也會修改Content-Type為application/json
from flask import jsonify

# 給設定post用的參數
# 把client端發進來的參數讓flask看得懂
# 符合資料表的格式
parser = reqparse.RequestParser()
parser.add_argument('price')
parser.add_argument('start_date')
parser.add_argument('title')
parser.add_argument('today')

# 全部課程列表的分頁的web method: get, post
class Courses(Resource):
    # 連接資料庫function
    def db_init(self):
        db = pymysql.connect(
            # 連到我的database的資訊，指定進到education
            '192.168.56.123',
            'tiffany',
            'admin123',
            'education',
        )
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    # response回傳function
    def response(self, result):
        response = {"code": 200, "msg": "success"}
        # 如果sql沒有執行成功，result會是0
        if result == 0:
            response['code'] = 400
            response['msg'] = 'error'
        return jsonify(response)

    def get(self):
        # 開啟資料庫連線
        db, cursor = self.db_init()
        # 連線到education(database)的careernet_flask(table)
        # sql = """SELECT * FROM education.careernet_flask;"""
        # 第二種寫法加上WHERE deleted = False，是為了配合後面的軟刪除
        sql = """SELECT * FROM education.careernet_flask WHERE deleted = False;"""
        # 執行sql語法
        cursor.execute(sql)
        # 返回所有結果
        courses = cursor.fetchall()
        # 關閉sql連線
        db.close()
        # 返回包含json格式的response
        return jsonify(courses)

    def post(self):
        # 開啟資料庫連線
        db, cursor = self.db_init()
        # 把解析的參數接到arg變數
        arg = parser.parse_args()
        # 把所有可能接到的變數整理成dictionary
        course = {
            'price': arg['price'],
            'start_date': arg['start_date'],
            'title': arg['title'],
            'today': arg['today']
        }
        # 把上面參數整理成sql語法
        sql = """
            INSERT INTO `education`.`careernet_flask` (`price`, `start_date`, `title`, `today`)
            VALUES ('{}', '{}', '{}', '{}');
        """.format(course['price'], course['start_date'], course['title'], course['today'])
        # 執行、變更並關閉sql連線，把執行結果接到result變數
        result = cursor.execute(sql)
        db.commit()
        db.close()
        # 依照執行結果，回傳response，引用前面response function
        return self.response(result)

# 指定課程列表的分頁的web method: get, delete, patch
class Course(Resource):
    # 連接資料庫function
    def db_init(self):
        db = pymysql.connect(
            # 連到我的database的資訊，指定進到education
            '192.168.56.123',
            'tiffany',
            'admin123',
            'education',
        )
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    # response回傳function
    def response(self, result):
        response = {"code": 200, "msg": "success"}
        # 如果sql沒有執行成功，result會是0
        if result == 0:
            response['code'] = 400
            response['msg'] = 'error'
        return jsonify(response)
    
    # 抓取符合id的課程資料
    def get(self, id):
        db, cursor = self.db_init()
        sql = """SELECT * FROM `education`.`careernet_flask` 
        WHERE id = {};
        """.format(id)
        cursor.execute(sql)
        # 只抓第一筆回傳資料
        course = cursor.fetchone()
        db.close()
        return jsonify(course)
    
    def delete(self, id):
        db, cursor = self.db_init()
        # 真正在sql刪除這一門課的資料
        # sql = """
        # DELETE FROM `education`.`careernet_flask`
        # WHERE id = {};
        # """.format(id)   
        # 軟刪除，把預設的deleted = 0都變成deleted = 1
        sql = """
        UPDATE `education`.`careernet_flask`
        SET deleted = True
        WHERE id = {};
        """.format(id)      
        result = cursor.execute(sql)
        db.commit()
        db.close()
        return self.response(result)

    def patch(self, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        course = {
            'price': arg['price'],
            'start_date': arg['start_date'],
            'title': arg['title'],
            'today': arg['today']
        }
        # 整理好的sql query語法會放在這裡
        query = []
        # 把一個dictionary的值都變成key, value的tuple
        for key, value in course.items():
            # 只要輸入的value不是空值，就用指定格式key = ‘value’寫進query這個list
            if value != None:
                query.append(key + " = " + " '{}' ".format(value))
        # 把query list裡面的每個項目join起來變成字串
        query = ",".join(query)
        # 更改指定的課程資訊
        sql = """
        UPDATE `education`.`careernet_flask` 
        SET {} 
        WHERE id = {};
        """.format(query, id)
        result = cursor.execute(sql)
        db.commit()
        db.close()
        return self.response(result)
    