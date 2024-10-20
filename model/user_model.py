import mysql.connector
import jsonify,json
from flask import make_response

class user_model():
    
    def __init__(self):
        # connection establishing with the environment
        try:

            self.con=mysql.connector.connect(host="localhost",
            user="root",password="786123",
            database="flask")
            # for other queries
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            
            print("successfull!") 
        except:
            print("Error")
            
    def PrintData(self):
        self.cur.execute("SELECT * FROM api")
        # return list of dictionaries
        result=self.cur.fetchall()
        # print(result)
        # converting into plan string
        if len(result)>0:
            return make_response({"playload":result},200)
        else:
            return make_response("No data Found ",204)
    
    def Insert(self,data):
        self.cur.execute(f"INSERT INTO api(Name,phone) VALUES ('{data['Name']}','{data['phone']}')")
        # print(data)
        # for response header
        # res=make_response({"message":"Successfully Added!"},201)
        # res.headers['Access-Control-Allow-origin']="*"
        return make_response({"message":"Successfully Added!"},201)
    
    def Update(self,data):
        self.cur.execute(f"UPDATE api SET Name='{data['Name']}',phone='{data['phone']}' where id={data['id']}")
        # print(data)
        if self.cur.rowcount>0:
            return make_response({"message ": "Successfully Updated !"},201)
        else:
            return make_response({"message":"Not Updated ! "},202)
    
    def Delete(self,id):
        self.cur.execute(f"DELETE FROM api where id={id}")
        if self.cur.rowcount>0:
            return make_response({"message ": "Successfully Deleted!"},200)
        else:
            return make_response({"message":"Not deleted ! "},202)
    def Patch(self,data,id):
        qry="UPDATE api SET "
        for key in data:
            qry+=f"{key}='{data[key]}',"
            
        self.cur.execute(qry[:-1]+f" WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message ": "Successfully Updated !"},201)
        else:
            return make_response({"message":"Not Updated ! "},202)    
        # pagination function 
    def GetPage(self,limit,page):
            limit=int(limit)
            page=int(page)
            start=(limit*page)-limit
            qry=f"SELECT * FROM api limit {start},{limit}"
            self.cur.execute(qry)
            # return list of dictionaries
            result=self.cur.fetchall()
            # print(result)
            # converting into plan string
            if len(result)>0:
                return make_response({"playload":result,"page":page,"limit":limit},200)
            else:
                return make_response("No data Found ",204)    