import boto3
import pandas as pd


from abc import ABC, abstractmethod
from typing import Iterable, Dict, List
from datetime import datetime


class DBClient(ABC):

    @staticmethod
    @abstractmethod
    def to_bd(information: List):
        pass

    @staticmethod
    @abstractmethod
    def get_from_bd(table_name: str):
        pass

    @staticmethod
    def to_error(name: str, error: Exception):
        with open('db_errors.txt', 'a') as f:
            f.write(f'{name}, {error}, {datetime.now()}\n')


class PostgresClient(DBClient):

    @staticmethod
    def to_bd():
        pass

    @staticmethod
    def get_from_bd():
        pass


class DynamoDBClient(DBClient):

    dynamodb_client = boto3.client('dynamodb', region_name='eu-west-2')
    dynamodb_resource = boto3.resource('dynamodb', region_name='eu-west-2')
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
        flag = True
        if isinstance(information, Iterable):
            condition_expression = 'attribute_not_exists(title)'
            table_name = information[0].__class__.__name__
            table = DynamoDBClient.dynamodb_resource.Table(table_name)
            with table.batch_writer() as batch:
                for obj in information:
                    try:
                        item = {attribute: {DynamoDBClient.data_types[type(value).__name__]: value}
                                for attribute, value in vars(obj).items()}
                        batch.put_item(Item=item)
                    except Exception as e:
                        flag = False
                        DBClient.to_error('DynamoDBClient', e)
        return flag

    @staticmethod
    def get_from_bd(table_name: str) -> pd.DataFrame:
        try:
            response = DynamoDBClient.dynamodb_client.scan(TableName=table_name)
            items = response['Items']

            while 'LastEvaluatedKey' in response:
                last_key = response['LastEvaluatedKey']
                response = DynamoDBClient.dynamodb_client.scan(
                    TableName=table_name,
                    ExclusiveStartKey=last_key
                )
                items.extend(response['Items'])

            df = pd.DataFrame(items)
            return df
        except Exception as e:
            DBClient.to_error('DynamoDBClient', e)

