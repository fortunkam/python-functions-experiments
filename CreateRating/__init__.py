import logging
import json
import requests
import uuid

import azure.functions as func


def main(req: func.HttpRequest, rating: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    requestData = req.get_json()
    userId = requestData.get('userId')
    productId = requestData.get('productId')
    ratingValue = requestData.get('rating')

    if not isUserValid(userId):
        return func.HttpResponse(
            "User Id is not valid",
            status_code=400
        )

    if not isProductValid(productId):
        return func.HttpResponse(
            "Product Id is not valid",
            status_code=400
        )

    if not isRatingValid(ratingValue):
        return func.HttpResponse(
            "Rating is not valid",
            status_code=400
        )

    rowKey = str(uuid.uuid4())

    data = {
        "PartitionKey": userId,
        "RowKey" : rowKey,
        "ProductId" : productId,
        "LocationName" : requestData.get('locationName'),
        "Rating" : ratingValue,
        "UserNotes" : requestData.get('userNotes'),
    }

    rating.set(json.dumps(data))

    return func.HttpResponse(
        json.dumps(data),
        status_code=200
    )    

def isUserValid(userId: str) -> bool:
    r=requests.get(f'https://serverlessohuser.trafficmanager.net/api/GetUser?userId={userId}')
    return r.status_code == 200

def isProductValid(productId: str) -> bool:
    r=requests.get(f'https://serverlessohproduct.trafficmanager.net/api/GetProduct?productId={productId}')
    return r.status_code == 200

def isRatingValid(rating: int) -> bool:
    return rating > 0 and rating < 5