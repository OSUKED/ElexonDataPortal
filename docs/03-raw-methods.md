# Raw Method Generation



<br>

### Imports

```python
#exports
import pandas as pd
import io
import yaml
import xmltodict
from jinja2 import Template
```

```python
from IPython.display import JSON
from ElexonDataPortal.dev import specgen
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



<br>

### Raw Method Generation

```python
#exports
dict_head = lambda dict_, n=5: dict(pd.Series(dict_).head(n))

def clean_path_name(
    path_name: str='/BMRS/B0610/v1',
    name_components_to_drop: list=['BMRS', 'v1', 'v2']
):
    for name_component_to_drop in name_components_to_drop:
        path_name = path_name.replace(name_component_to_drop, '')

    path_name = path_name.strip('/')
    
    return path_name
```

```python
path_name = '/BMRS/B0610/v1'

clean_path_name(path_name)
```




    'B0610'



```python
#exports
def get_available_methods(
    API_yaml: dict, 
    path: str,
    acceptable_methods: list=['get', 'post', 'put', 'head', 'delete', 'patch', 'options']
):
    path_keys = API_yaml['paths'][path].keys()
    available_methods = list(set(path_keys) - (set(path_keys) - set(acceptable_methods)))

    return available_methods

def extract_parameter_example(parameter):
    if 'examples' in parameter.keys():
        examples = [value['value'] for value in parameter['examples'].values()]
        example = examples[0]
    else:
        example = parameter['example']
        
    return example

def construct_parameters(method_details):    
    parameters = list()
    
    for parameter in method_details['parameters']:
        parameter_info = dict()
        parameter_info['name'] = parameter['name']
        parameter_info['type'] = parameter['schema']['type']
        parameter_info['example'] = extract_parameter_example(parameter)

        parameters += [parameter_info]
        
    return parameters
    
def construct_path_functions(API_yaml, path):
    functions = list()
    root_url = API_yaml['servers'][0]['url']
    available_methods = get_available_methods(API_yaml, path)
    
    for method in available_methods:
        function = dict()
        method_details = API_yaml['paths'][path][method]
        
        function['name'] = f'{method}_{clean_path_name(path)}'
        function['endpoint'] = f'{root_url}{path}'
        function['description'] = method_details['description']
        function['parameters'] = construct_parameters(method_details)
        
        functions += [function]
        
    return functions

def construct_all_functions(API_yaml):
    functions = list()

    for path in API_yaml['paths']:
        functions += construct_path_functions(API_yaml, path)
        
    return functions
```

```python
functions = construct_all_functions(API_yaml)
    
functions[0]
```




    {'name': 'get_B0610',
     'endpoint': 'https://api.bmreports.com/BMRS/B0610/v1',
     'description': 'Actual Total Load per Bidding Zone',
     'parameters': [{'name': 'APIKey', 'type': 'string', 'example': 'AP8DA23'},
      {'name': 'SettlementDate', 'type': 'string', 'example': '2021-01-01'},
      {'name': 'Period', 'type': 'string', 'example': '1'},
      {'name': 'ServiceType', 'type': 'string', 'example': 'csv'}]}



```python
#exports
def save_methods(
    functions: list,
    in_fp: str='../templates/raw_methods.py',
    out_fp: str='../ElexonDataPortal/dev/raw.py'
):
    rendered_schema = Template(open(in_fp).read()).render(functions=functions)

    with open(out_fp, 'w') as f:
        try:
            f.write(rendered_schema)
        except e as exc:
            raise exc
```

```python
save_methods(functions)
```

```python
from ElexonDataPortal.dev import raw

r = raw.get_B1610(
    APIKey=api_key, 
    SettlementDate='2020-01-01', 
    Period=1,
    NGCBMUnitID='*', 
    ServiceType='csv'
)

pd.read_csv(io.StringIO(r.text), skiprows=1).head(3)
```




|   Unnamed: 0 | Time Series ID        | Registered Resource EIC Code   | BM Unit ID   | NGC BM Unit ID   | PSR Type   | Market Generation Unit EIC Code   | Market Generation BMU ID   | Market Generation NGC BM Unit ID   | Settlement Date   |   SP |   Quantity (MW) |
|-------------:|:----------------------|:-------------------------------|:-------------|:-----------------|:-----------|:----------------------------------|:---------------------------|:-----------------------------------|:------------------|-----:|----------------:|
|            0 | ELX-EMFIP-AGOG-TS-319 | 48W00000LNCSO-1R               | T_LNCSW-1    | LNCSO-1          | Generation | 48W00000LNCSO-1R                  | T_LNCSW-1                  | LNCSO-1                            | 2020-01-01        |    1 |          56.076 |
|            1 | ELX-EMFIP-AGOG-TS-320 | 48W00000LNCSO-2P               | T_LNCSW-2    | LNCSO-2          | Generation | 48W00000LNCSO-2P                  | T_LNCSW-2                  | LNCSO-2                            | 2020-01-01        |    1 |          47.456 |
|            2 | ELX-EMFIP-AGOG-TS-175 | 48W00000CLDRW-16               | E_CLDRW-1    | CLDRW-1          | Generation | 48W00000CLDRW-16                  | E_CLDRW-1                  | CLDRW-1                            | 2020-01-01        |    1 |           3.096 |</div>


