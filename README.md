1. Запускаем докер(Postgres,Redis)
   
   docker compose up -d

   ps: Redis нужен для храненияя jwt
2. Ставим все зависимости
   
   pip install -r requirements.txt
3. Запускаем сервак
   
   python3 main.py
4. Сваггер лежит тут
   
   127.0.0.1:8000/docs
5. Коллекция Postman

socialNetworkColl.postman_collection.json

6. Окружение Postman

socialNetworkEnv.postman_environment.json

