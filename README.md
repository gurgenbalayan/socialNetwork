1. Скачиваем проект

   git clone https://github.com/gurgenbalayan/socialNetwork.git && cd socialNetwork

2. Запускаем докер(Postgres,Redis)
   
   docker compose up -d

   ps: Redis нужен для храненияя jwt
3. Ставим все зависимости (python3.12)
   
   python3 -m venv env
   
   source env/bin/activate

   pip install -r requirements.txt
   
4. Запускаем сервак
   
   python3 main.py
5. Сваггер лежит тут
   
   127.0.0.1:8000/docs
6. Коллекция Postman

socialNetworkColl.postman_collection.json

7. Окружение Postman

socialNetworkEnv.postman_environment.json

