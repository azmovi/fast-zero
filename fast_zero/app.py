from fastapi import FastAPI

from fast_zero.schemas import Message

from fastapi.testclient import TestClient

app = FastAPI()


@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'mensage': 'Ola mundo'}


cliente = TestClient(app)
resposta = cliente.get('/')
print(resposta)
