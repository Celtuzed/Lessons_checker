# Lessons checker

Данный телеграмм бот создан для присылания результатов проверки уроков с сайта [dvmn](https://dvmn.org/)

### Как установить

Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

Для запуска скрипта нужно ввести в консоль:

```
  Python3 main.py
```

### Переменные окружения

Для использования скрипта необходимо создать `.env` файл, и по примеру ввести все необходимые данные:
```
DVMN_TOKEN=.....
TG_TOKEN=.......
CHAT_ID=........
```  

-`DVMN_TOKEN` - Токен, который нужно будет получить во вкладке [API](https://dvmn.org/api/docs/), при регистрации на сайте [dvmn](https://dvmn.org/).
-`TG_TOKEN` - Токен бота, который можно получить при создании у [отца ботов](https://t.me/BotFather)
-`CHAT_ID` - ID чата с вами, который можно получить у [бота](https://t.me/userinfobot)
