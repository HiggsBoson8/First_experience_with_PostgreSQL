import random
import requests
import json 
import psycopg2 
from random import randint

def generate_person(n = 1):
    #Создайте список дял хранения информации о людях
    people_list = []
    professions = ["engineer", "teacher", "programmer", "nurse", "policeman", "designer", "lawyer", "painter"]

    # Connect к PostgreSQL database
    connection = psycopg2.connect(
        host = "localhost",
        user = "abay",
        password = "123",
        database = "mydb2"
    )

    cursor = connection.cursor()

    # Создать таблицу, если она не существует
    cursor.execute("CREATE TABLE users(id SERIAL PRIMARY KEY, name VARCHAR(50),\
        age INT, email VARCHAR(255), profession VARCHAR(255), phone VARCHAR(255))") 

    # Отправить n запросов на получение в API
    for i in range(n):
        response = requests.get("https://randomuser.me/api/?nat=us")
        
        # Проанализируем ответ JSON
        data = json.loads(response.text)
        
        # Извлеките имя и фамилию
        first_name = data["results"][0]["name"]["first"]
        last_name = data["results"][0]["name"]["last"]
        
        # Объединяем имя и фамилию 
        full_name = first_name + " " + last_name

        # Сгенерируйте возраст с помощью randint
        age = randint(18, 80)

        # Сгенерировать электронное письмо 
        email = data["results"][0]["email"]

        # Генерировать случайную профессию
        profession = professions[randint(0, len(professions)-1)]

        # Сгенерировать номер телефона
        phone = data["results"][0]["phone"]

        # Вставьте информацию о человеке в таблицу
        cursor.execute("INSERT INTO users(name, age, email, profession, phone) VALUES\
            (%s, %s, %s, %s, %s)", (full_name, age, email, profession, phone))

        # Зафиксируйте изменения в базе данных
        connection.commit()

        # Добавляем информацию о людях в список
        people_list.append({
            "name": full_name, 
            "age": age, 
            "email": email, 
            "profession": profession, 
            "phone": phone
            })

    # Закройте курсор и соединение
    cursor.close()

    # Закрыть connection
    connection.close()
    return people_list
print(generate_person(500)) 





