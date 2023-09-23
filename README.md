# Скрипт для автоматизации добавления расписаний в Oncall Lincked In 

---

## Для запуска необходимо установить следующие библиоткеи:
````
pip install requests
pip install pyyaml
ppip install logging
````
---
## Назначение скрипта
Скрипт предназначен для распаршивания yaml файл,который содержит информацию :
* Команде 
* Дежурных
* Их расписание 

После того, как произошел анализ  файла, скрипт совершает запроосы на API  oncall для создания графика дежурст 
по командам и возвращете коды ответа сервера в py_log.log

---
## Пример конфигурационного файла config.yaml:
````
oncall:                            ## Секция настройки oncall
  url: 'http://localhost:8080'     ## Адрес до хоста oncall
  user_name: 'root'                ## Имя супер юзера для создания пользователей
  password: '1'                    ## Пароль пользователя
yaml:                              ## Секция yaml файла 
  file: 'teams.yaml'               ## Путь до файлай, которой принимает программа
````

## Пример входного  файла:
````
teams:
  - name: "k8s SRE"
    scheduling_timezone: "Europe/Moscow"
    email: "k8s@sre-course.ru"
    slack_channel: "#k8s-team"
    users:
      - name: "o.ivanov"
        full_name: "Oleg Ivanov"
        phone_number: "+1 111-111-1111"
        email: "o.ivanov@sre-course.ru"
        duty:
          - date: "02/10/2023"
            role: "primary"
          - date: "03/10/2023"
            role: "secondary"
          - date: "04/10/2023"
            role: "primary"
          - date: "05/10/2023"
            role: "secondary"
          - date: "06/10/2023"
            role: "primary"
      - name: "d.petrov"
        full_name: "Dmitriy Petrov"
        phone_number: "+1 211-111-1111"
        email: "d.petrov@sre-course.ru"
        duty:
          - date: "02/10/2023"
            role: "secondary"
          - date: "03/10/2023"
            role: "primary"
          - date: "04/10/2023"
            role: "secondary"
          - date: "05/10/2023"
            role: "primary"
          - date: "06/10/2023"
            role: "secondary"

  - name: "DBA SRE"
    scheduling_timezone: "Asia/Novosibirsk"
    email: "dba@sre-course.ru"
    slack_channel: "#dba-team"
    users:
      - name: "a.seledkov"
        full_name: "Alexander Seledkov"
        phone_number: "+1 311-111-1111"
        email: "a.seledkov@sre-course.ru"
        duty:
          - date: "02/10/2023"
            role: "primary"
          - date: "03/10/2023"
            role: "primary"
          - date: "04/10/2023"
            role: "primary"
          - date: "05/10/2023"
            role: "secondary"
          - date: "06/10/2023"
            role: "primary"
      - name: "d.hludeev"
        full_name: "Dmitriy Hludeev"
        phone_number: "+1 411-111-1111"
        email: "user-4@sre-course.ru"
        duty:
          - date: "02/10/2023"
            role: "secondary"
          - date: "03/10/2023"
            role: "secondary"
          - date: "04/10/2023"
            role: "vacation"
          - date: "05/10/2023"
            role: "primary"
          - date: "06/10/2023"
            role: "secondary"
````