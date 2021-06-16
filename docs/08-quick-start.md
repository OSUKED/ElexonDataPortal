# Quick Start Guide



<br>

This notebook outlines how to get up and running with the `ElexonDataPortal` library, a Python client for retrieving data from the Elexon/BMRS API.

The core functionality is exposed through the `ElexonDataPortal.api` module which we'll now import.

<br>

### Client Initialisation

We're now ready to initialise the API `Client`. The key parameter to pass is the `api_key`, alternatively this can be set as the environment variable `BMRS_API_KEY` which will then be loaded automatically (as in this example).

```python
from ElexonDataPortal import api

client = api.Client() # or use `api.Client('your_api_key_here')`

client
```




    <ElexonDataPortal.api.Client at 0x201633d4eb0>



<br>

### Client Usage

The client exposes a `methods` attribute which provides a quick way to explore what request methods are available alongside a short description of the data they return.

```python
import pandas as pd

pd.Series(client.methods).head()
```




    get_B0610                  Actual Total Load per Bidding Zone
    get_B0620      Day-Ahead Total Load Forecast per Bidding Zone
    get_B0630     Week-Ahead Total Load Forecast per Bidding Zone
    get_B0640    Month-Ahead Total Load Forecast Per Bidding Zone
    get_B0650     Year Ahead Total Load Forecast per Bidding Zone
    dtype: object



<br>

Lets look at the docstring for a specific method, in this case the B1610 stream.

```python
print(client.get_B1610.__doc__)
```

    
            Actual Generation Output per Generation Unit
            
            Parameters:
                start_date (str)
                end_date (str)
                NGCBMUnitID (str)
            
    

<br>

Now we know what to pass in to the `get_B1610` method lets call it! 

Each response (4 in this example) will be automatically cleaned and parsed, then concatenated into a single Pandas DataFrame.

```python
start_date = '2020-01-01'
end_date = '2020-01-01 1:30'

df_B1610 = client.get_B1610(start_date, end_date)

df_B1610.head(3)
```

    B1610: 100%|â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ| 4/4 [00:08<00:00,  2.14s/it]
    




|   Unnamed: 0 | documentType      | businessType   | processType   | timeSeriesID          | curveType                   | settlementDate   | powerSystemResourceType   | registeredResourceEICCode   | marketGenerationUnitEICCode   | marketGenerationBMUId   | ...   | nGCBMUnitID   | activeFlag   | documentID              |   documentRevNum | resolution   | start      | end        |   settlementPeriod |   quantity | local_datetime            |
|-------------:|:------------------|:---------------|:--------------|:----------------------|:----------------------------|:-----------------|:--------------------------|:----------------------------|:------------------------------|:------------------------|:------|:--------------|:-------------|:------------------------|-----------------:|:-------------|:-----------|:-----------|-------------------:|-----------:|:--------------------------|
|            0 | Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-212 | Sequential fixed size block | 2020-01-01       | Generation                | 48W000CAS-BEU01F            | 48W000CAS-BEU01F              | M_CAS-BEU01             | ...   | CAS-BEU01     | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     18.508 | 2020-01-01 00:00:00+00:00 |
|            1 | Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-355 | Sequential fixed size block | 2020-01-01       | Generation                | 48W00000STLGW-3A            | 48W00000STLGW-3A              | T_STLGW-3               | ...   | STLGW-3       | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     28.218 | 2020-01-01 00:00:00+00:00 |
|            2 | Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-278 | Sequential fixed size block | 2020-01-01       | Generation                | 48W00000GNFSW-1H            | 48W00000GNFSW-1H              | T_GNFSW-1               | ...   | GNFSW-1       | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     29.44  | 2020-01-01 00:00:00+00:00 |</div>



<br>

We could see from the docstring that there were more parameters we could specify, lets pass in the `NGCBMUnitID` and look at the output for a single power plant. In this example we'll look at the power output from *'LARYO-1'*, which makes up roughly 1/4 of the London Array wind farm.

```python
start_date = '2021-01-01'
end_date = '2021-01-02 23:30'
NGCBMUnitID = 'LARYO-1'

df_LARYO_1 = client.get_B1610(start_date, end_date, NGCBMUnitID)

df_LARYO_1.set_index('local_datetime')['quantity'].astype(float).plot()
```

    B1610: 100%|â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ| 96/96 [00:46<00:00,  2.08it/s]
    




    <AxesSubplot:xlabel='local_datetime'>




![png](img/nbs/08-quick-start_cell_10_output_2.png)


<br>

Before moving on we'll quickly show what an alternative data stream might return, in this case the `B1440` stream which provides *'Generation forecasts for Wind and Solar'*.

```python
start_date = '2020-01-01'
end_date = '2020-01-01 1:30'

df_B1440 = client.get_B1440(start_date, end_date)

df_B1440.head(3)
```

    B1440: 100%|â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ| 4/4 [00:01<00:00,  2.39it/s]
    




|   Unnamed: 0 | timeSeriesID                | businessType     | powerSystemResourceType   | settlementDate   | processType   |   settlementPeriod |   quantity | documentType            | curveType                   | resolution   | activeFlag   | documentID               |   documentRevNum | local_datetime            |
|-------------:|:----------------------------|:-----------------|:--------------------------|:-----------------|:--------------|-------------------:|-----------:|:------------------------|:----------------------------|:-------------|:-------------|:-------------------------|-----------------:|:--------------------------|
|            0 | NGET-EMFIP-DGWS-TS-00034592 | Solar generation | "Solar"                   | 2020-01-01       | Day Ahead     |                  1 |       0    | Wind and solar forecast | Sequential fixed size block | PT30M        | Y            | NGET-EMFIP-DGWS-00035923 |                1 | 2020-01-01 00:00:00+00:00 |
|            1 | NGET-EMFIP-DGWS-TS-00034590 | Wind generation  | "Wind Offshore"           | 2020-01-01       | Day Ahead     |                  1 |    2843.18 | Wind and solar forecast | Sequential fixed size block | PT30M        | Y            | NGET-EMFIP-DGWS-00035923 |                1 | 2020-01-01 00:00:00+00:00 |
|            2 | NGET-EMFIP-DGWS-TS-00034591 | Wind generation  | "Wind Onshore"            | 2020-01-01       | Day Ahead     |                  1 |    3024.24 | Wind and solar forecast | Sequential fixed size block | PT30M        | Y            | NGET-EMFIP-DGWS-00035923 |                1 | 2020-01-01 00:00:00+00:00 |</div>



<br>

### Under the Hood

If you've previously written your own code for extracting data from the Elexon/BMRS API then you may be wondering where some of the normal parameters you pass have gone. The differences in the parameters passed are due to 4 core drivers:

* Standardisation of date range parameter names
* Removal of the need to specify `ServiceType`
* Automatic passing of `APIKey` after client initialisation
* Shipped with sensible defaults for all remaining parameters

If you wish to make requests using the raw methods these are available through the `ElexonDataportal.dev.raw` module. We'll quickly make one of these requests, note that in this example we'll specify `ServiceType=csv`.

```python
import io
from ElexonDataPortal import dev

r = dev.raw.get_B1610(
    APIKey=api_key,
    SettlementDate='2020-01-01',
    Period='1',
    NGCBMUnitID='*',
    ServiceType='csv',
)

df_B1610_raw_csv = pd.read_csv(io.StringIO(r.content.decode('utf-8')), skiprows=1)

df_B1610_raw_csv.head(3)
```




|   Unnamed: 0 | Time Series ID        | Registered Resource EIC Code   | BM Unit ID   | NGC BM Unit ID   | PSR Type   | Market Generation Unit EIC Code   | Market Generation BMU ID   | Market Generation NGC BM Unit ID   | Settlement Date   |   SP |   Quantity (MW) |
|-------------:|:----------------------|:-------------------------------|:-------------|:-----------------|:-----------|:----------------------------------|:---------------------------|:-----------------------------------|:------------------|-----:|----------------:|
|            0 | ELX-EMFIP-AGOG-TS-319 | 48W00000LNCSO-1R               | T_LNCSW-1    | LNCSO-1          | Generation | 48W00000LNCSO-1R                  | T_LNCSW-1                  | LNCSO-1                            | 2020-01-01        |    1 |          56.076 |
|            1 | ELX-EMFIP-AGOG-TS-320 | 48W00000LNCSO-2P               | T_LNCSW-2    | LNCSO-2          | Generation | 48W00000LNCSO-2P                  | T_LNCSW-2                  | LNCSO-2                            | 2020-01-01        |    1 |          47.456 |
|            2 | ELX-EMFIP-AGOG-TS-175 | 48W00000CLDRW-16               | E_CLDRW-1    | CLDRW-1          | Generation | 48W00000CLDRW-16                  | E_CLDRW-1                  | CLDRW-1                            | 2020-01-01        |    1 |           3.096 |</div>



<br>

If you wish to use `ServiceType=xml` you can use the `ElexonDataPortal.dev.utils.parse_xml_response` function to convert the response into a Pandas DataFrame.

```python
r = dev.raw.get_B1610(
    APIKey=api_key,
    SettlementDate='2020-01-01',
    Period='1',
    NGCBMUnitID='*',
    ServiceType='xml',
)

df_B1610_raw_xml = dev.utils.parse_xml_response(r)

df_B1610_raw_xml.head(3)
```




|   Unnamed: 0 | documentType      | businessType   | processType   | timeSeriesID          | curveType                   | settlementDate   | powerSystemResourceType   | registeredResourceEICCode   | marketGenerationUnitEICCode   | marketGenerationBMUId   | ...   | bMUnitID    | nGCBMUnitID   | activeFlag   | documentID              |   documentRevNum | resolution   | start      | end        |   settlementPeriod |   quantity |
|-------------:|:------------------|:---------------|:--------------|:----------------------|:----------------------------|:-----------------|:--------------------------|:----------------------------|:------------------------------|:------------------------|:------|:------------|:--------------|:-------------|:------------------------|-----------------:|:-------------|:-----------|:-----------|-------------------:|-----------:|
|            0 | Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-212 | Sequential fixed size block | 2020-01-01       | Generation                | 48W000CAS-BEU01F            | 48W000CAS-BEU01F              | M_CAS-BEU01             | ...   | M_CAS-BEU01 | CAS-BEU01     | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     18.508 |
|            1 | Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-355 | Sequential fixed size block | 2020-01-01       | Generation                | 48W00000STLGW-3A            | 48W00000STLGW-3A              | T_STLGW-3               | ...   | T_STLGW-3   | STLGW-3       | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     28.218 |
|            2 | Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-278 | Sequential fixed size block | 2020-01-01       | Generation                | 48W00000GNFSW-1H            | 48W00000GNFSW-1H              | T_GNFSW-1               | ...   | T_GNFSW-1   | GNFSW-1       | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     29.44  |</div>



<br>

But how do we go from these raw methods to the standardised client that we first saw?

The glue that enables this is the `ElexonDataPortal.dev.orchestrator.query_orchestrator` function which provides a wrapper for the various request types. Crucially, the `query_orchestrator` provides a mechanism for collating requests over a date range with the different request types broken down into:

* SP_and_date
* date_range
* date_time_range
* year
* year_and_month
* year_and_week
* non_temporal

Let's make a request to the same BMRS stream using the orchestrator.

```python
start_date = '2020-01-01'
end_date = '2020-01-01'

df_B1610_orchestrator = dev.orchestrator.query_orchestrator(
    api_key=api_key,
    start_date=start_date,
    end_date=end_date,
    method='get_B1610',
    request_type='SP_and_date',
    kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
    func_params=['APIKey', 'date', 'SP', 'ServiceType'],
)

df_B1610_orchestrator.head(3)
```

    B1610: 100%|â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ| 1/1 [00:01<00:00,  1.65s/it]
    




|   Unnamed: 0 | documentType      | businessType   | processType   | timeSeriesID          | curveType                   | settlementDate   | powerSystemResourceType   | registeredResourceEICCode   | marketGenerationUnitEICCode   | marketGenerationBMUId   | ...   | nGCBMUnitID   | activeFlag   | documentID              |   documentRevNum | resolution   | start      | end        |   settlementPeriod |   quantity | local_datetime            |
|-------------:|:------------------|:---------------|:--------------|:----------------------|:----------------------------|:-----------------|:--------------------------|:----------------------------|:------------------------------|:------------------------|:------|:--------------|:-------------|:------------------------|-----------------:|:-------------|:-----------|:-----------|-------------------:|-----------:|:--------------------------|
|            0 | Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-212 | Sequential fixed size block | 2020-01-01       | Generation                | 48W000CAS-BEU01F            | 48W000CAS-BEU01F              | M_CAS-BEU01             | ...   | CAS-BEU01     | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     18.508 | 2020-01-01 00:00:00+00:00 |
|            1 | Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-355 | Sequential fixed size block | 2020-01-01       | Generation                | 48W00000STLGW-3A            | 48W00000STLGW-3A              | T_STLGW-3               | ...   | STLGW-3       | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     28.218 | 2020-01-01 00:00:00+00:00 |
|            2 | Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-278 | Sequential fixed size block | 2020-01-01       | Generation                | 48W00000GNFSW-1H            | 48W00000GNFSW-1H              | T_GNFSW-1               | ...   | GNFSW-1       | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     29.44  | 2020-01-01 00:00:00+00:00 |</div>



<br>

It's worth noting that there are some differences in the returned DataFrames. Firstly, when specifying `ServiceType=csv` the number of columns is much smaller as the data that is nested within the xml representation is simply not included. Secondly, the orchestrator response includes an additional column relative to the xml one even though it itself specifies `ServiceType=xml`, this is because the orchestrator introduces a new column containing the local datetime as Pandas Timestamps.

```python
(
    df_B1610_raw_csv.columns.size, 
    df_B1610_raw_xml.columns.size, 
    df_B1610_orchestrator.columns.size
)
```




    (11, 21, 22)



<br>

The response from the `ElexonDataPortal.api.Client` is the same as that returned by the orchestrator.

```python
(df_B1610.columns == df_B1610_orchestrator.columns).mean() == 1
```




    True


