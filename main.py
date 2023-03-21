from fastapi import FastAPI,Request, Form, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,FileResponse,StreamingResponse
from typing import List
import numpy as np
import time,os
from argparse import ArgumentParser



app = FastAPI()
root_path = os.path.dirname(os.path.abspath(__file__))
print(root_path)

template = Jinja2Templates("pages")
pic_path = os.path.join(root_path,'fixed_pic/home_pic.png')
todo_list=["积硅步 致千里"]
cout = 0
# root_path = '/data/jinhui.lin/code/mmdetect/deep_learning_od/app_design/dingyu/'
files_path = ''
image_name = ''
pic_name =''
flag = 0
# upload_list=[]

@app.get("/")
def show_home(req:Request):
    global pic_name
    global flag
    if flag == 1:
        flag = 0
    else:
        pic_name =''
    
    return template.TemplateResponse('home.html',context={"request":req,"todos":todo_list})


@app.get("/xiaohui")
def show_pic():
    pic_path = os.path.join(root_path,'fixed_pic/xiaohui.png') 
    return FileResponse(pic_path)
@app.get("/yuanhui")
def show_pic():
    pic_path1 = os.path.join(root_path,'fixed_pic/yuanhui4.png')  
    return FileResponse(pic_path1)
@app.get("/background")
def show_pic():
    pic_path1 = os.path.join(root_path,'fixed_pic/background5.png')
    return FileResponse(pic_path1)

@app.get("/smoke")
def show_pic():
    pic_path1 = os.path.join(root_path,'fixed_pic/smoke.jpeg')
    return FileResponse(pic_path1)
@app.get("/fire")
def show_pic():
    pic_path1 = os.path.join(root_path,'fixed_pic/fire.jpeg')
    return FileResponse(pic_path1)
@app.get("/clothes")
def show_pic():
    pic_path1 = os.path.join(root_path,'fixed_pic/clothes.png')
    return FileResponse(pic_path1)




@app.get("/pic_upload")
def show_pic():
    pic_path2 = os.path.join(files_path,pic_name)
    print('----------------------w-------------------------')
    if pic_name =='':
        return 'FileResponse(pic_path2)'
    else:
        return FileResponse(pic_path2)

@app.post("/upload_pics/")
async def upload(files:UploadFile):
    print(files)
    imageby = files.file.read()
    global pic_name
    global files_path
    pic_name = files.filename
    today_time = time.strftime("%Y_%m_%d",time.localtime())
    files_path = os.path.join(root_path,'pic_uploaded/'+ today_time)
    if not os.path.exists(files_path):
        os.mkdir(files_path)
    print(files_path)
    with open(files_path +'/' + pic_name,'wb') as file_out:
        file_out.write(imageby)


    global cout
    global flag
    flag = 1
    cout +=1
    if len(todo_list):
        todo_list.pop(0)
    todo_list.insert(0,'上传成功：{}'.format(cout))
    # return image_name
    return RedirectResponse("/",status_code=302)


@app.post("/todo")
def todo(todo=Form(None)):
    todo_list.insert(0,todo)
    return RedirectResponse("/",status_code=302)


result = {}

@app.post("/inference")
async def inference(files:UploadFile):
    imageby = files.file.read()
    global pic_name
    global files_path
    pic_name = files.filename
    today_time = time.strftime("%Y_%m_%d",time.localtime())
    files_path = os.path.join(root_path,'pic_uploaded/'+ today_time)
    if not os.path.exists(files_path):
        os.mkdir(files_path)
    print(files_path)
    with open(files_path +'/' + pic_name,'wb') as file_out:
        file_out.write(imageby)

    # model = './loaded_models/exp13_best.pt'
    #  without model return test result
    gen_img = 'result'
    # return RedirectResponse("/",status_code=302)
    return FileResponse(gen_img)
