import logging
import requests
import yaml
import time
import datetime


def login(url, user_name, password):
    payload = {
        "username": user_name,
        "password": password
    }
    url = f'{url}/login'
    return requests.post(url, data=payload)


def logout(token, url):
    url = f'{url}/logout'
    return requests.post(url, data=token)


def create_rosters(team, token, url):
    roster = {
        "name": f"roster-{team}"
    }
    logging.info(roster)
    return requests.post(f"{url}/api/v0/teams/{team}/rosters",
                         json=roster,
                         cookies=token.cookies.get_dict(),
                         headers={'X-CSRF-TOKEN': token.json().get('csrf_token')})


def create_team(name, scheduling_timezone, email, slack_channel, token, url):
    team = {
        'name': name,
        'scheduling_timezone': scheduling_timezone,
        'email': email,
        'slack_channel': slack_channel
    }
    logging.info(team)
    return requests.post(f"{url}/api/v0/teams",
                         json=team,
                         cookies=token.cookies.get_dict(),
                         headers={'X-CSRF-TOKEN': token.json().get('csrf_token')})


def create_user(user_name, token, url):
    user = {
        "name": user_name
    }
    logging.info(user)
    return requests.post(f"{url}/api/v0/users",
                         json=user,
                         cookies=token.cookies.get_dict(),
                         headers={'X-CSRF-TOKEN': token.json().get('csrf_token')})


def add_user_roster(user, team, token, url):
    names = {
        "name": f"{user}"
    }
    return requests.post(f"{url}/api/v0/teams/{team}/rosters/roster-{team}/users",
                         json=names,
                         cookies=token.cookies.get_dict(),
                         headers={'X-CSRF-TOKEN': token.json().get('csrf_token')})


def add_info_user(call, email, name, full_name, token, url):
    info = {
        "contacts": {
            "call": call,
            "email": email,
            "sms": call
        },
        "name": name,
        "full_name": full_name,
    }
    logging.info(info)
    return requests.put(f"{url}/api/v0/users/{name}",
                        json=info,
                        cookies=token.cookies.get_dict(),
                        headers={'X-CSRF-TOKEN': token.json().get('csrf_token')})


def read_yaml(file_path):
    with open(file_path) as fh:
        read_data = yaml.load(fh, Loader=yaml.FullLoader)
    return read_data


def create_event(date, user, team, role, token, url):
    date_time = list(map(int, date.split("/")))
    start = datetime.datetime(date_time[2], date_time[1], date_time[0], 0, 0, 0)
    end = datetime.datetime(date_time[2], date_time[1], date_time[0], 23, 59, 59)
    event = {
        "start": time.mktime(start.timetuple()),
        "end": time.mktime(end.timetuple()),
        "user": user,
        "team": team,
        "role": role,
    }
    return requests.post(f"{url}/api/v0/events",
                         json=event,
                         cookies=token.cookies.get_dict(),
                         headers={'X-CSRF-TOKEN': token.json().get('csrf_token')})


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
config = read_yaml('config.yaml')
teams = read_yaml(config['yaml']['file'])['teams']
token = login(config['oncall']['url'], config['oncall']['user_name'], config['oncall']['password'])
for i in range(len(teams)):
    logging.info(f"Create Team:{create_team(teams[i]['name'],teams[i]['scheduling_timezone'],teams[i]['email'],teams[i]['slack_channel'], token, config['oncall']['url'])}")
    logging.info(f"Create Roster In Team:{create_rosters(teams[i]['name'], token, config['oncall']['url'])}")
for i in range(len(teams)):
    userinfo = teams[i]['users']
    for j in range(len(userinfo)):
        logging.info(f"Create User:{create_user(userinfo[j]['name'], token, config['oncall']['url'])}")
        logging.info(f"Add User Info:{add_info_user(userinfo[j]['phone_number'], userinfo[j]['email'], userinfo[j]['name'], userinfo[j]['full_name'], token, config['oncall']['url'])}")
        logging.info(f"Add User In Roster:{add_user_roster(userinfo[j]['name'], teams[i]['name'], token, config['oncall']['url'])}")
        duty = teams[i]['users'][j]['duty']
        for k in range(len(duty)):
            logging.info(f"Create event :{create_event(duty[k]['date'], userinfo[j]['name'], teams[i]['name'], duty[k]['role'], token, config['oncall']['url'])}")
logging.info(f"LogOut:{logout(token, config['oncall']['url'])}")
