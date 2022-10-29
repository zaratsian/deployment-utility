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

def bqCreateDataset(dataset_id):
    try:
        dataset_id = f'{bigquery_client.project}.{dataset_id}'
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        dataset = bigquery_client.create_dataset(dataset, timeout=30)
        return f'Created dataset {bigquery_client.project}.{dataset.dataset_id}'
    except Exception as e:
        return f'{e}'


def bqCreateTable(dataset_id, table_name):
    table_id = f'{bigquery_client.project}.{dataset_id}.{table_name}'
    
    schema = [
        bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
    ]
    
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )

#############################################################
#
#   Routes
#
#############################################################

@app.route("/test", methods = ['GET'])
def test():
    return f'Test Successful!', 200

@app.route("/create", methods = ['GET'])
def index():
    if request.method == 'GET':
        args = request.args
        print(f'args: {args}')
        
        if 'dataset' in args:
            msg = bqCreateDataset(args.get('dataset'))
        elif 'table' in args:
            print('table found')
        
        return msg, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
