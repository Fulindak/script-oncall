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


def create_rosters(team, res, url):
    roster = {
        "name": f"roster-{team}"
    }
    print(roster)
    return requests.post(f"{url}/api/v0/teams/{team}/rosters",
                         json=roster,
                         cookies=res.cookies.get_dict(),
                         headers={'X-CSRF-TOKEN': res.json().get('csrf_token')})


def create_team(name, scheduling_timezone, email, slack_channel, res, url):
    team = {
        'name': name,
        'scheduling_timezone': scheduling_timezone,
        'email': email,
        'slack_channel': slack_channel
    }
    print(team)
    return requests.post(f"{url}/api/v0/teams",
                         json=team,
                         cookies=res.cookies.get_dict(),
                         headers={'X-CSRF-TOKEN': res.json().get('csrf_token')})


def create_user(user_name, res, url):
    user = {
        "name": user_name
    }
    print(user)
    return requests.post(f"{url}/api/v0/users",
                         json=user,
                         cookies=res.cookies.get_dict(),
                         headers={'X-CSRF-TOKEN': res.json().get('csrf_token')})


def add_user_roster(user, team, res, url):
    names = {
        "name": f"{user}"
    }
    return requests.post(f"{url}/api/v0/teams/{team}/rosters/roster-{team}/users",
                         json=names,
                         cookies=res.cookies.get_dict(),
                         headers={'X-CSRF-TOKEN': res.json().get('csrf_token')})


def add_info_user(call, email, name, full_name, res, url):
    info = {
        "contacts": {
            "call": call,
            "email": email,
            "sms": call
        },
        "name": name,
        "full_name": full_name,
    }
    print(info)
    return requests.put(f"{url}/api/v0/users/{name}",
                        json=info,
                        cookies=res.cookies.get_dict(),
                        headers={'X-CSRF-TOKEN': res.json().get('csrf_token')})


def read_yaml(file_path):
    with open(file_path) as fh:
        read_data = yaml.load(fh, Loader=yaml.FullLoader)
    return read_data


def create_event(date, user, team, role, res, url):
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
    print(user, role)
    return requests.post(f"{url}/api/v0/events",
                         json=event,
                         cookies=res.cookies.get_dict(),
                         headers={'X-CSRF-TOKEN': res.json().get('csrf_token')})


teams = read_yaml('teams.yaml')['teams']
config = read_yaml('config.yaml')
res = login(config['oncall']['url'], config['oncall']['user_name'], config['oncall']['password'])
for i in range(len(teams)):
    print(create_team(
        teams[i]['name'],
        teams[i]['scheduling_timezone'],
        teams[i]['email'],
        teams[i]['slack_channel'], res, config['oncall']['url']))
    print(create_rosters(teams[i]['name'], res, config['oncall']['url']))
for i in range(len(teams)):
    userinfo = teams[i]['users']
    for j in range(len(userinfo)):
        print(create_user(userinfo[j]['name'], res, config['oncall']['url']))
        print(add_info_user(userinfo[j]['phone_number'],
                            userinfo[j]['email'],
                            userinfo[j]['name'],
                            userinfo[j]['full_name'], res, config['oncall']['url']))
        print(add_user_roster(userinfo[j]['name'], teams[i]['name'], res, config['oncall']['url']))
        duty = teams[i]['users'][j]['duty']
        for k in range(len(duty)):
            print(create_event(duty[k]['date'], userinfo[j]['name'], teams[i]['name'], duty[k]['role'], res,
                               config['oncall']['url']))
