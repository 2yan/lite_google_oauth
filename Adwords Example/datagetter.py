import pandas as pd
import requests
from author import Author
import json

doc = Author(scope=['https://www.googleapis.com/auth/analytics.readonly'])
url = 'https://analyticsreporting.googleapis.com/v4/reports:batchGet'


last_response = None

def get_headers():
    global doc
    headers = {'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(doc.sign({})['access_token'])}
    return headers


def make_google_json(start_date, end_date, view_id, metrics, dimensions, segmentid, next_token=False):
    data = {'reportRequests': []}

        
    temp = [
        {
            "viewId": view_id,
            "dateRanges": [{"startDate": start_date, "endDate": end_date}],
            "metrics": [],
            "dimensions":[],
            "includeEmptyRows": "true",
            "hideTotals": 'true'
        }
    ]
    
    if segmentid:
        dimensions.append('ga:segment')
        temp[0]['segments'] = [{'segmentId':segmentid}]
        
    for metric in metrics:
        temp[0]['metrics'].append({'expression':metric})
        
        
    for dimension in dimensions:
            temp[0]['dimensions'].append({'name':dimension})

    if next_token != False:
        temp[0]['pageToken'] = next_token


    data['reportRequests'].append(temp)
    return data


def get(data):
    headers = get_headers()
    r = requests.post(url, data=data, headers=headers)
    global last_response
    last_response = r
    return r.json()



def get_data(start_date, end_date, view_id, metric, dimension, segmentid, next_token=False):
    data = make_google_json(start_date, end_date, view_id, metric, dimension, segmentid, next_token)
    data = json.dumps(data)
    return get(data)


def to_english(result_in):
    
    try:
        result = result_in['reports'][0]
    except KeyError:
        raise ValueError(str(result_in))
    dimensions = result['columnHeader']['dimensions']
    metrics = result['columnHeader']['metricHeader']['metricHeaderEntries']
    metrics = [x['name'] for x in metrics]
    
    final = pd.DataFrame()

    i = 0
        
    if 'rows' not in result['data'].keys():
        global last_response
        print(last_response.text)
        raise ValueError('No data returned for this query : \n{}'.format(str(result)))
    
    for row in result['data']['rows']:
                    
        for temp in zip(dimensions,row['dimensions'] ):
            final.loc[i, temp[0]] = temp[1]

        for temp in zip(metrics,row['metrics'][0]['values'] ):
            final.loc[i, temp[0]] = temp[1]    

        
        i = i + 1


    return final


def get_next_page_token(data):
    try:
        return data['reports'][0]['nextPageToken']
    except KeyError:
        return False


def full_get(start_date, end_date, view_id, metric, dimension, segment_id):
    done = False
    next_token = False

    results = []
    while not done:
        print('Downloading: Next Token = {}'.format(next_token))
        result = get_data(start_date, end_date, view_id, metric, dimension, segment_id, next_token)
        next_token = get_next_page_token(result)
        results.append(result)
        if next_token == False:
            done = True

    final = []
    for result in results:
        final.append(to_english(result))

    df = pd.DataFrame(columns=final[0].columns)
    df.index.name = final[0].index.name
    for thing in final:
        df = df.append(thing)

    return df




def get_segments():
    headers = get_headers()
    x = requests.get('https://www.googleapis.com/analytics/v3/management/segments', headers = headers)
    global last_response
    last_response = x
    x = x.json()
    x = x['items']
    x = pd.DataFrame(x)
    x.set_index('segmentId', inplace = True)
    return x