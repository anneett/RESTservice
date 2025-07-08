import sys
import os
from fastapi import FastAPI, UploadFile, Form

root = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(root)
sys.path.append(os.path.join(root, 'antiplagiat_nii'))

from antiplagiat_nii.main import AntiplagiatClient
from antiplagiat_nii.libs.schemas import *
from antiplagiat_nii.libs.logger import *

app = FastAPI(title="Antiplagiat swagger")

client = AntiplagiatClient(
    login="testapi@antiplagiat.ru",
    password="testapi",
    company_name="testapi"
)

@app.post("/add")
def add_to_index(
        file: UploadFile,
        author_surname: str = Form(""),
        author_other_names: str = Form(""),
        external_user_id: str = Form("")
):
    doc_id = client.add_to_index(
        file.filename,
        author_surname=author_surname,
        author_other_names=author_other_names,
        external_user_id=external_user_id,
        custom_id="original"
    )
    return doc_id

@app.get("/check_from_id")
def check_document(doc_id: int):
    doc_id_obj = client.factory.DocumentId(Id=doc_id, External=None)
    report = client.check_by_id(doc_id_obj)
    return report

@app.post("/add_and_check")
def add_and_check(file: UploadFile,
                  author_surname: str = Form(""),
                  author_other_names: str = Form(""),
                  external_user_id: str = Form("")):

    doc_id = client.add_to_index(
        file.filename,
        author_surname=author_surname,
        author_other_names=author_other_names,
        external_user_id=external_user_id,
        custom_id = "original"
    )

    report = client.check_by_id(doc_id)

    return {"doc_id": doc_id, "report": report}