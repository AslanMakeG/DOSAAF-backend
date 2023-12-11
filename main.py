import glob
import hashlib
import json
import os
from datetime import datetime
from fastapi import FastAPI
import uvicorn
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import Response, JSONResponse
from models import test_models, database_models
from lib import User, ServiceManager, NewsManager, RequestManager
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_id():
    b = bytes(str(datetime.now()), encoding='utf-8')
    hash_object = hashlib.md5(b)
    return hash_object.hexdigest()

def create_test_file(data):
    with open(f"tests/test_{data['id']}.json", "w") as json_file:
        json.dump(data, json_file)

@app.post('/api/create_test')
async def create_test(test: test_models.Test):
    test_json = test.model_dump()
    test_json['id'] = get_id()
    create_test_file(test_json)
    return Response(status_code=status.HTTP_200_OK)

@app.get('/api/get_tests')
async def get_tests():
    path = 'tests/'
    test_list = []
    for filename in glob.glob(os.path.join(path, '*.json')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            test = json.loads(f.read())
            test_list.append({"id": test['id'], "name": test['name']})

    return {'tests': test_list}

@app.get('/api/get_test/{test_id}')
async def get_tests(test_id: str):
    path = 'tests/'
    test_list = []
    for filename in glob.glob(os.path.join(path, f'test_{test_id}.json')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            test = json.loads(f.read())
            for question in test['questions']:
                del question['right_answer']
            test_list.append(test)

    return {'test': test_list}

@app.get('/api/delete_test/{id}')
async def delete_test(id: str):
    os.remove(f"tests/test_{id}.json")
    return Response(status_code=status.HTTP_200_OK)

@app.post('/api/check_answers')
async def create_test(test: test_models.UserSolvedTest):
    user_questions = test.questions
    right_questions = []

    result = 0

    path = 'tests/'
    for filename in glob.glob(os.path.join(path, f'test_{test.id}.json')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            test = json.loads(f.read())
            right_questions = test['questions']

    for i in range(len(user_questions)):
        if user_questions[i].right_answer == right_questions[i]['right_answer']:
            result += 1

    return {"result": result, "question_amount": len(right_questions)}

@app.post('/api/register_user')
async def register_user(user: database_models.User):
    response = User.registration(get_id(), user.name, user.surname, user.patronymic, user.email, user.password)

    if response is None:
        return {'status': 200}
    else:
        return {'status': 400, 'error': response}


@app.get('/api/auth_user/{email}/{password}')
async def auth_user(email: str, password: str):
    success, response = User.auth(email, password)

    if success:
        return JSONResponse(content=jsonable_encoder({'status': 200, 'user_id': response}))
    else:
        return JSONResponse(content=jsonable_encoder({'status': 400, 'error': response}))


@app.get('/api/get_user_info/{id}')
async def get_user_info(id: str):
    user_info = User.get_info(id)

    return JSONResponse(content=jsonable_encoder(user_info))


@app.get('/api/get_user_type/{id}')
async def get_user_info(id: str):
    user_type = User.get_type(id)

    return JSONResponse(content=jsonable_encoder(user_type))


@app.post('/api/create_service')
async def create_service(service: database_models.Service):
    service_id = ServiceManager.create_service(get_id(), service.name, service.description, int(service.cost))

    return JSONResponse(content=jsonable_encoder({'id': service_id, 'name': service.name,
                                                  'description': service.description, 'cost': service.cost}))


@app.get('/api/delete_service/{id}')
async def delete_service(id: str):
    ServiceManager.delete_service(id)
    return Response(status_code=status.HTTP_200_OK)


@app.get('/api/get_services')
async def get_services():
    service_list = ServiceManager.get_all()
    return JSONResponse(content=jsonable_encoder(service_list))


@app.post('/api/create_news')
async def create_news(news: database_models.News):
    news_id = NewsManager.create_news(get_id(), news.name, news.description)

    return JSONResponse(content=jsonable_encoder({'id': news_id, 'name': news.name,
                                                  'description': news.description }))


@app.get('/api/delete_news/{id}')
async def delete_news(id: str):
    NewsManager.delete_news(id)
    return Response(status_code=status.HTTP_200_OK)


@app.get('/api/get_news')
async def get_news():
    news_list = NewsManager.get_all()
    return JSONResponse(content=jsonable_encoder(news_list))


@app.post('/api/create_request')
async def create_request(request: database_models.Request):
    RequestManager.create_request(get_id(), request.id_user, request.id_service, request.user_fullname, request.phone_number)

    return Response(status_code=status.HTTP_200_OK)

if __name__ == '__main__':
    uvicorn.run(app=app)