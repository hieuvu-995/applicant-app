import random
import requests
import string
import datetime
import time
from faker import Faker


country_list = ['United States', 'Vietnam', "Singapore"]
lst_dct = []

for i in range(50):
    fake = Faker()
    name = ''.join(random.choices(string.ascii_letters, k=8))
    start_date = datetime.date(year=1995, month=1, day=1)
    dob = fake.date_between(start_date=start_date, end_date='-18y').strftime('%Y-%m-%d')
    email = ''.join(random.choice(string.ascii_letters) for _ in range(8)) + "@gmail.com"
    country = random.choice(country_list)
    dct = {
        "name": name,
        "dob": dob,
        "email": email,
        "country": country,
    }
    lst_dct.append(dct)
start = time.time()
for i in range(len(lst_dct)):
    api_url = "http://127.0.0.1:8000/admin/applicant/"
    todo = lst_dct[i]
    response = requests.post(api_url, json=todo)
end = time.time()
print("Total time to processing 1000 requests via API: ", end - start)
