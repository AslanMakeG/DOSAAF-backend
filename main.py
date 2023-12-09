import glob
import hashlib
import json
import os
from datetime import datetime
from fastapi import FastAPI
import uvicorn
from starlette import status
from starlette.responses import Response
from models import test_models
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

if __name__ == '__main__':
    uvicorn.run(app=app)