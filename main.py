from dotenv import load_dotenv
import os
from ticktick.oauth2 import OAuth2      
from ticktick.api import TickTickClient   
from datetime import datetime

load_dotenv()


CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
URI = os.environ.get("URI")
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")


auth_client = OAuth2(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     redirect_uri=URI)

client = TickTickClient(EMAIL, PASSWORD, auth_client)


def add_task_to_ticktick(title, task_description, start_time, end_time):
    start_time = datetime.strptime(start_time, "%Y-%m-%d-%H-%M")
    print(f"start_time: {start_time} {type(start_time)}")
    end_time = datetime.strptime(end_time, "%Y-%m-%d-%H-%M")
    print(f"end_time: {end_time} {type(end_time)}")

    task = client.task.builder(title,
                            startDate=start_time,
                            dueDate=end_time,
                            content=task_description)

    mollys_party = client.task.create(task)
