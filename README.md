# Решения задач от **FOUNDER**

## Названия проектов и описание 

Здесь представлено 2 проекта:

 - Quiz - телеграмм приложение, которое запускается main.py файлом в папке. Телеграм предоставляет 3 кнопки-команды: Начать квиз, продолжить квиз(Работает даже, если вы играете впервые - просто начинаете с первого вопроса), Статистика(всех игроков). 

 - Future для будущего. (Учился делать виртуальные окружения в multi-root проектах vsCode с автозапуском окружений. Работает через раз. Фаил конфигурации проекта остался.)

 - Ещё корневой фаил представлен проектом для удобной работой с gitignore и readme.md

## Подробноеописание структуры проектов

### Quiz

 - **Card** сборник модели для работы с картами
    - card.py модель карточки с вопросом для квиза: айди, вопрос, неверные ответы и верный.
    - deck.json - данные для составления карт
    - deck.py - объект для управления колодой карт
 - **User** сборник модели для User
    - user.py модель пользователя игры: айди, текущий вопрос, текущее кол-во верных вопросов, лучшее кол-во за всё время, кол-во прохождения квиза
    - userDB.py объект для работой с базой данных. Присутсвует объект для инверсии зависимостей, т.к. проект изначально перестараивал из консольного.
    - user.db - sqlite база данных синформацией о пользователях
 - **Services** SQLiteDataBase.py - родительская модель для работы SQLite. Автоматически собирает столбцы таблицы для переданных целевых объектов, а также предоставляет объект таблицу, которой дальше и пользуется userDB для получиения, изменения и создания данных в базе.
 - **quiz.py** - бизнес-логика проекта и буфер для связи между представлением и данными.
 - **main.py** - Работа с API проекта и **точка входа в проект**
 - **requirements.txt** - список зависимостей проекта Quiz