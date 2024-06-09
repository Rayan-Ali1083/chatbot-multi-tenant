import json

import joblib
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from core.config import INPUT_EXAMPLE
from services.predict import ChromaHandlerScore as db
from models.prediction import (
    HealthResponse,
    MachineLearningResponse,
    MachineLearningDataInput,
)
from loguru import logger
data_router = APIRouter()



@data_router.post(path='/create',name='createOrgCollection')
async def create_collection(input : dict):
    try:
        db.get_knowledge_base().upload(input['bucket_name'],input['collection_name'])
        return True
    except Exception as e:
        logger.error(e)



@data_router.post(path='/delete_docs',name='deleteDocsCollection')
async def delete_docs(input: dict):
    try:
        ids,_=db.query(input["collection_name"],input["text"],input["top_k"])
        db.get_knowledge_base().delete_doc(ids,input["collection_name"])
        return True
    except Exception as e:
        logger.error(e)

@data_router.post(path='/delete',name='deleteOrgCollection')
async def delete(input:dict):
    try:
        db.get_knowledge_base().delete_collection(input["collection_name"])
        return True
    except Exception as e:
        logger.error(e)


@data_router.post(path='/add_docs',name='addDocsCollection')
async def add_docs(input : dict):
    try:
        db.get_knowledge_base().upload_files(input["files"],bucket_name=input["bucket_name"],collection_name=input["collection_name"])
        return True
    except Exception as e:
        logger.error(e)

@data_router.post(path='/add_doc',name='addDocsCollection')
async def add_doc(input:dict):
    try:
        db.get_knowledge_base().upload_doc(text=input["text"],collection_name=input["collection_name"])
        return True
    except Exception as e:
        logger.error(e)


@data_router.get('/search')
async def return_docs(query: str, collection_name: str,top_k : int):
    try:
        # logger.info(data_input)
        # data = jsonable_encoder(data_input)
        logger.info(f"query: {query}, collection_name: {collection_name}, top_k: {top_k} ")
        ids,context=db.get_knowledge_base().query(query,collection_name,top_k)
        return {"ids":ids,"context":context}
    except Exception as e:
        logger.error(e)

@data_router.get(path='/get_collection',name='getOrgCollection')
async def get_collection(collection_name: str, limit : int):
    try:
        logger.info(input)
        return db.get_knowledge_base().get_peek_collection(collection_name=collection_name,limit=limit)
    except Exception as e:
        logger.error(e)