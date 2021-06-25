# Elexon Data Portal

[![DOI](https://zenodo.org/badge/189842391.svg)](https://zenodo.org/badge/latestdoi/189842391) [![Binder](https://notebooks.gesis.org/binder/badge_logo.svg)](https://notebooks.gesis.org/binder/v2/gh/OSUKED/ElexonDataPortal/master?urlpath=lab%2Ftree%2Fnbs%2F08-quick-start.ipynb) [![PyPI version](https://badge.fury.io/py/ElexonDataPortal.svg)](https://badge.fury.io/py/ElexonDataPortal)

The `ElexonDataPortal` library is a Python Client for retrieving data from the Elexon/BMRS API. The library significantly reduces the complexity of interfacing with the Elexon/BMRS API through the standardisation of parameter names and orchestration of multiple queries when making requests over a date range. To use the `ElexonDataPortal` you will have to register for an Elexon API key which can be done [here](https://www.elexonportal.co.uk/registration/newuser). 

<br>
<br>

### Installation

The library can be easily installed from PyPi, this can be done using:

```bash
pip install ElexonDataPortal
```

<br>
<br>

### Getting Started

We'll begin by initialising the API `Client`. The key parameter to pass here is the `api_key`, alternatively this can be set by specifying the environment variable `BMRS_API_KEY` which will then be loaded automatically.

```python
from ElexonDataPortal import api

client = api.Client('your_api_key_here')
```

<br>

Now that the client has been initialised we can make a request! 

One of the key abstractions within the `ElexonDataPortal` library is the handling of multiple requests over a date range specified through the `start_date` and `end_date` parameters. Each response will be automatically cleaned and parsed, then concatenated into a single Pandas DataFrame. If a settlement period and date column can be identified in the returned data then a new column will be added with the local datetime for each data-point. N.b. that if passed as a string the start and end datetimes will be assumed to be in the local timezone for the UK

```python
start_date = '2020-01-01'
end_date = '2020-01-01 1:30'

df_B1610 = client.get_B1610(start_date, end_date)

df_B1610.head(3)
```

|    | documentType      | businessType   | processType   | timeSeriesID          | curveType                   | settlementDate   | powerSystemResourceType   | registeredResourceEICCode   | marketGenerationUnitEICCode   | marketGenerationBMUId   | marketGenerationNGCBMUId   | bMUnitID    | nGCBMUnitID   | activeFlag   | documentID              |   documentRevNum | resolution   | start      | end        |   settlementPeriod |   quantity | local_datetime            |
|---:|:------------------|:---------------|:--------------|:----------------------|:----------------------------|:-----------------|:--------------------------|:----------------------------|:------------------------------|:------------------------|:---------------------------|:------------|:--------------|:-------------|:------------------------|-----------------:|:-------------|:-----------|:-----------|-------------------:|-----------:|:--------------------------|
|  0 | Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-212 | Sequential fixed size block | 2020-01-01       | Generation                | 48W000CAS-BEU01F            | 48W000CAS-BEU01F              | M_CAS-BEU01             | CAS-BEU01                  | M_CAS-BEU01 | CAS-BEU01     | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     18.508 | 2020-01-01 00:00:00+00:00 |
|  1 | Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-355 | Sequential fixed size block | 2020-01-01       | Generation                | 48W00000STLGW-3A            | 48W00000STLGW-3A              | T_STLGW-3               | STLGW-3                    | T_STLGW-3   | STLGW-3       | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     28.218 | 2020-01-01 00:00:00+00:00 |
|  2 | Actual generation | Production     | Realised      | ELX-EMFIP-AGOG-TS-278 | Sequential fixed size block | 2020-01-01       | Generation                | 48W00000GNFSW-1H            | 48W00000GNFSW-1H              | T_GNFSW-1               | GNFSW-1                    | T_GNFSW-1   | GNFSW-1       | Y            | ELX-EMFIP-AGOG-22495386 |                1 | PT30M        | 2020-01-01 | 2020-01-01 |                  1 |     29.44  | 2020-01-01 00:00:00+00:00 |

<br>

If you've previously written your own code for extracting data from the Elexon/BMRS API then you may be wondering where some of the normal parameters you pass have gone. The reduction in the parameters passed are due to 4 core drivers:

* Standardisation of date range parameter names
* Removal of the need to specify `ServiceType`
* Automatic passing of `APIKey` after client initialisation
* Shipped with sensible defaults for all remaining parameters

The full list of data streams that are able to be requested can be found [here](#data-stream-descriptions). If you wish to make requests using the raw methods these are available through the `ElexonDataportal.dev.raw` module.

Further information can be found in the [Quick Start guide](https://osuked.github.io/ElexonDataPortal/08-quick-start/).

<br>
<br>

### What's Changed in v2

The latest release of the library includes a full rewrite of the code-base. We have endeavoured to make the new API as intuitive as possible but that has required breaking changes from v1, if you wish to continue using the historic library use `pip install ElexonDataPortal==1.0.4`. N.b v1 will not be maintained going forward, you are advised to change over to v2.0.0+. 

The key feature changes are:

* Coverage of more BMRS streams 
* Automated default values
* Cleaner client API
* A larger range of request types are compatible with the date range orchestrator

<br>
<br>

### Programmatic Library Generation

One of the core features within the `ElexonDataPortal` library is that it is *self-generating*, by which we mean it can rebuild itself (including any new API request methods) from scratch using only the `endpoints.csv` spreadsheet. As well as generating the Python Client library a `BMRS_API.yaml` file is created, this provides an OpenAPI specification representation of the Elexon/BMRS API. In turn this allows us to automatically generate documentation, as well as run tests on the API itself to ensure that everything is working as expected - during this process we identified and corrected several small errors in the API documentation provided by Elexon. 

To rebuild the library simply run the following in the root directory: 

```bash
python -m ElexonDataPortal.rebuild
```

N.b. If you wish to develop the library further or use any of the programmatic library generation functionality then please install the development version of the library using:

```bash
pip install ElexonDataPortal[dev]
```

If you are not installing into a fresh environment it is recommended you install `pyyaml` and `geopandas` using conda to avoid any dependency conflicts. In future we are looking to release `ElexonDataPortal` as a conda package to avoid these issues.

<br>
<br>

### Data Stream Descriptions

The following table describes the data streams that are currently retreivable through the API. The client method to retrieve data from a given stream follows the naming convention `get_{stream-name}`.

| Stream                 | Description                                                    |
|:-----------------------|:---------------------------------------------------------------|
| B0610                  | Actual Total Load per Bidding Zone                             |
| B0620                  | Day-Ahead Total Load Forecast per Bidding Zone                 |
| B0630                  | Week-Ahead Total Load Forecast per Bidding Zone                |
| B0640                  | Month-Ahead Total Load Forecast Per Bidding Zone               |
| B0650                  | Year Ahead Total Load Forecast per Bidding Zone                |
| B0710                  | Planned Unavailability of Consumption Units                    |
| B0720                  | Changes In Actual Availability Of Consumption Units            |
| B0810                  | Year Ahead Forecast Margin                                     |
| B0910                  | Expansion and Dismantling Projects                             |
| B1010                  | Planned Unavailability In The Transmission Grid                |
| B1020                  | Changes In Actual Availability In The Transmission Grid        |
| B1030                  | Changes In Actual Availability of Offshore Grid Infrastructure |
| B1320                  | Congestion Management Measures Countertrading                  |
| B1330                  | Congestion Management Measures Costs of Congestion Management  |
| B1410                  | Installed Generation Capacity Aggregated                       |
| B1420                  | Installed Generation Capacity per Unit                         |
| B1430                  | Day-Ahead Aggregated Generation                                |
| B1440                  | Generation forecasts for Wind and Solar                        |
| B1510                  | Planned Unavailability of Generation Units                     |
| B1520                  | Changes In Actual Availability of Generation Units             |
| B1530                  | Planned Unavailability of Production Units                     |
| B1540                  | Changes In Actual Availability of Production Units             |
| B1610                  | Actual Generation Output per Generation Unit                   |
| B1620                  | Actual Aggregated Generation per Type                          |
| B1630                  | Actual Or Estimated Wind and Solar Power Generation            |
| B1720                  | Amount Of Balancing Reserves Under Contract Service            |
| B1730                  | Prices Of Procured Balancing Reserves Service                  |
| B1740                  | Accepted Aggregated Offers                                     |
| B1750                  | Activated Balancing Energy                                     |
| B1760                  | Prices Of Activated Balancing Energy                           |
| B1770                  | Imbalance Prices                                               |
| B1780                  | Aggregated Imbalance Volumes                                   |
| B1790                  | Financial Expenses and Income For Balancing                    |
| B1810                  | Cross-Border Balancing Volumes of Exchanged Bids and Offers    |
| B1820                  | Cross-Border Balancing Prices                                  |
| B1830                  | Cross-border Balancing Energy Activated                        |
| BOD                    | Bid Offer Level Data                                           |
| CDN                    | Credit Default Notice Data                                     |
| DETSYSPRICES           | Detailed System Prices                                         |
| DEVINDOD               | Daily Energy Volume Data                                       |
| DISBSAD                | Balancing Services Adjustment Action Data                      |
| FORDAYDEM              | Forecast Day and Day Ahead Demand Data                         |
| FREQ                   | Rolling System Frequency                                       |
| FUELHH                 | Half Hourly Outturn Generation by Fuel Type                    |
| MELIMBALNGC            | Forecast Day and Day Ahead Margin and Imbalance Data           |
| MID                    | Market Index Data                                              |
| MessageDetailRetrieval | REMIT Flow - Message List Retrieval                            |
| MessageListRetrieval   | REMIT Flow - Message List Retrieval                            |
| NETBSAD                | Balancing Service Adjustment Data                              |
| NONBM                  | Non BM STOR Instructed Volume Data                             |
| PHYBMDATA              | Physical Data                                                  |
| SYSDEM                 | System Demand                                                  |
| SYSWARN                | System Warnings                                                |
| TEMP                   | Temperature Data                                               |
| WINDFORFUELHH          | Wind Generation Forecast and Out-turn Data                     |