# Установка контейнера 3X-UI + Traefik + Telegram Bot
Инструкция будет включать в себя:

1.  Установка контейнера 3X-UI + Traefik + Telegram Bot
2.  Настройка

Для установки понадобится:

1.  **VPS или иной сервер с доступом к консоли SSH**
2.  **1 ГБ ОЗУ**
3.  **Debian не ниже версии 9 или Ubuntu не ниже 20.04 (инструкция может работать и на других дистрибутивах, но некоторые детали будут отличатся)**

Официальный репозиторий 3X-UI: [https://github.com/MHSanaei/3x-ui](https://github.com/MHSanaei/3x-ui)

Официальный репозиторий форка X-UI: [https://github.com/alireza0/x-ui](https://github.com/alireza0/x-ui)

Скачиваем скрипт, делаем файл исполняемым и запускаем установку:

    curl -sSL https://raw.githubusercontent.com/torikki-tou/team418/main/setup.sh -o setup.sh && chmod +x setup.sh && ./setup.sh

Скрипт запросит у вас:

Имя пользователя для панели администратора - "Enter username for 3X-UI Panel"

Пароль администратора - "Enter password"

Порт подключения к панели администратора - "Enter port on which 3X-UI would be available: "

имя хоста (домен) или IP если домен отсутствует "Enter your hostname:"

Ваш адрес почты для сертификата LetsEncrypt "Enter your e-mail for certificate:"

API токен вашего телеграм бота (подробнее [тут](https://medium.com/geekculture/generate-telegram-token-for-bot-api-d26faf9bf064)) "Enter your Telegram bot API token:"

Имя пользователя Telegram администратора - "Enter your Telegram admin profile"

Также сервер спросит хотите ли вы заменить таблицу inbounds (она содержит данные о клиентах и конфигурациях прокси, по умолчанию пустая) - первый запуск скрипта заменяет пустую таблицу, последующий запуск заменит данные на дефолтную конфигурацию с Vless XTLS-Reality, порт 443.

По завершении работы скрипт выдаст адрес подключения к панели администратора.

3X-UI, Traefik и Telegram бот установлены и работают.

Для настройки через Веб UI:

Для 3X-UI переходим по адресу _https://yourIPorDomain:PORT,_ где yourIPorDomain - IP-адрес вашего сервера или доменное имя, если оно у вас есть и настроено

Для настройки через Telegram Бота:
От администратора:
1. Перейдите в вашего бота Telegram
2. Запустите команду /start
![](https://telegra.ph/file/77b2a279581c21fd8b5db.png)
3. Для добавления пользователя - Добавить юзера
4. Ввести имя пользователя (без @)
5. ввести количество устройств с которых пользователь может одновременно подключаться

Для настройки клиентов через админскую панель:

![](https://telegra.ph/file/7eb8f8013da91cfbfebe0.png)
 Выбираем Меню
![](https://telegra.ph/file/d085c978b3c622d54a875.png)
Добавить пользователя
![](https://telegra.ph/file/d2721d1ed8a72f8398b45.png)
Меняем необходимые данные или оставляем по умолчанию (ID должен соответствовать формату UUID)
![](https://telegra.ph/file/12f1372bb3b3239746968.png)
Ограничение по IP - количество одновременно подключенных устройств по данному пользователю
Flow - xtls-rprx-vision
Общий расход - ограничение расхода (при превышении необходимо будет сбросить счетчик трафика)
Срок действия конфигурации (Дата окончания) - дата истечения конфигурации (будет деактивирована, но не удалена)
![](https://telegra.ph/file/e97259146bedf9ce7394c.png)
по значку QR - отобразить QR Код для подключения, который можно отсканировать камерой в мобильных клиентах ([v2rayNG](https://github.com/2dust/v2rayNG/releases) или [Nekobox](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases) на Android, [Wings X](https://apps.apple.com/us/app/wings-x/id6446119727)/[FoXray](https://apps.apple.com/us/app/foxray/id6448898396) или [Shadowrocket](https://apps.apple.com/us/app/shadowrocket/id932747118) на iOS)
![](https://telegra.ph/file/9120e5869e7e5dd352357.png)
по значку I (info) - информация о подключении и ссылка на конфиг (vless://)

Также по кнопке "Меню" можно сбросить счетчики трафика, добавить пользователей (в том числе сгенерировать разом N аккаунтов по шаблону).
