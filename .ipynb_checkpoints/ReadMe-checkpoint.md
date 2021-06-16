# Elexon Data Portal

[![DOI](https://zenodo.org/badge/189842391.svg)](https://zenodo.org/badge/latestdoi/189842391) [![Binder](https://notebooks.gesis.org/binder/badge_logo.svg)](https://notebooks.gesis.org/binder/v2/gh/OSUKED/ElexonDataPortal/main?urlpath=lab%2Ftree%2Fnbs%2F08-quick-start.ipynb)

The `ElexonDataPortal` library is a Python Client for retrieving data from the Elexon/BMRS API. The library significantly reduces the complexity of interfacing with the Elexon/BMRS API through the standardisation of parameter names and orchestration of multiple queries when making requests over a date range. To use the `ElexonDataPortal` you will have to register for an Elexon API key which can be done [here](https://www.elexonportal.co.uk/registration/newuser). 

<br>
<br>

### Installation

The library can be easily installed from PyPi, this can be done using:

```bash
pip install ElexonDataPortal
```

If you wish to develop the library further or use any of the programmatic library generation functionality then please use:

```bash
pip install ElexonDataPortal[dev]
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

Each response will be automatically cleaned and parsed, then concatenated into a single Pandas DataFrame. This abstraction around date range requests is a key feature within the `ElexonDataPortal` library

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

If you wish to make requests using the raw methods these are available through the `ElexonDataportal.dev.raw` module.

Further information can be found in the [Quick Start notebook](https://github.com/OSUKED/BMRS-Wrapper-v2/blob/main/nbs/08-quick-start.ipynb).

<br>
<br>

### What's Changed in v2.0.0

The latest release of the library includes a full rewrite of the code-base. We have endeavoured to make the new API as intuitive as possible but that has required breaking changes from v1.0.0, if you wish to continue using the historic library use `pip install ElexonDataPortal==1.0.4`. N.b v1.0.0 will not be maintained going forward, you are advised to change over to v2.0.0+. 

The key feature changes are:

* Coverage of more BMRS streams 
* Automated default values
* Cleaner client API
* A larger range of request types are compatible with the date range orchestrator

<br>
<br>

### Programmatic Library Generation

One of the core features within the `ElexonDataPortal` library is that it is *self-generating*, by which we mean it can rebuild itself (including any new API request methods) from scratch using only the `endpoints.csv` spreadsheet. As well as generating the Python Client library a `BMRS_API.yaml` file is created, this provides an OpenAPI specification representation of the Elexon/BMRS API. In turn allows us to automatically generate documentation, as well as run tests on the API itself to ensure that everything is working as expected - during this process we identified and corrected several small errors in the API documentation provided by Elexon. 

To rebuild the library simply run the following in the root directory: 

```bash
python -m ElexonDataPortal.rebuild
```