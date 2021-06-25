# Open-API Specification Generation



<br>

### Imports

```python
#exports
import numpy as np
import pandas as pd

import os
import yaml

from jinja2 import Template
```

```python
from IPython.display import JSON
```

```python
#exports
def init_spec(
    title='BMRS API',
    description='API for the Elexon Balancing Mechanism Reporting Service',
    root_url='https://api.bmreports.com'
):
    API_spec = dict()

    API_spec['title'] = title
    API_spec['description'] = description
    API_spec['root_url'] = root_url
    
    return API_spec
```

```python
API_spec = init_spec()

API_spec
```




    {'title': 'BMRS API',
     'description': 'API for the Elexon Balancing Mechanism Reporting Service',
     'root_url': 'https://api.bmreports.com'}



```python
#exports
def load_endpoints_df(endpoints_fp: str='data/endpoints.csv'):
    df_endpoints = pd.read_csv(endpoints_fp)

    date_idxs = (df_endpoints['Sample Data'].str.count('/')==2).replace(np.nan, False)
    time_idxs = df_endpoints['Sample Data'].str.contains(':').replace(np.nan, False)

    df_endpoints.loc[date_idxs & ~time_idxs, 'Sample Data'] = pd.to_datetime(df_endpoints.loc[date_idxs & ~time_idxs, 'Sample Data']).dt.strftime('%Y-%m-%d')
    df_endpoints.loc[date_idxs & time_idxs, 'Sample Data'] = pd.to_datetime(df_endpoints.loc[date_idxs & time_idxs, 'Sample Data']).dt.strftime('%Y-%m-%d %H:%M:%S')

    df_endpoints['Sample Data'] = df_endpoints['Sample Data'].fillna('')
    df_endpoints['Field Name'] = df_endpoints['Field Name'].str.replace(' ', '')
    
    return df_endpoints
```

```python
df_endpoints = load_endpoints_df('../data/endpoints.csv')
df_endpoints.to_csv('../data/endpoints.csv', index=False)

df_endpoints.head(3)
```




|   Unnamed: 0 | id    | name                                              |   version | method   | direction   | Field Name     | Field Type   |   Remarks | Mandatory   | Format     | Sample Data   |
|-------------:|:------|:--------------------------------------------------|----------:|:---------|:------------|:---------------|:-------------|----------:|:------------|:-----------|:--------------|
|            0 | B1720 | Amount Of Balancing Reserves Under Contract Se... |         1 | get      | request     | APIKey         | String       |       nan | Yes         | nan        | AP8DA23       |
|            1 | B1720 | Amount Of Balancing Reserves Under Contract Se... |         1 | get      | request     | SettlementDate | String       |       nan | Yes         | YYYY-MM-DD | 2021-01-01    |
|            2 | B1720 | Amount Of Balancing Reserves Under Contract Se... |         1 | get      | request     | Period         | String       |       nan | Yes         | */1-50     | 1             |</div>



```python
#exports
def get_endpoint_single_attr(df_endpoint, attribute='version'):
    attr_val = df_endpoint[attribute].unique()
    assert len(attr_val)==1, f'Expected only 1 {attribute}, instead found {len(attr_val)}'
    attr_val = attr_val[0]

    return attr_val
```

```python
endpoint_id = 'B1720'
df_endpoint = df_endpoints.query(f'id==@endpoint_id')

get_endpoint_single_attr(df_endpoint, 'version')
```




    1



```python
#exports
def init_stream_dict(df_endpoint, endpoint_id):
    version = get_endpoint_single_attr(df_endpoint, 'version')
    name = get_endpoint_single_attr(df_endpoint, 'name')

    stream = dict()

    stream['endpoint'] = f'/BMRS/{endpoint_id}/v{version}'
    stream['description'] = name
    stream['parameters'] = list()
    
    return stream
```

```python
stream = init_stream_dict(df_endpoint, endpoint_id)

stream
```




    {'endpoint': '/BMRS/B1720/v1',
     'description': 'Amount Of Balancing Reserves Under Contract Service',
     'parameters': []}



```python
#exports
def add_params_to_stream_dict(
    df_endpoint: pd.DataFrame, 
    stream: dict,
    field_type_map: dict={
        'String': 'string',
        'Int': 'integer',
        'int': 'integer',
        'Integer': 'integer',
        'Date': 'string'
    }
):
    for _, (param_name, param_type, param_sample) in df_endpoint.query('direction=="request"')[['Field Name', 'Field Type', 'Sample Data']].iterrows():               
        parameter = dict()
        
        parameter['name'] = param_name
        parameter['type'] = field_type_map[param_type]
        
        if param_type in ['Date']:
            parameter['format'] = 'date'
        
        if param_name == 'APIKey':
            parameter['format'] = 'password'
        
        if param_sample == 'csv/xml':
            parameter['examples'] = {f'{param_sub_sample}': {'value': param_sub_sample} for param_sub_sample in param_sample.split('/')}
        else:
            parameter['example'] = param_sample
        
        stream['parameters'] += [parameter]
        
    return stream
```

```python
stream = add_params_to_stream_dict(df_endpoint, stream)

stream
```




    {'endpoint': '/BMRS/B1720/v1',
     'description': 'Amount Of Balancing Reserves Under Contract Service',
     'parameters': [{'name': 'APIKey',
       'type': 'string',
       'format': 'password',
       'example': 'AP8DA23'},
      {'name': 'SettlementDate', 'type': 'string', 'example': '2021-01-01'},
      {'name': 'Period', 'type': 'string', 'example': '1'},
      {'name': 'ServiceType',
       'type': 'string',
       'examples': {'csv': {'value': 'csv'}, 'xml': {'value': 'xml'}}}]}



```python
#exports
def add_streams_to_spec(API_spec, df_endpoints):
    API_spec['streams'] = list()
    endpoint_ids = sorted(list(df_endpoints['id'].unique()))

    for endpoint_id in endpoint_ids:
        df_endpoint = df_endpoints.query(f'id==@endpoint_id')

        stream = init_stream_dict(df_endpoint, endpoint_id)
        stream = add_params_to_stream_dict(df_endpoint, stream)

        API_spec['streams'] += [stream]
        
    return API_spec
```

```python
API_spec = add_streams_to_spec(API_spec, df_endpoints)
        
JSON(API_spec)
```




    <IPython.core.display.JSON object>



```python
#exports
def construct_spec(
    df_endpoints: pd.DataFrame,
    title: str='BMRS API',
    description: str='API for the Elexon Balancing Mechanism Reporting Service',
    root_url: str='https://api.bmreports.com'
):
    API_spec = init_spec()
    API_spec = add_streams_to_spec(API_spec, df_endpoints)
    
    return API_spec
```

```python
%%time

API_spec = construct_spec(df_endpoints)
```

    Wall time: 480 ms
    

```python
#exports
def save_spec(
    API_spec: dict,
    in_fp: str='../templates/open_api_spec.yaml',
    out_fp: str='../data/BMRS_API.yaml'
):
    rendered_schema = Template(open(in_fp).read()).render(API_spec=API_spec)

    with open(out_fp, 'w') as f:
        try:
            f.write(rendered_schema)
        except e as exc:
            raise exc
```

```python
save_spec(API_spec)
```

```python
#exports
def load_API_yaml(fp='../data/BMRS_API.yaml'):
    with open(fp, 'r') as stream:
        try:
            API_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc
            
    return API_yaml
```

```python
API_yaml = load_API_yaml(fp='../data/BMRS_API.yaml')

JSON(API_yaml)
```




    <IPython.core.display.JSON object>



```python
# https://app.swaggerhub.com/apis/AyrtonB/default-title/0.1
```
