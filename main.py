from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import sys, os
root = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(root)
sys.path.append(os.path.join(root, 'antiplagiat_nii'))
from antiplagiat_nii.libs.schemas import *
from antiplagiat_nii.main import AntiplagiatClient

# from libs.schemas import SimpleCheckResult, Service, Source, Author, LoanBlock
from antiplagiat_nii.libs.logger import logger

app = FastAPI()

client = AntiplagiatClient(
    login="testapi@antiplagiat.ru",
    password="testapi",
    company_name="testapi"
)


@app.get("/check")
def check_document(doc_id: int):
    doc_id_obj = client.factory.DocumentId(Id=doc_id, External=None)
    report = client.check_by_id(doc_id_obj)
    return report


@app.post("/add")
def add_to_index(filename: str, author_surname: str = '',
                 author_other_names: str = '',
                 external_user_id: str = 'ivanov',
                 custom_id: str = 'original'):

    doc_id = client.add_to_index(
                    filename,
                    author_surname=author_surname,
                    author_other_names=author_other_names,
                    external_user_id=external_user_id,
                    custom_id = "original"
                )
    return doc_id