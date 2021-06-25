# Client Preparation



<br>

### Imports

```python
#exports
from tqdm import tqdm
from warnings import warn
from functools import reduce

from ElexonDataPortal.dev import rawgen, specgen, raw, utils
```

```python
from IPython.display import JSON
import pandas as pd
```

```python
import os
from dotenv import load_dotenv

assert load_dotenv('../.env'), 'Environment variables could not be loaded'

api_key = os.environ['BMRS_API_KEY']
```

```python
API_yaml = specgen.load_API_yaml(fp='../data/BMRS_API.yaml')

JSON(API_yaml)
```




    <IPython.core.display.JSON object>



```python
#exports
def test_endpoints(
    default_kwargs: dict
):
    methods_to_test = [func for func in dir(raw) if 'get_' in func]
    stream_to_df = dict()

    for method_to_test in tqdm(methods_to_test):
        method_func = getattr(raw, method_to_test)
        func_kwargs = dict(zip(method_func.__code__.co_varnames, method_func.__defaults__))

        for kwarg, value in default_kwargs.items():
            if kwarg in func_kwargs.keys():
                func_kwargs.update({kwarg: value})

        r = method_func(**func_kwargs)
        df = utils.parse_xml_response(r)

        stream_to_df[method_to_test.split('_')[1]] = df

    streams_without_content = []

    for stream, df in stream_to_df.items():
        if df.size == 0:
            streams_without_content += [stream]

    return streams_without_content
     
    if len(streams_without_content) > 0:
        warn(f"The following data streams returned no content data: {', '.join(streams_without_content)}")
        
    return stream_to_df
```

```python
default_kwargs = {
    'APIKey': api_key,
    'ServiceType': 'xml'
}

stream_to_df = test_endpoints(default_kwargs)
```

    100% 49/49 [00:35<00:00,  1.39it/s]
    

```python
#exports
def construct_method_to_params_dict(API_yaml):
    method_to_params = reduce(lambda k, v: {**k, **v}, [
        {
            f'{k}_{rawgen.clean_path_name(stream)}': {
                parameter['name']: rawgen.extract_parameter_example(parameter) 
                for parameter 
                in v['parameters']
            } 
            for k, v 
            in method.items() 
            if k in ['get', 'post']
        } 
        for stream, method 
        in API_yaml['paths'].items()
    ])

    return method_to_params
```

```python
method_to_params = construct_method_to_params_dict(API_yaml)

pd.Series(method_to_params).head(3).to_dict()
```




    {'get_B0610': {'APIKey': 'AP8DA23',
      'SettlementDate': '2021-01-01',
      'Period': '1',
      'ServiceType': 'csv'},
     'get_B0620': {'APIKey': 'AP8DA23',
      'SettlementDate': '2021-01-01',
      'Period': '1',
      'ServiceType': 'csv'},
     'get_B0630': {'APIKey': 'AP8DA23',
      'Year': '2021',
      'Week': '22',
      'ServiceType': 'csv'}}



```python
flatten_list = lambda list_: [item for sublist in list_ for item in sublist]

field_names = sorted(list(set(flatten_list([list(params.keys()) for params in method_to_params.values()]))))

field_names
```




    ['APIKey',
     'ActiveFlag',
     'AssetID',
     'BMUnitId',
     'BMUnitType',
     'EndDate',
     'EndTime',
     'EventEnd',
     'EventStart',
     'EventType',
     'FromClearedDate',
     'FromDate',
     'FromDateTime',
     'FromSettlementDate',
     'FuelType',
     'LeadPartyName',
     'MessageID',
     'MessageId',
     'MessageType',
     'Month',
     'NGCBMUnit',
     'NGCBMUnitID',
     'Name',
     'ParticipantId',
     'Period',
     'ProcessType',
     'PublicationFrom',
     'PublicationTo',
     'SequenceId',
     'ServiceType',
     'SettlementDate',
     'SettlementPeriod',
     'StartDate',
     'StartTime',
     'ToClearedDate',
     'ToDate',
     'ToDateTime',
     'ToSettlementDate',
     'UnavailabilityType',
     'Week',
     'Year',
     'isTwoDayWindow']



```python
#exports
def construct_request_type_filter(
    has_start_time: bool,
    has_end_time: bool,
    has_start_date: bool,
    has_end_date: bool,
    has_date: bool,
    has_SP: bool,
    has_year: bool,
    has_month: bool,
    has_week: bool
):
    request_type_filter = {
        'year': (has_year + has_month + has_week == 1) and (has_year == 1),
        'month': (has_year + has_month == 1) and (has_month == 1),
        'week': (has_year + has_week == 1) and (has_week == 1),
        'year_and_month': has_year + has_month == 2,
        'year_and_week': has_year + has_week == 2,
        'SP_and_date': has_SP + has_date == 2,
        'date_range': has_start_time + has_end_time + has_start_date + has_end_date == 2,
        'date_time_range': has_start_time + has_end_time + has_start_date + has_end_date == 4,
        'non_temporal': has_start_time + has_end_time + has_start_date + has_end_date + has_SP + has_date + has_year + has_month == 0,
    }
    
    return request_type_filter

def check_request_type_filter(
    field_names: list,
    request_type_filter: dict,
    has_start_time: bool,
    has_end_time: bool,
    has_start_date: bool,
    has_end_date: bool,
    has_date: bool,
    has_SP: bool,
    has_year: bool,
    has_month: bool,
    has_week: bool
):
    """
    Checks the validity of the specified stream parameters
    
    The following conditions will raise an error:
    * has month without a year
    * has only one of start/end time
    * has only one of start/end date
    * has only one settlement period or date
    * filter does not contain only one request type
    """
    
    filter_str = f'\n\nFilter:\n{request_type_filter}\n\nField Names:\n{", ".join(field_names)}'

    assert {(False, True): True, (False, False): False, (True, True): False, (True, False): False}[(has_year, has_month)] == False, 'Cannot provide a month without a year' + filter_str
    assert {(False, True): True, (False, False): False, (True, True): False, (True, False): False}[(has_year, has_week)] == False, 'Cannot provide a week without a year' + filter_str
    assert has_start_time + has_end_time != 1, 'Only one of start/end time was provided' + filter_str
    assert has_start_date + has_end_date != 1, 'Only one of start/end date was provided' + filter_str
    assert (has_SP + has_date != 1) or (has_start_date + has_end_date == 2), 'Only one of date/SP was provided' + filter_str
    assert sum(request_type_filter.values()) == 1, 'Request type could not be determined\n\nFilter' + filter_str
    
    return 

def determine_request_type_from_fields(
    field_names: list,
    start_time_cols: list=['StartTime'],
    end_time_cols: list=['EndTime'],
    start_date_cols: list=['StartDate', 'FromSettlementDate', 'FromDate'],
    end_date_cols: list=['EndDate', 'ToSettlementDate', 'ToDate'],
    date_cols: list=['SettlementDate', 'ImplementationDate', 'DecommissioningDate', 'Date', 'startTimeOfHalfHrPeriod'],
    SP_cols: list=['SettlementPeriod', 'Period'],
    year_cols: list=['Year'],
    month_cols: list=['Month', 'MonthName'],
    week_cols: list=['Week']
):   
    has_start_time = bool(set(field_names).intersection(set(start_time_cols)))
    has_end_time = bool(set(field_names).intersection(set(end_time_cols)))
    has_start_date = bool(set(field_names).intersection(set(start_date_cols)))
    has_end_date = bool(set(field_names).intersection(set(end_date_cols)))
    has_date = bool(set(field_names).intersection(set(date_cols)))
    has_SP = bool(set(field_names).intersection(set(SP_cols)))
    has_year = bool(set(field_names).intersection(set(year_cols)))
    has_month = bool(set(field_names).intersection(set(month_cols)))
    has_week = bool(set(field_names).intersection(set(week_cols)))

    request_type_filter = construct_request_type_filter(
        has_start_time, has_end_time, has_start_date, 
        has_end_date, has_date, has_SP, has_year, has_month, has_week
    )
    
    check_request_type_filter(
        field_names, request_type_filter, has_start_time, has_end_time, has_start_date, 
        has_end_date, has_date, has_SP, has_year, has_month, has_week
    )

    request_type = [k for k, v in request_type_filter.items() if v==True][0]

    return request_type
```

```python
method = 'get_B1610'

field_names = list(method_to_params[method].keys())
request_type = determine_request_type_from_fields(field_names)

request_type
```




    'SP_and_date'



```python
#exports
def determine_method_request_types(method_to_params):
    method_to_request_type = dict()

    for method in method_to_params.keys():
        field_names = list(method_to_params[method].keys())
        method_to_request_type[method] = determine_request_type_from_fields(field_names)

    return method_to_request_type
```

```python
method_to_request_type = determine_method_request_types(method_to_params)

pd.Series(method_to_request_type).value_counts()
```




    SP_and_date        22
    date_time_range     9
    non_temporal        8
    year                5
    year_and_month      3
    year_and_week       1
    date_range          1
    dtype: int64



```python
#exports
def construct_method_to_params_map(method_to_params):
    standardised_params_map = {
        'start_time': ['StartTime'],
        'end_time': ['EndTime'],
        'start_date': ['StartDate', 'FromSettlementDate', 'FromDate'],
        'end_date': ['EndDate', 'ToSettlementDate', 'ToDate'],
        'date': ['SettlementDate', 'ImplementationDate', 'DecommissioningDate', 'Date', 'startTimeOfHalfHrPeriod'],
        'SP': ['SettlementPeriod', 'Period'],
        'year': ['Year'],
        'month': ['Month', 'MonthName'],
        'week': ['Week']
    }

    method_to_params_map = dict()

    for method, params in method_to_params.items():
        method_to_params_map[method] = dict()

        for param in params.keys():
            for standardised_param, bmrs_params in standardised_params_map.items():
                if param in bmrs_params:
                    method_to_params_map[method][standardised_param] = param

    return method_to_params_map
```

```python
method_to_params_map = construct_method_to_params_map(method_to_params)

pd.Series(method_to_params_map).head(3).to_dict()
```




    {'get_B0610': {'date': 'SettlementDate', 'SP': 'Period'},
     'get_B0620': {'date': 'SettlementDate', 'SP': 'Period'},
     'get_B0630': {'year': 'Year', 'week': 'Week'}}



```python
#exports
def construct_method_info_dict(API_yaml_fp: str):
    API_yaml = specgen.load_API_yaml(API_yaml_fp)
    
    method_to_params = construct_method_to_params_dict(API_yaml)
    method_to_request_type = determine_method_request_types(method_to_params)
    method_to_params_map = construct_method_to_params_map(method_to_params)

    method_info = dict()

    for method, params in  method_to_params.items():
        method_info[method] = dict()

        method_info[method]['request_type'] = method_to_request_type[method]
        method_info[method]['kwargs_map'] = method_to_params_map[method]
        method_info[method]['func_kwargs'] = {
            (
                {v: k for k, v in method_to_params_map[method].items()}[k] 
                if k in method_to_params_map[method].values()
                else k
            ): v 
            for k, v 
            in method_to_params[method].items()
        }
        
    return method_info
```

```python
method_info = construct_method_info_dict('../data/BMRS_API.yaml')
    
JSON([method_info])
```




    <IPython.core.display.JSON object>


