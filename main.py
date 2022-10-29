# Copyright 2022 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
import re
import json
import base64
from flask import Flask, render_template, request, redirect, url_for, flash
from google.cloud import bigquery

app = Flask(__name__)

bigquery_client = bigquery.Client()


def getDataType(value):
    if type(value)==float:
        return "FLOAT64"
    elif type(value)==int:
        return "INT64"
    elif type(value)==bool:
        return "BOOL"
    else:
        return "STRING"


def bqCreateDataset(dataset_id):
    try:
        dataset_id = f'{bigquery_client.project}.{dataset_id}'
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        dataset = bigquery_client.create_dataset(dataset, timeout=30)
        return f'Created dataset {bigquery_client.project}.{dataset.dataset_id}'
    except Exception as e:
        return f'{e}'


def bqCreateTable(dataset_id, table_name, payload):
    try:
        table_id = f'{bigquery_client.project}.{dataset_id}.{table_name}'
        
        schema = []
        for k,v in payload.items():
            dataType = getDataType(v)
            schema.append( bigquery.SchemaField(k, dataType) )
        
        table = bigquery.Table(table_id, schema=schema)
        table = bigquery_client.create_table(table)
        return f'Created table {bigquery_client.project}.{dataset_id}.{table_name}'
    except Exception as e:
        return f'{e}'


def bqInsertData(dataset_id, table_name, payload):
    try:
        table_id = f'{bigquery_client.project}.{dataset_id}.{table_name}'
        
        rows_to_insert = [payload]
        
        errors = bigquery_client.insert_rows_json(table_id, rows_to_insert)
        if errors == []:
            return f"New rows have been added."
        else:
            return f"Encountered errors while inserting rows: {errors}"
    except Exception as e:
        return f'{e}'    


def bqQuery(dataset_id, table_name, payload):
    try:
        query = """
            SELECT name, SUM(number) as total_people
            FROM `bigquery-public-data.usa_names.usa_1910_2013`
            WHERE state = 'TX'
            GROUP BY name, state
            ORDER BY total_people DESC
            LIMIT 20
        """
        query_job = bigquery_client.query(query)  # Make an API request.
        
        print("The query data:")
        for row in query_job:
            # Row values can be accessed by field name or index.
            print("name={}, count={}".format(row[0], row["total_people"]))
    except Exception as e:
        return f'{e}'

#############################################################
#
#   Routes
#
#############################################################

@app.route("/test", methods = ['GET'])
def test():
    return f'Test Successful!', 200

@app.route("/dataset", methods = ['GET','POST'])
def dataset():
    if request.method == 'GET':
        args = request.args
        print(f'args: {args}')
        
        if 'create' in args:
            msg = bqCreateDataset(args.get('create'))
            return msg, 200

@app.route("/table", methods = ['GET','POST'])
def table():
    if request.method == 'POST':
        try:
            requestPayload = request.get_json()
            
            dataset_id = requestPayload['dataset']
            table_name = requestPayload['table']
            payload    = requestPayload['payload']
            
            msg = bqCreateTable(dataset_id, table_name, payload)
            return msg, 200
        except Exception as e:
            return f'{e}', 400


@app.route("/insert", methods = ['GET','POST'])
def insert():
    if request.method == 'POST':
        try:
            requestPayload = request.get_json()
            
            dataset_id = requestPayload['dataset']
            table_name = requestPayload['table']
            payload    = requestPayload['payload']
            
            msg = bqInsertData(dataset_id, table_name, payload)
            return msg, 200
        except Exception as e:
            return f'{e}', 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
