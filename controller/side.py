from __main__ import app
from flask import request
from model.user_model import user_model
obj=user_model()
@app.route('/user')

def index():
    return obj.PrintData()
# by default get is allowed
@app.route('/user/add',methods=['POST'])
def Add():
    return obj.Insert(request.form)

@app.route('/user/update',methods=['PUT'])
def change():
    return obj.Update(request.form)
# passing attribute from url
@app.route('/user/delete/<id>',methods=['DELETE'])
def modify(id):
    return obj.Delete(id)
# means we are just changing what we want not have to
# pass all the entries to updatee 

@app.route('/user/patch/<id>',methods=['PATCH'])
def modify2(id):
    return obj.Patch(request.form,id)
# pagination method
@app.route("/user/limit/<limit>/page/<page>")
def getAll(limit,page):
    return obj.GetPage(limit,page)