import json
from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

def login():
    loginUrl = 'https://cses.fi/login'
    response = requests.get(loginUrl)
    soup = BeautifulSoup(response.content, 'html.parser')

    csrf_token_input = soup.find('input', {'name': 'csrf_token'})['value']
    csrf_token_cookie = response.cookies.get_dict()['PHPSESSID']

    # print("csrf_token_input", csrf_token_input, len(csrf_token_input))
    # print("csrf_token_cookie", csrf_token_cookie, len(csrf_token_cookie))

    data = {
        'csrf_token': csrf_token_input,
        'nick': os.getenv('USERNAME'),
        'pass': os.getenv('PASSWORD'),
    }

    cookies = { 'PHPSESSID': csrf_token_cookie }

    loginResponse = requests.post(loginUrl, data=data, cookies=cookies)

    return csrf_token_cookie

@app.route('/', methods=['GET'])
def get_users_info():
    try:
        user_ids = request.args.get('user_ids').split(';')
    except:
        user_ids = []

    csrf_token_cookie = login()
    cookies = { 'PHPSESSID': csrf_token_cookie }

    data = []

    for user_id in user_ids:
        userUrl = f'https://cses.fi/problemset/user/{user_id}/'
        userResponse = requests.get(userUrl, cookies=cookies)

        soup = BeautifulSoup(userResponse.content, 'html.parser')

        username = soup.find_all('h2')[0].text.split(' ')[-1]
        solved_tasks = soup.find_all('p')[0].text.split(' ')[-1].split('/')[0]
        
        aux = {}

        aux['id'] = user_id
        aux['username'] = username
        aux['number_of_questions'] = solved_tasks

        data.append(aux)

    return jsonify(data)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404

@app.route('/test')
def test():
    return 'Test'

if __name__ == '__main__':
   app.run(port=5000)
