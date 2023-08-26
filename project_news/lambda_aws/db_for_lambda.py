import boto3
import pandas as pd
import os
from dotenv import load_dotenv


from abc import ABC, abstractmethod
from typing import Iterable, List
from datetime import datetime


load_dotenv()


class DBClient(ABC):

    @staticmethod
    @abstractmethod
    def to_bd(information: List):
        pass

    @staticmethod
    @abstractmethod
    def get_from_bd(table_name: str) -> pd.DataFrame:
        pass

    @staticmethod
    def to_error(name: str, error: Exception):
        with open('../db_errors.txt', 'a') as f:
            f.write(f'{name}, {error}, {datetime.now()}\n')


class DynamoDBClient(DBClient):

    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    dynamodb_client = boto3.client('dynamodb', region_name='eu-west-2')
    dynamodb_resource = session.resource('dynamodb', region_name='eu-west-2')
    data_types = {
        'str': 'S',
        'number': 'N',
        'binary': 'B',
        'bool': 'BOOL',
        'null': 'NULL',
        'str_set': 'SS',
        'number_set': 'NS',
        'binary_set': 'BS',
        'list': 'L',
        'map': 'M'
    }

    @staticmethod
    def to_bd(information: List):
        if isinstance(information, Iterable):
            table_name = information[0].__class__.__name__
            table = DynamoDBClient.dynamodb_resource.Table(table_name)
            with table.batch_writer() as batch:
                for obj in information:
                    try:
                        item = {attribute: value for attribute, value in vars(obj).items()}
                        batch.put_item(Item=item)
                    except Exception as e:
                        print(e)
                        DBClient.to_error('DynamoDBClient.to_bd()', e)

    @staticmethod
    def get_from_bd(table_name: str) -> pd.DataFrame:
        try:
            table = DynamoDBClient.dynamodb_resource.Table(table_name)
            response = table.scan()
            items = response['Items']

            while 'LastEvaluatedKey' in response:
                last_key = response['LastEvaluatedKey']
                response = table.scan(ExclusiveStartKey=last_key)
                items.extend(response['Items'])

            df = pd.DataFrame(items)
            return df
        except Exception as e:
            DBClient.to_error('DynamoDBClient', e)
