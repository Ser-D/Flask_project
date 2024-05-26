# Flask_project

1. Створити файл .env і скопіюйте дані з .env.example.

2. Запускаємо Docker:
        docker-compose up -d 

3. Без Postgres(Docker) почнем на SQLite.

4.Команди для старту з "0":
        flask db init   
        flask db migrate -m "Init" 
        flask db upgrade 

5. Адмін в бд -- ser(12345)


Додаток:
- Analyst -- перегляд tickets;
- Manager -- створення, зміна статусу tickets в своїй групі;
- Admin -- створення, зміна статусу всіх tickets.

        

