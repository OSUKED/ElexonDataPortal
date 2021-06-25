# Title



```python
#exports
from jinja2 import Template

from ElexonDataPortal.dev import specgen, rawgen, clientprep
```

```python
import os
from dotenv import load_dotenv

assert load_dotenv('../.env'), 'Environment variables could not be loaded'

api_key = os.environ['BMRS_API_KEY']
```

<br>

### API Client Generation

```python
#exports
def generate_streams(API_yaml_fp):
    request_type_to_date_range_example = {
        'SP_and_date': ('2020-01-01', '2020-01-01 1:30'),
        'date_range': ('2020-01-01', '2020-01-07'),
        'date_time_range': ('2020-01-01', '2020-01-07'),
        'year': ('2019-01-01', '2021-01-01'),
        'year_and_month': ('2020-01-01', '2020-06-01'),
        'year_and_week': ('2020-01-01', '2020-06-01'),
        'non_temporal': (None, None)
    }
    
    API_yaml = specgen.load_API_yaml(API_yaml_fp)
    functions = rawgen.construct_all_functions(API_yaml)
    method_info = clientprep.construct_method_info_dict(API_yaml_fp)

    streams = list()

    for function in functions:
        name = function['name']
        function_method_info = method_info[name]

        stream = dict()
        stream['name'] = name
        stream['description'] = function['description']
        stream['date_range_example'] = request_type_to_date_range_example[function_method_info['request_type']]
        stream['extra_kwargs'] = [param for param in function['parameters'] if param['name'] not in list(function_method_info['kwargs_map'].values())+['APIKey', 'ServiceType']]
        stream['request_type'] = function_method_info['request_type']
        stream['kwargs_map'] = function_method_info['kwargs_map']
        stream['func_params'] = list(function_method_info['func_kwargs'].keys())

        streams += [stream]
        
    return streams
```

```python
API_yaml_fp = '../data/BMRS_API.yaml'

streams = generate_streams(API_yaml_fp)

streams[0]
```




    {'name': 'get_B0610',
     'description': 'Actual Total Load per Bidding Zone',
     'date_range_example': ('2020-01-01', '2020-01-01 1:30'),
     'extra_kwargs': [],
     'request_type': 'SP_and_date',
     'kwargs_map': {'date': 'SettlementDate', 'SP': 'Period'},
     'func_params': ['APIKey', 'date', 'SP', 'ServiceType']}



```python
#exports
def save_api_client(
    API_yaml_fp: str,
    in_fp: str='../templates/api.py',
    out_fp: str='../ElexonDataPortal/api.py'
):
    streams = generate_streams(API_yaml_fp)
    rendered_schema = Template(open(in_fp).read()).render(streams=streams)

    with open(out_fp, 'w') as f:
        try:
            f.write(rendered_schema)
        except e as exc:
            raise exc
```

```python
save_api_client(API_yaml_fp)
```

<br>

### API Client Testing

```python
from ElexonDataPortal import api

client = api.Client(api_key)

df = client.get_B1610()

df.head(3)
```

    B1610: 100% 4/4 [00:04<00:00,  1.24s/it]
    




| documentType      | businessType   | processType   | timeSeriesID          | curveType                   | settlementDate   | powerSystemResourceType   | registeredResourceEICCode   | marketGenerationUnitEICCode   | marketGenerationBMUId   | ...   | nGCBMUnitID   | activeFlag   | documentID              |   documentRevNum | resolution   | start      | end        |   settlementPeriod |   quantity | local_datetime   |
|:------------------|:---------------|:--------------|:----------------------|:----------------------------|:-----------------|:--------------------------|:----------------------------|:------------------------------|:------------------------|:------|:--------------|:-------------|:------------------------|-----------------:|:-------------|:-----------|:-----------|-------------------:|-----------:|:-----------------|
| Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-180 | Sequential fixed size block | 2020-01-01       | Generation                | 48W000000FASN-42            | 48W000000FASN-42              | E_FASN-4                | ...   | FASN-4        | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |      7.46  | NaT              |
| Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-298 | Sequential fixed size block | 2020-01-01       | Generation                | 48W000000HINB-77            | 48W000000HINB-77              | T_HINB-7                | ...   | HINB-7        | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |    502.064 | NaT              |
| Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-317 | Sequential fixed size block | 2020-01-01       | Generation                | 48W00000LARYO-4T            | 48W00000LARYO-4T              | T_LARYW-4               | ...   | LARYO-4       | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     70.118 | NaT              |</div>



```python
client_methods = [method for method in dir(client) if ('__' not in method) and (method not in ['api_key', 'methods'])]
method_to_df = dict()

for client_method in client_methods:
    method_to_df[client_method] = getattr(client, client_method)()
```

    B0610: 100% 4/4 [00:00<00:00,  6.34it/s]
    B0620: 100% 4/4 [00:00<00:00,  6.43it/s]
    B0630: 100% 22/22 [00:05<00:00,  4.14it/s]
    B0640: 100% 5/5 [00:00<00:00,  5.29it/s]
    B0650: 100% 3/3 [00:04<00:00,  1.41s/it]
    c:\users\ayrto\desktop\phd\data\bmrs\elexon-bmrs-api-wrapper\ElexonDataPortal\dev\utils.py:27: UserWarning: Data request was succesful but no content was returned
      warn(f'Data request was succesful but no content was returned')
    B0810: 100% 3/3 [00:00<00:00,  6.40it/s]
    B0910: 100% 3/3 [00:00<00:00,  5.75it/s]
    B1320: 100% 4/4 [00:00<00:00,  6.00it/s]
    B1330: 100% 5/5 [00:00<00:00,  5.62it/s]
    B1410: 100% 3/3 [00:00<00:00,  5.08it/s]
    B1420: 100% 3/3 [00:05<00:00,  1.91s/it]
    B1430: 100% 4/4 [00:01<00:00,  3.89it/s]
    B1440: 100% 4/4 [00:01<00:00,  3.88it/s]
    B1610: 100% 4/4 [00:05<00:00,  1.44s/it]
    B1620: 100% 4/4 [00:00<00:00,  4.33it/s]
    B1630: 100% 4/4 [00:00<00:00,  5.61it/s]
    B1720: 100% 4/4 [00:01<00:00,  3.41it/s]
    B1730: 100% 4/4 [00:00<00:00,  5.47it/s]
    B1740: 100% 4/4 [00:00<00:00,  5.92it/s]
    B1750: 100% 4/4 [00:00<00:00,  5.93it/s]
    B1760: 100% 4/4 [00:00<00:00,  6.24it/s]
    B1770: 100% 4/4 [00:01<00:00,  2.78it/s]
    B1780: 100% 4/4 [00:00<00:00,  4.10it/s]
    B1790: 100% 5/5 [00:00<00:00,  6.13it/s]
    B1810: 100% 4/4 [00:00<00:00,  6.13it/s]
    B1820: 100% 4/4 [00:00<00:00,  6.06it/s]
    B1830: 100% 4/4 [00:00<00:00,  6.28it/s]
    BOD: 100% 4/4 [00:00<00:00,  5.60it/s]
    DETSYSPRICES: 100% 4/4 [00:02<00:00,  1.58it/s]
    DISBSAD: 100% 4/4 [00:00<00:00,  5.19it/s]
    c:\users\ayrto\desktop\phd\data\bmrs\elexon-bmrs-api-wrapper\ElexonDataPortal\dev\orchestrator.py:114: UserWarning: Response was capped: a new `start_date` to continue requesting could not be determined automatically, please handle manually for `get_MID`
      warn(f'Response was capped: a new `start_date` to continue requesting could not be determined automatically, please handle manually for `{method}`')
    NETBSAD: 100% 4/4 [00:01<00:00,  2.71it/s]
    PHYBMDATA: 100% 4/4 [00:19<00:00,  4.77s/it]
    c:\users\ayrto\desktop\phd\data\bmrs\elexon-bmrs-api-wrapper\ElexonDataPortal\dev\orchestrator.py:98: UserWarning: Response was capped, request is rerunning for missing data from 2020-01-05
      warn(f'Response was capped, request is rerunning for missing data from {start_date}')
    

```python
method = 'get_B1440'

print(getattr(client, method).__doc__)
method_to_df[method].head(3)
```

    
            Generation forecasts for Wind and Solar
            
            Parameters:
                start_date (str)
                end_date (str)
                ProcessType (str)
            
    




| timeSeriesID                | businessType     | powerSystemResourceType   | settlementDate   | processType   |   settlementPeriod |   quantity | documentType            | curveType                   | resolution   | activeFlag   | documentID               |   documentRevNum | local_datetime   |
|:----------------------------|:-----------------|:--------------------------|:-----------------|:--------------|-------------------:|-----------:|:------------------------|:----------------------------|:-------------|:-------------|:-------------------------|-----------------:|:-----------------|
| NGET-EMFIP-DGWS-TS-00034592 | Solar generation | "Solar"                   | 2020-01-01       | Day Ahead     |                  1 |       0    | Wind and solar forecast | Sequential fixed size block | PT30M        | Y            | NGET-EMFIP-DGWS-00035923 |                1 | NaT              |
| NGET-EMFIP-DGWS-TS-00034590 | Wind generation  | "Wind Offshore"           | 2020-01-01       | Day Ahead     |                  1 |    2843.18 | Wind and solar forecast | Sequential fixed size block | PT30M        | Y            | NGET-EMFIP-DGWS-00035923 |                1 | NaT              |
| NGET-EMFIP-DGWS-TS-00034591 | Wind generation  | "Wind Onshore"            | 2020-01-01       | Day Ahead     |                  1 |    3024.24 | Wind and solar forecast | Sequential fixed size block | PT30M        | Y            | NGET-EMFIP-DGWS-00035923 |                1 | NaT              |</div>


