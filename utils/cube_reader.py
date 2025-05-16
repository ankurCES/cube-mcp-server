import json
import datetime
import requests
import json
import jwt

ENV_VAR = json.load(open('env.json'))

CUBE_SECRET = ENV_VAR['CUBE_SECRET']
ACT_OPTIONS = ENV_VAR['ACT_OPTIONS']
CUBE_API_URL = ENV_VAR['CUBE_API_URL']

QUERY_PAYLOAD = ENV_VAR['QUERY_PAYLOAD']


def run_tags(plant_code, token, tag_list, cube_agg, start_date, end_date, valueType, granularity):

    query = json.dumps(QUERY_PAYLOAD)    
    query = query.replace("<START_DATE>", start_date)
    query = query.replace("<END_DATE>", end_date)
    query = query.replace("<PLANT_CODE>", plant_code)
    query = query.replace("<CUBE_AGG>", cube_agg)
    query = query.replace("<TAG_NAME>", ",".join(map(str, tag_list)))

    query = query.replace("<VALUE>", valueType)
    query = query.replace("<GRANULARITY>", granularity)
    
    url = "{}/load?query={}&queryType=multi".format(CUBE_API_URL, query)

    
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    response = requests.request("GET", url, headers=headers)

    data = response.json()

    try:
        result_obj = data['results'][0]['data']
        cleaned_result = {}
        for tag_val in result_obj:
            tagName = tag_val['{}{}.tagName'.format(plant_code, cube_agg)]
            timestamp = tag_val['{}{}.timestamp'.format(plant_code, cube_agg)]
            value = tag_val['{}{}.{}'.format(plant_code, cube_agg, valueType)]
            try:
                cleaned_result[tagName][timestamp] = value
            except KeyError as e:
                cleaned_result[tagName] = {}
                cleaned_result[tagName][timestamp] = value
        return cleaned_result
    except Exception as e:
        pass
    return None

def generate_signed_cube_tokens(plant_list,environment):
    cube_token_list = {}
    for plant_code in plant_list:
        payload = {
		    'plant_name': plant_code,
        }
        cube_token_list[plant_code] = jwt.encode(payload=payload, key=CUBE_SECRET[environment], algorithm="HS256")
    return cube_token_list

def __task_runner(plant_list, partial_tag_match_list, environment, cube, start_date, end_date, valueType, granularity):
    result_set = []
    cube_token = generate_signed_cube_tokens(plant_list, environment)
    for plant_code in plant_list:
        token = cube_token[plant_code]
        result = run_tags(plant_code, token, partial_tag_match_list, cube, start_date, end_date, valueType, granularity)
        result_set.append(result)
    return result_set


def main_runner(plants, environment, tag_list, days_delta):
    plant_list = plants.split(',')
    tag_match_list = tag_list.split(',')

    act_option = ''
    action_act_option = ''
    valueType = ''
    granularity = ''


    if days_delta <= 14 and days_delta > 0:
        # Number of days to go back
        act_option = 'Five'
        action_act_option = 'ActFive'
        valueType = 'lastValue'
        granularity = 'minute'
    elif days_delta <= 30 and days_delta > 14:
        act_option = 'Hourly'
        valueType = 'avgValue'
        granularity = 'hour'
        action_act_option = 'ActHour'
    elif days_delta > 30:
        act_option = 'Daily'
        valueType = 'avgValue'
        granularity = 'day'
        action_act_option = 'ActDaily'


    start_date = (datetime.datetime.now() - datetime.timedelta(days=days_delta)).isoformat()
    end_date = datetime.datetime.now().isoformat()

    results = __task_runner(plant_list, tag_match_list, environment, ACT_OPTIONS[act_option], start_date, end_date, valueType, granularity)
    return results

