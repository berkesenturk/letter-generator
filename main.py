import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from fastapi import FastAPI
from pydantic import BaseModel
import json
from typing import List,Dict
import logging


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG) 

# get letter first then find the words with brackets and replace them. brackets can be only squared for now.

# todos

# mail temp. priority: low
# deploy to cloud: mid

# Models


class CoverLetterRequest(BaseModel):
    letter: str
    args: Dict[str, str]

class CoverLetterResponse(BaseModel):
    letter: str

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})
class Item(BaseModel):
    text: str

@app.post("/")
async def root(data: Item):
    return {"message": f"You wrote: '{data.text}'"}

@app.post("/coverletter")
async def generate_cover_letter(body: CoverLetterRequest):
    
    loaded_body = json.loads(body.json())
    # logger.info(f"req before load: {str(loaded_body.keys())}")
    result = build_letter(loaded_body)

    # send email

    send_email_to_user(result, loaded_body['args'])
    return result


def build_letter(body):
    
    result_letter = "" 
    # replace
    if 'args' in body.keys():
        result_letter = replace_arguments_with_values(body['letter'], body['args'])
        
        return result_letter
    else:
        return 0


def replace_arguments_with_values(letter, generic_arguments):

    # find_occurences
    # logger.info(letter.index('\n'))
    changed_letter = letter 
    for index, argument in enumerate(generic_arguments):
        if index != 0:
            changed_letter = changed_letter.replace(f'[{argument}]', generic_arguments[argument])
        else:
            changed_letter = letter.replace(f'[{argument}]', generic_arguments[argument])

    changed_letter = changed_letter.replace("\n", "<br>")
    return changed_letter

def send_email_to_user(letter, generic_arguments):
    msg ="<!DOCTYPEhtml><html><head><style>table{font-family:arial,sans-serif;}td,th{border:1pxsolid#dddddd;text-align:left;padding:8px;}tr:nth-child(even){background-color:#dddddd;}</style></head>"

    msg += letter
    logger.info(letter, generic_arguments)

    # company_name = generic_arguments[[argument for index, argument in enumerate(generic_arguments) if argument == 'Company Name'][0]]
    # job_title = generic_arguments[[argument for index, argument in enumerate(generic_arguments) if argument == 'Job Position'][0]]
                                
    mail_provider = Mail_Provider("jobupdatesfromeumetsat@gmail.com", 
                                  "scjpagonkjqozalo", 
                                  "berkesenturk11@gmail.com", 
                                  # f"Your cover letter for company: {company_name} as role: for {job_title}", 
                                  "Your cover letter is ready!",
                                  msg)

    mail_provider.build_message()
    mail_provider.send_mail()







class Mail_Provider:
    def __init__(self, sender, password, receiver, subject, body):
        self.sender = sender
        self.password = password
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.message = ""
    
    def build_message(self):
        message = MIMEMultipart()
        message["from"] = self.sender
        message["to"] = self.receiver
        message["subject"] = self.subject

        message.attach(MIMEText(self.body, "html"))

        self.message = message.as_string()

    
    def send_mail(self):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = ssl.create_default_context()) as server:
            server.login(self.sender, self.password)
            errors = server.sendmail(self.sender, self.receiver, self.message)

            print("Successfully delivered") if len(errors) == 0 else print("Something terrible happend while sending mail")

