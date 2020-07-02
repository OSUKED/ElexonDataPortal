# ElexonDataPortal

<br>

## About the ElexonDataPortal Python API Wrapper

The ElexonDataPortal python wrapper is a project being developed within the UCL Energy & AI research group. It aims to provide an easy to use wrapper which enables data retrieval from a wide range of resources relating to UK electricity demand, generation and markets.

The ElexonDataPortal provides the ability to download data directly from the Elexon API and have it parsed into a user-friendly Pandas dataframe. All queries require both a stream name and query arguments, all query argument information can be found <a href="https://www.elexon.co.uk/wp-content/uploads/2018/09/BMRS-API-Data-Push-User-Guide.pdf">here</a>. Previous users of Elexon data will have had to switch between many different naming conventions for query arguments, the ElexonDataPortal harmonises these so that instead of using one of say <i>FromDate</i>, <i>EventStart</i> or <i>SettlementDate</i> we would use <i>start_date</i> for all of them.

You will also have to have an Elexon API key which you will receive after registering <a href="https://www.elexonportal.co.uk/registration/newuser?cachebust=e2242lmr6w">here</a>. 

The module can be installed with

```bash
pip install ElexonDataPortal
```

<br>
<br>

## Using the ElexonDataPortal Python API Wrapper

### Making Standalone Queries

Elexon allows you to query data in a very limited fashion, often constrained to returning individual settlment periods. These queries are exposed through the default query function from the API wrapper.

```python
stream = 'B1630'

query_args = {
    'query_date' : '2019-09-25',
    'SP' : 48,
}

df_RES_gen = edp_wrapper.query(stream, query_args)

df_RES_gen
```

<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>timeSeriesID</th>      <th>businessType</th>      <th>powerSystemResourceType</th>      <th>settlementDate</th>      <th>settlementPeriod</th>      <th>quantity</th>      <th>documentType</th>      <th>processType</th>      <th>curveType</th>      <th>resolution</th>      <th>activeFlag</th>      <th>documentID</th>      <th>documentRevNum</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>NGET-EMFIP-AGWS-TS-00291950</td>      <td>Solar generation</td>      <td>"Solar"</td>      <td>2019-09-25</td>      <td>48</td>      <td>0</td>      <td>Wind and solar generation</td>      <td>Realised</td>      <td>Sequential fixed size block</td>      <td>PT30M</td>      <td>Y</td>      <td>NGET-EMFIP-AGWS-00145968</td>      <td>1</td>    </tr>    <tr>      <th>1</th>      <td>NGET-EMFIP-AGWS-TS-00291951</td>      <td>Wind generation</td>      <td>"Wind Offshore"</td>      <td>2019-09-25</td>      <td>48</td>      <td>79.657</td>      <td>Wind and solar generation</td>      <td>Realised</td>      <td>Sequential fixed size block</td>      <td>PT30M</td>      <td>Y</td>      <td>NGET-EMFIP-AGWS-00145968</td>      <td>1</td>    </tr>    <tr>      <th>2</th>      <td>NGET-EMFIP-AGWS-TS-00291952</td>      <td>Wind generation</td>      <td>"Wind Onshore"</td>      <td>2019-09-25</td>      <td>48</td>      <td>1342.004</td>      <td>Wind and solar generation</td>      <td>Realised</td>      <td>Sequential fixed size block</td>      <td>PT30M</td>      <td>Y</td>      <td>NGET-EMFIP-AGWS-00145968</td>      <td>1</td>    </tr>  </tbody></table>

<br>

### Orchestrating Multiple Queries

Where the standard <i>query</i> call will carry out individual requests for data from Elexon, the <i>query orchestrator</i> accepts a date range and repeatedly requests data over it. Alongside the start and end dates for the period in question any additional parameters which you would make in a standalone call can also be included.

```python
stream = 'FUELHH'

query_args = {
    'start_date' : '2019-09-25',
    'end_date' : '2019-09-25 23:30',
}

df_generation = edp_wrapper.query_orchestrator(stream, query_args)

df_generation.head()
```
<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>recordType</th>      <th>startTimeOfHalfHrPeriod</th>      <th>settlementPeriod</th>      <th>ccgt</th>      <th>oil</th>      <th>coal</th>      <th>nuclear</th>      <th>wind</th>      <th>ps</th>      <th>npshyd</th>      <th>ocgt</th>      <th>other</th>      <th>intfr</th>      <th>intirl</th>      <th>intned</th>      <th>intew</th>      <th>biomass</th>      <th>intnem</th>      <th>activeFlag</th>      <th>local_datetime</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>FUELHH</td>      <td>2019-09-25</td>      <td>1</td>      <td>7965</td>      <td>0</td>      <td>0</td>      <td>6598</td>      <td>4245</td>      <td>0</td>      <td>293</td>      <td>1</td>      <td>80</td>      <td>1502</td>      <td>0</td>      <td>760</td>      <td>0</td>      <td>1753</td>      <td>0</td>      <td>Y</td>      <td>2019-09-25 00:00:00+01:00</td>    </tr>    <tr>      <th>1</th>      <td>FUELHH</td>      <td>2019-09-25</td>      <td>2</td>      <td>7405</td>      <td>0</td>      <td>0</td>      <td>6596</td>      <td>4376</td>      <td>0</td>      <td>292</td>      <td>1</td>      <td>79</td>      <td>1504</td>      <td>0</td>      <td>758</td>      <td>0</td>      <td>1756</td>      <td>0</td>      <td>Y</td>      <td>2019-09-25 00:30:00+01:00</td>    </tr>    <tr>      <th>2</th>      <td>FUELHH</td>      <td>2019-09-25</td>      <td>3</td>      <td>7423</td>      <td>0</td>      <td>0</td>      <td>6595</td>      <td>4243</td>      <td>0</td>      <td>290</td>      <td>2</td>      <td>80</td>      <td>1502</td>      <td>0</td>      <td>758</td>      <td>0</td>      <td>1758</td>      <td>0</td>      <td>Y</td>      <td>2019-09-25 01:00:00+01:00</td>    </tr>    <tr>      <th>3</th>      <td>FUELHH</td>      <td>2019-09-25</td>      <td>4</td>      <td>7574</td>      <td>0</td>      <td>0</td>      <td>6600</td>      <td>4020</td>      <td>0</td>      <td>301</td>      <td>2</td>      <td>78</td>      <td>1504</td>      <td>0</td>      <td>758</td>      <td>0</td>      <td>1755</td>      <td>0</td>      <td>Y</td>      <td>2019-09-25 01:30:00+01:00</td>    </tr>    <tr>      <th>4</th>      <td>FUELHH</td>      <td>2019-09-25</td>      <td>5</td>      <td>7811</td>      <td>0</td>      <td>0</td>      <td>6596</td>      <td>3920</td>      <td>0</td>      <td>280</td>      <td>1</td>      <td>77</td>      <td>1502</td>      <td>0</td>      <td>758</td>      <td>0</td>      <td>1754</td>      <td>0</td>      <td>Y</td>      <td>2019-09-25 02:00:00+01:00</td>    </tr>  </tbody></table>

<br>
<br>

### We Need Your Help!

Currently a number of commonly used streams are included as part of the module. Unfortunately as there are over 100 streams in total, and as Elexon is planning a new data <a href="https://www.elexon.co.uk/about/about-elexon/foundation-programme-2018/">Foundation Platform</a>, it was not deemed viable to initially include each and every stream. Instead the module has been made to be extendable so that new streams can be added for those who require them. If you add new streams please make a Git request to add them to the main module!

Information for each stream is laid out in the format below. The request type refers to whether the existing Elexon API queries data on a settlement period by settlement period basis or by accepting a date range. The required params is a dictionary which maps this modules harmonised names (e.g. query_date and SP) to the Elexon data stream param names (e.g. SettlementDate, SettlementPeriod) which vary from stream to stream. 

```python
'DETSYSPRICES' : {
    'name' : 'Detailed System Prices',
    'request_type' : 'SP_by_SP',
    'data_parse_type' : 'dataframe',
    'API_version' : '1',
    'optional_params' : None,
    'required_params' : {
        'query_date' : 'SettlementDate',
        'SP' : 'SettlementPeriod',
    },
},
```

We are also looking for any contributions for data cleaners and plotters which can be used for specific streams. Currently these are limited to just Balancing Market streams.
