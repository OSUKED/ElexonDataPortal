# Core API



<br>

### Imports

```python
#exports
import pandas as pd
from tqdm import tqdm
from warnings import warn
from requests.models import Response

from ElexonDataPortal.dev import utils, raw
```

```python
from IPython.display import JSON
from ElexonDataPortal.dev import clientprep
```

```python
import os
from dotenv import load_dotenv

assert load_dotenv('../.env'), 'Environment variables could not be loaded'

api_key = os.environ['BMRS_API_KEY']
```

```python
API_yaml_fp = '../data/BMRS_API.yaml'

method_info = clientprep.construct_method_info_dict(API_yaml_fp)
    
JSON([method_info])
```




    <IPython.core.display.JSON object>



<br>

### Request Types

```python
#exports
def if_possible_parse_local_datetime(df):
    dt_cols_with_period_in_name = ['startTimeOfHalfHrPeriod', 'initialForecastPublishingPeriodCommencingTime', 'latestForecastPublishingPeriodCommencingTime', 'outTurnPublishingPeriodCommencingTime']
    
    dt_cols = [col for col in df.columns if 'date' in col.lower() or col in dt_cols_with_period_in_name]
    sp_cols = [col for col in df.columns if 'period' in col.lower() and col not in dt_cols_with_period_in_name]

    if len(dt_cols)==1 and len(sp_cols)==1:
        df = utils.parse_local_datetime(df, dt_col=dt_cols[0], SP_col=sp_cols[0])
        
    return df

def SP_and_date_request(
    method: str,
    kwargs_map: dict,
    func_params: list,
    api_key: str,
    start_date: str,
    end_date: str,
    **kwargs
):
    assert start_date is not None, '`start_date` must be specified'
    assert end_date is not None, '`end_date` must be specified'
    
    df = pd.DataFrame()
    stream = '_'.join(method.split('_')[1:])
    
    kwargs.update({
        'APIKey': api_key,
        'ServiceType': 'xml'
    })

    df_dates_SPs = utils.dt_rng_to_SPs(start_date, end_date)
    date_SP_tuples = list(df_dates_SPs.reset_index().itertuples(index=False, name=None))

    for datetime, query_date, SP in tqdm(date_SP_tuples, desc=stream, total=len(date_SP_tuples)):
        kwargs.update({
            kwargs_map['date']: datetime.strftime('%Y-%m-%d'),
            kwargs_map['SP']: SP,
        })
        
        missing_kwargs = list(set(func_params) - set(['SP', 'date'] + list(kwargs.keys())))
        assert len(missing_kwargs) == 0, f"The following kwargs are missing: {', '.join(missing_kwargs)}"

        r = getattr(raw, method)(**kwargs)
        utils.check_status(r)
        df_SP = utils.parse_xml_response(r)

        df = df.append(df_SP)
    
    df = utils.expand_cols(df)
    df = if_possible_parse_local_datetime(df)
        
    return df
```

```python
method_info_mock = {
    'get_B1610': {
        'request_type': 'SP_and_date',
        'kwargs_map': {'date': 'SettlementDate', 'SP': 'Period'},
        'func_kwargs': {
            'APIKey': 'AP8DA23',
            'date': '2020-01-01',
            'SP': '1',
            'NGCBMUnitID': '*',
            'ServiceType': 'csv'
        }
    }
}

method = 'get_B1610'
kwargs = {'NGCBMUnitID': '*'}

kwargs_map = method_info_mock[method]['kwargs_map']
func_params = list(method_info_mock[method]['func_kwargs'].keys())

df = SP_and_date_request(
    method=method,
    kwargs_map=kwargs_map,
    func_params=func_params,
    api_key=api_key,
    start_date='2020-01-01',
    end_date='2020-01-01 01:30',
    **kwargs
)
    
df.head(3)
```

    B1610: 100% 4/4 [00:02<00:00,  1.45it/s]
    




| documentType      | businessType   | processType   | timeSeriesID          | curveType                   | settlementDate   | powerSystemResourceType   | registeredResourceEICCode   | marketGenerationUnitEICCode   | marketGenerationBMUId   | ...   | nGCBMUnitID   | activeFlag   | documentID              |   documentRevNum | resolution   | start      | end        |   settlementPeriod |   quantity | local_datetime            |
|:------------------|:---------------|:--------------|:----------------------|:----------------------------|:-----------------|:--------------------------|:----------------------------|:------------------------------|:------------------------|:------|:--------------|:-------------|:------------------------|-----------------:|:-------------|:-----------|:-----------|-------------------:|-----------:|:--------------------------|
| Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-305 | Sequential fixed size block | 2020-01-01       | Generation                | 48W00000HRSTW-19            | 48W00000HRSTW-19              | T_HRSTW-1               | ...   | HRSTW-1       | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     48.346 | 2020-01-01 00:00:00+00:00 |
| Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-338 | Sequential fixed size block | 2020-01-01       | Generation                | 48W000000RREW-14            | 48W000000RREW-14              | T_RREW-1                | ...   | RREW-1        | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     35.92  | 2020-01-01 00:00:00+00:00 |
| Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-349 | Sequential fixed size block | 2020-01-01       | Generation                | 48W000000SIZB-2S            | 48W000000SIZB-2S              | T_SIZB-2                | ...   | SIZB-2        | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |    599.94  | 2020-01-01 00:00:00+00:00 |</div>



```python
#exports
def handle_capping(
    r: Response, 
    df: pd.DataFrame,
    method: str,
    kwargs_map: dict,
    func_params: list,
    api_key: str,
    end_date: str,
    request_type: str,
    **kwargs
):
    capping_applied = utils.check_capping(r)
    assert capping_applied != None, 'No information on whether or not capping limits had been breached could be found in the response metadata'
    
    if capping_applied == True: # only subset of date range returned
        dt_cols_with_period_in_name = ['startTimeOfHalfHrPeriod']
        dt_cols = [col for col in df.columns if ('date' in col.lower() or col in dt_cols_with_period_in_name) and ('end' not in col.lower())]
        
        if len(dt_cols) == 1:
            start_date = pd.to_datetime(df[dt_cols[0]]).max().strftime('%Y-%m-%d')
            if 'start_time' in kwargs.keys():
                kwargs['start_time'] = '00:00'
            
            if pd.to_datetime(start_date) >= pd.to_datetime(end_date):
                warnings.warn(f'The `end_date` ({end_date}) was earlier than `start_date` ({start_date})\nThe `start_date` will be set one day earlier than the `end_date`.')
                start_date = (pd.to_datetime(end_date) - pd.Timedelta(days=1)).strftime('%Y-%m-%d')
                        
            warn(f'Response was capped, request is rerunning for missing data from {start_date}')
            df_rerun = date_range_request(
                            method=method,
                            kwargs_map=kwargs_map,
                            func_params=func_params,
                            api_key=api_key,
                            start_date=start_date,
                            end_date=end_date,
                            request_type=request_type,
                            **kwargs
                        )
        
            df = df.append(df_rerun)
            df = df.drop_duplicates()
            
        else:
            warn(f'Response was capped: a new `start_date` to continue requesting could not be determined automatically, please handle manually for `{method}`')
            
    return df
    
def date_range_request(
    method: str,
    kwargs_map: dict,
    func_params: list,
    api_key: str,
    start_date: str,
    end_date: str,
    request_type: str,
    **kwargs
):
    assert start_date is not None, '`start_date` must be specified'
    assert end_date is not None, '`end_date` must be specified'
    
    kwargs.update({
        'APIKey': api_key,
        'ServiceType': 'xml'
    })

    for kwarg in ['start_time', 'end_time']:
        if kwarg not in kwargs_map.keys():
            kwargs_map[kwarg] = kwarg
        
    kwargs[kwargs_map['start_date']], kwargs[kwargs_map['start_time']] = pd.to_datetime(start_date).strftime('%Y-%m-%d %H:%M:%S').split(' ')
    kwargs[kwargs_map['end_date']], kwargs[kwargs_map['end_time']] = pd.to_datetime(end_date).strftime('%Y-%m-%d %H:%M:%S').split(' ')
    
    if 'SP' in kwargs_map.keys():
        kwargs[kwargs_map['SP']] = '*'
        func_params.remove('SP')
        func_params += [kwargs_map['SP']]

    missing_kwargs = list(set(func_params) - set(['start_date', 'end_date', 'start_time', 'end_time'] + list(kwargs.keys())))
    assert len(missing_kwargs) == 0, f"The following kwargs are missing: {', '.join(missing_kwargs)}"
    
    if request_type == 'date_range':
        kwargs.pop(kwargs_map['start_time'])
        kwargs.pop(kwargs_map['end_time'])

    r = getattr(raw, method)(**kwargs)
    utils.check_status(r)
    
    df = utils.parse_xml_response(r)
    df = if_possible_parse_local_datetime(df)
    
    # Handling capping
    df = handle_capping(
        r, 
        df,
        method=method,
        kwargs_map=kwargs_map,
        func_params=func_params,
        api_key=api_key,
        end_date=end_date,
        request_type=request_type,
        **kwargs
    )
        
    return df
```

```python
method = 'get_B1540'
kwargs = {}

kwargs_map = method_info[method]['kwargs_map']
func_params = list(method_info[method]['func_kwargs'].keys())
request_type = method_info[method]['request_type']
    
df = date_range_request(
    method=method,
    kwargs_map=kwargs_map,
    func_params=func_params,
    api_key=api_key,
    start_date='2020-01-01',
    end_date='2021-01-01',
    request_type=request_type,
    **kwargs
)
    
df.head(3)
```

    <ipython-input-8-a3b15d7a70c8>:28: UserWarning: Response was capped, request is rerunning for missing data from 2020-06-23
      warn(f'Response was capped, request is rerunning for missing data from {start_date}')
    <ipython-input-8-a3b15d7a70c8>:28: UserWarning: Response was capped, request is rerunning for missing data from 2020-11-03
      warn(f'Response was capped, request is rerunning for missing data from {start_date}')
    <ipython-input-8-a3b15d7a70c8>:28: UserWarning: Response was capped, request is rerunning for missing data from 2020-12-31
      warn(f'Response was capped, request is rerunning for missing data from {start_date}')
    




| timeSeriesID             | businessType     | settlementStartDate   | settlementStartTime   | settlementEndDate   | settlementEndTime   |   quantity | prodRegisteredResourcemRID   |   bMUnitID | nGCBMUnitID   | documentType              | processType        | activeFlag   | documentID                          |   documentRevNum | reasonCode                |   prodRegisteredResourceName |   prodRegisteredResourcemLocation |   pSRType | reasonDescription   |
|:-------------------------|:-----------------|:----------------------|:----------------------|:--------------------|:--------------------|-----------:|:-----------------------------|-----------:|:--------------|:--------------------------|:-------------------|:-------------|:------------------------------------|-----------------:|:--------------------------|-----------------------------:|----------------------------------:|----------:|:--------------------|
| MP-NGET-AAPU-TS-00050434 | Unplanned outage | 2020-06-23            | 23:00:00              | 2020-07-07          | 23:00:00            |          0 | 48WSTN0000ABTHBN             |        nan | ABTHB         | Production unavailability | Outage information | Y            | 11XINNOGY------2-NGET-AAPU-00050434 |              597 | nan                       |                          nan |                               nan |       nan | nan                 |
| nan                      | nan              | 2020-06-23            | 23:00:00              | 2020-07-07          | 23:00:00            |        nan | nan                          |        nan | nan           | Production unavailability | Outage information | Y            | 11XINNOGY------2-NGET-AAPU-00050434 |              597 | Failure                   |                          nan |                               nan |       nan | nan                 |
| nan                      | nan              | 2020-06-23            | 23:00:00              | 2020-07-07          | 23:00:00            |        nan | nan                          |        nan | nan           | Production unavailability | Outage information | Y            | 11XINNOGY------2-NGET-AAPU-00050434 |              597 | Complementary information |                          nan |                               nan |       nan | Other               |</div>



```python
#exports
def year_request(
    method: str,
    kwargs_map: dict,
    func_params: list,
    api_key: str,
    start_date: str,
    end_date: str,
    **kwargs
):
    assert start_date is not None, '`start_date` must be specified'
    assert end_date is not None, '`end_date` must be specified'
    
    df = pd.DataFrame()
    stream = '_'.join(method.split('_')[1:])
    
    kwargs.update({
        'APIKey': api_key,
        'ServiceType': 'xml'
    })
    
    start_year = int(pd.to_datetime(start_date).strftime('%Y'))
    end_year = int(pd.to_datetime(end_date).strftime('%Y'))

    for year in tqdm(range(start_year, end_year+1), desc=stream):
        kwargs.update({kwargs_map['year']: year})

        missing_kwargs = list(set(func_params) - set(['year'] + list(kwargs.keys())))
        assert len(missing_kwargs) == 0, f"The following kwargs are missing: {', '.join(missing_kwargs)}"

        r = getattr(raw, method)(**kwargs)
        utils.check_status(r)
        df_year = utils.parse_xml_response(r)
        
        df = df.append(df_year)
        
    df = if_possible_parse_local_datetime(df)
        
    return df
```

```python
method = 'get_B0650'
kwargs = {}

kwargs_map = method_info[method]['kwargs_map']
func_params = list(method_info[method]['func_kwargs'].keys())

df = year_request(
    method=method,
    kwargs_map=kwargs_map,
    func_params=func_params,
    api_key=api_key,
    start_date='2020-01-01',
    end_date='2021-01-01 01:30',
    **kwargs
)
    
df.head(3)
```

    B0650: 100% 2/2 [00:01<00:00,  1.06it/s]
    




| timeSeriesID                | businessType      |   year |   week |   quantity | documentType      | processType   | objectAggregation   | curveType                   | resolution   | unitOfMeasure   | monthName   | activeFlag   | documentID               |   documentRevNum |
|:----------------------------|:------------------|-------:|-------:|-----------:|:------------------|:--------------|:--------------------|:----------------------------|:-------------|:----------------|:------------|:-------------|:-------------------------|-----------------:|
| NGET-EMFIP-YATL-TS-00000762 | Maximum available |   2020 |     53 |       4019 | System total load | Year ahead    | Area                | Sequential fixed size block | P7D          | Mega watt       | DEC         | Y            | NGET-EMFIP-YATL-00000741 |                1 |
| NGET-EMFIP-YATL-TS-00000781 | Minimum possible  |   2020 |     53 |       2181 | System total load | Year ahead    | Area                | Sequential fixed size block | P7D          | Mega watt       | DEC         | Y            | NGET-EMFIP-YATL-00000761 |                1 |
| NGET-EMFIP-YATL-TS-00000782 | Maximum available |   2020 |     53 |       4100 | System total load | Year ahead    | Area                | Sequential fixed size block | P7D          | Mega watt       | DEC         | Y            | NGET-EMFIP-YATL-00000761 |                1 |</div>



```python
#exports
def construct_year_month_pairs(start_date, end_date):
    dt_rng = pd.date_range(start_date, end_date, freq='M')

    if len(dt_rng) == 0:
        year_month_pairs = [tuple(pd.to_datetime(start_date).strftime('%Y %b').split(' '))]
    else:
        year_month_pairs = [tuple(dt.strftime('%Y %b').split(' ')) for dt in dt_rng]

    year_month_pairs = [(int(year), week.upper()) for year, week in year_month_pairs]
    
    return year_month_pairs

def year_and_month_request(
    method: str,
    kwargs_map: dict,
    func_params: list,
    api_key: str,
    start_date: str,
    end_date: str,
    **kwargs
):
    assert start_date is not None, '`start_date` must be specified'
    assert end_date is not None, '`end_date` must be specified'
    
    df = pd.DataFrame()
    stream = '_'.join(method.split('_')[1:])
    
    kwargs.update({
        'APIKey': api_key,
        'ServiceType': 'xml'
    })
    
    year_month_pairs = construct_year_month_pairs(start_date, end_date)

    for year, month in tqdm(year_month_pairs, desc=stream):
        kwargs.update({
            kwargs_map['year']: year,
            kwargs_map['month']: month
        })

        missing_kwargs = list(set(func_params) - set(['year', 'month'] + list(kwargs.keys())))
        assert len(missing_kwargs) == 0, f"The following kwargs are missing: {', '.join(missing_kwargs)}"

        r = getattr(raw, method)(**kwargs)
        utils.check_status(r)
        df_year = utils.parse_xml_response(r)
        
        df = df.append(df_year)
        
    df = if_possible_parse_local_datetime(df)
    
    return df
```

```python
method = 'get_B0640'
kwargs = {}

kwargs_map = method_info[method]['kwargs_map']
func_params = list(method_info[method]['func_kwargs'].keys())

df = year_and_month_request(
    method=method,
    kwargs_map=kwargs_map,
    func_params=func_params,
    api_key=api_key,
    start_date='2020-01-01',
    end_date='2020-03-31',
    **kwargs
)
    
df.head(3)
```

    B0640: 100% 3/3 [00:00<00:00,  5.57it/s]
    




| timeSeriesID                | businessType      |   year | monthName   | week       |   quantity | documentType      | processType   | objectAggregation   | curveType                   | resolution   | unitOfMeasure   | activeFlag   | documentID               |   documentRevNum |
|:----------------------------|:------------------|-------:|:------------|:-----------|-----------:|:------------------|:--------------|:--------------------|:----------------------------|:-------------|:----------------|:-------------|:-------------------------|-----------------:|
| NGET-EMFIP-MATL-TS-06201799 | Minimum possible  |   2020 | JAN         | 2020-01-27 |      20201 | System total load | Month ahead   | Area                | Sequential fixed size block | P7D          | Mega watt       | Y            | NGET-EMFIP-MATL-16201797 |                1 |
| NGET-EMFIP-MATL-TS-06201800 | Maximum available |   2020 | JAN         | 2020-01-27 |      53599 | System total load | Month ahead   | Area                | Sequential fixed size block | P7D          | Mega watt       | Y            | NGET-EMFIP-MATL-16201797 |                1 |
| NGET-EMFIP-MATL-TS-06201801 | Minimum possible  |   2020 | JAN         | 2020-01-27 |      20201 | System total load | Month ahead   | Area                | Sequential fixed size block | P7D          | Mega watt       | Y            | NGET-EMFIP-MATL-16201817 |                1 |</div>



```python
#exports
def clean_year_week(year, week):
    year = int(year)
    
    if week == '00':
        year = int(year) - 1
        week = 52
        
    else:
        year = int(year)
        week = int(week.strip('0'))
        
    return year, week

def construct_year_week_pairs(start_date, end_date):
    dt_rng = pd.date_range(start_date, end_date, freq='W')

    if len(dt_rng) == 0:
        year_week_pairs = [tuple(pd.to_datetime(start_date).strftime('%Y %W').split(' '))]
    else:
        year_week_pairs = [tuple(dt.strftime('%Y %W').split(' ')) for dt in dt_rng]

    year_week_pairs = [clean_year_week(year, week) for year, week in year_week_pairs]
    
    return year_week_pairs

def year_and_week_request(
    method: str,
    kwargs_map: dict,
    func_params: list,
    api_key: str,
    start_date: str,
    end_date: str,
    **kwargs
):
    assert start_date is not None, '`start_date` must be specified'
    assert end_date is not None, '`end_date` must be specified'
    
    df = pd.DataFrame()
    stream = '_'.join(method.split('_')[1:])
    
    kwargs.update({
        'APIKey': api_key,
        'ServiceType': 'xml'
    })
    
    year_week_pairs = construct_year_week_pairs(start_date, end_date)

    for year, week in tqdm(year_week_pairs, desc=stream):
        kwargs.update({
            kwargs_map['year']: year,
            kwargs_map['week']: week
        })

        missing_kwargs = list(set(func_params) - set(['year', 'week'] + list(kwargs.keys())))
        assert len(missing_kwargs) == 0, f"The following kwargs are missing: {', '.join(missing_kwargs)}"

        r = getattr(raw, method)(**kwargs)
        utils.check_status(r)
        df_year = utils.parse_xml_response(r)
        
        df = df.append(df_year)
        
    df = if_possible_parse_local_datetime(df)
    
    return df
```

```python
method = 'get_B0630'
kwargs = {}

kwargs_map = method_info[method]['kwargs_map']
func_params = list(method_info[method]['func_kwargs'].keys())

df = year_and_week_request(
    method=method,
    kwargs_map=kwargs_map,
    func_params=func_params,
    api_key=api_key,
    start_date='2020-01-01',
    end_date='2020-01-31',
    **kwargs
)
    
df.head(3)
```

    B0630: 100% 4/4 [00:00<00:00,  6.22it/s]
    




| timeSeriesID                | businessType      | settlementDate   |   quantity |   week | documentType      | processType   | objectAggregation   | curveType                   | resolution   | unitOfMeasure   |   year | activeFlag   | documentID               |   documentRevNum |
|:----------------------------|:------------------|:-----------------|-----------:|-------:|:------------------|:--------------|:--------------------|:----------------------------|:-------------|:----------------|-------:|:-------------|:-------------------------|-----------------:|
| NGET-EMFIP-WATL-TS-00005681 | Minimum possible  | 2019-12-29       |      22753 |     52 | System total load | Week ahead    | Area                | Sequential fixed size block | P1D          | Mega watt       |   2019 | Y            | NGET-EMFIP-WATL-00005681 |                1 |
| NGET-EMFIP-WATL-TS-00005682 | Maximum available | 2019-12-29       |      40156 |     52 | System total load | Week ahead    | Area                | Sequential fixed size block | P1D          | Mega watt       |   2019 | Y            | NGET-EMFIP-WATL-00005681 |                1 |
| NGET-EMFIP-WATL-TS-00005681 | Minimum possible  | 2019-12-28       |      23644 |     52 | System total load | Week ahead    | Area                | Sequential fixed size block | P1D          | Mega watt       |   2019 | Y            | NGET-EMFIP-WATL-00005681 |                1 |</div>



```python
#exports
def non_temporal_request(
    method: str,
    api_key: str,
    **kwargs
):    
    kwargs.update({
        'APIKey': api_key,
        'ServiceType': 'xml'
    })
    
    r = getattr(raw, method)(**kwargs)
    utils.check_status(r)
    
    df = utils.parse_xml_response(r)
    df = if_possible_parse_local_datetime(df)
        
    return df
```

<br>

### Query Orchestrator

```python
#exports
def query_orchestrator(
    method: str,
    api_key: str,
    request_type: str,
    kwargs_map: dict=None,
    func_params: list=None,
    start_date: str=None,
    end_date: str=None,
    **kwargs
):    
    if request_type not in ['non_temporal']:
        kwargs.update({
            'kwargs_map': kwargs_map,
            'func_params': func_params,
            'start_date': start_date,
            'end_date': end_date,
        })
        
    if request_type in ['date_range', 'date_time_range']:
        kwargs.update({
            'request_type': request_type,
        })
        
    request_type_to_func = {
        'SP_and_date': SP_and_date_request,
        'date_range': date_range_request,
        'date_time_range': date_range_request,
        'year': year_request,
        'year_and_month': year_and_month_request,
        'year_and_week': year_and_week_request,
        'non_temporal': non_temporal_request
    }
    
    assert request_type in request_type_to_func.keys(), f"{request_type} must be one of: {', '.join(request_type_to_func.keys())}"
    request_func = request_type_to_func[request_type]
    
    df = request_func(
        method=method,
        api_key=api_key,
        **kwargs
    )
    
    df = df.reset_index(drop=True)

    return df
```

```python
method = 'get_B0630'
start_date = '2020-01-01'
end_date = '2020-01-31'

request_type = method_info[method]['request_type']
kwargs_map = method_info[method]['kwargs_map']
func_params = list(method_info[method]['func_kwargs'].keys())

df = query_orchestrator(
    method=method,
    api_key=api_key,
    request_type=request_type,
    kwargs_map=kwargs_map,
    func_params=func_params,
    start_date=start_date,
    end_date=end_date
)

df.head(3)
```

    B0630: 100% 4/4 [00:00<00:00,  6.54it/s]
    




| timeSeriesID                | businessType      | settlementDate   |   quantity |   week | documentType      | processType   | objectAggregation   | curveType                   | resolution   | unitOfMeasure   |   year | activeFlag   | documentID               |   documentRevNum |
|:----------------------------|:------------------|:-----------------|-----------:|-------:|:------------------|:--------------|:--------------------|:----------------------------|:-------------|:----------------|-------:|:-------------|:-------------------------|-----------------:|
| NGET-EMFIP-WATL-TS-00005681 | Minimum possible  | 2019-12-29       |      22753 |     52 | System total load | Week ahead    | Area                | Sequential fixed size block | P1D          | Mega watt       |   2019 | Y            | NGET-EMFIP-WATL-00005681 |                1 |
| NGET-EMFIP-WATL-TS-00005682 | Maximum available | 2019-12-29       |      40156 |     52 | System total load | Week ahead    | Area                | Sequential fixed size block | P1D          | Mega watt       |   2019 | Y            | NGET-EMFIP-WATL-00005681 |                1 |
| NGET-EMFIP-WATL-TS-00005681 | Minimum possible  | 2019-12-28       |      23644 |     52 | System total load | Week ahead    | Area                | Sequential fixed size block | P1D          | Mega watt       |   2019 | Y            | NGET-EMFIP-WATL-00005681 |                1 |</div>


