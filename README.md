### Using the api

Example request:
```
https://<api_url>?user_ids=44736,69243
```

Example response:
```json
[
    {
        "id": "44736",
        "number_of_questions": "124",
        "username": "tilnoene"
    },
    {
        "id": "69243",
        "number_of_questions": "169",
        "username": "Lia"
    }
]
```

### Manual Install

You should create an `.env` like this:
```
USERNAME=cses_account_username
PASSWORD=cses_account_password
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

And then run the api:
```py
python ./app/index.py
```

### Docker

