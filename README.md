# tech_challenge_04

Para rodar instalar os pacotes:

pip3 install -r requirements.txt

Antes de rodar a API, treinar o modelo:

python train.py

Para rodar a API:

uvicorn main:app --host 0.0.0.0 --port 8085 --reload