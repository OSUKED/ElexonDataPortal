import requests


def get_B0610(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B0610/v1'
):
    """Actual Total Load per Bidding Zone
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B0620(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B0620/v1'
):
    """Day-Ahead Total Load Forecast per Bidding Zone
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B0630(
    APIKey='AP8DA23',
    Year='2021',
    Week='22',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B0630/v1'
):
    """Week-Ahead Total Load Forecast per Bidding Zone
    """
    
    params = { 
        'APIKey': APIKey,
        'Year': Year,
        'Week': Week,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B0640(
    APIKey='AP8DA23',
    Year='2021',
    Month='MAR',
    ServiceType='csv/xml/CSV/XML',
    endpoint='https://api.bmreports.com/BMRS/B0640/v1'
):
    """Month-Ahead Total Load Forecast Per Bidding Zone
    """
    
    params = { 
        'APIKey': APIKey,
        'Year': Year,
        'Month': Month,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B0650(
    APIKey='AP8DA23',
    Year='2021',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B0650/v1'
):
    """Year Ahead Total Load Forecast per Bidding Zone
    """
    
    params = { 
        'APIKey': APIKey,
        'Year': Year,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B0710(
    APIKey='AP8DA23',
    EndTime='23:59:59',
    StartTime='00:00:00',
    StartDate='2021-01-01',
    EndDate='2021-01-02',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B0710/v1'
):
    """Planned Unavailability of Consumption Units
    """
    
    params = { 
        'APIKey': APIKey,
        'EndTime': EndTime,
        'StartTime': StartTime,
        'StartDate': StartDate,
        'EndDate': EndDate,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B0720(
    APIKey='AP8DA23',
    StartDate='2021-01-01',
    StartTime='00:00:00',
    EndDate='2021-01-02',
    EndTime='23:59:59',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B0720/v1'
):
    """Changes In Actual Availability Of Consumption Units
    """
    
    params = { 
        'APIKey': APIKey,
        'StartDate': StartDate,
        'StartTime': StartTime,
        'EndDate': EndDate,
        'EndTime': EndTime,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B0810(
    APIKey='AP8DA23',
    Year='2021',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B0810/v1'
):
    """Year Ahead Forecast Margin
    """
    
    params = { 
        'APIKey': APIKey,
        'Year': Year,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B0910(
    APIKey='AP8DA23',
    Year='2021',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B0910/v1'
):
    """Expansion and Dismantling Projects
    """
    
    params = { 
        'APIKey': APIKey,
        'Year': Year,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1010(
    APIKey='AP8DA23',
    StartDate='2021-01-01',
    EndDate='2021-01-02',
    StartTime='00:00:00',
    EndTime='23:59:59',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1010/v1'
):
    """Planned Unavailability In The Transmission Grid
    """
    
    params = { 
        'APIKey': APIKey,
        'StartDate': StartDate,
        'EndDate': EndDate,
        'StartTime': StartTime,
        'EndTime': EndTime,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1020(
    APIKey='AP8DA23',
    StartDate='2021-01-01',
    EndDate='2021-01-02',
    StartTime='00:00:00',
    EndTime='23:59:59',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1020/v1'
):
    """Changes In Actual Availability In The Transmission Grid
    """
    
    params = { 
        'APIKey': APIKey,
        'StartDate': StartDate,
        'EndDate': EndDate,
        'StartTime': StartTime,
        'EndTime': EndTime,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1030(
    APIKey='AP8DA23',
    StartDate='2021-01-01',
    EndDate='2021-01-02',
    StartTime='00:00:00',
    EndTime='23:59:59',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1030/v1'
):
    """Changes In Actual Availability of Offshore Grid Infrastructure
    """
    
    params = { 
        'APIKey': APIKey,
        'StartDate': StartDate,
        'EndDate': EndDate,
        'StartTime': StartTime,
        'EndTime': EndTime,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1320(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1320/v1'
):
    """Congestion Management Measures Countertrading
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1330(
    APIKey='AP8DA23',
    Year='2021',
    Month='Mar',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1330/v1'
):
    """Congestion Management Measures Costs of Congestion Management
    """
    
    params = { 
        'APIKey': APIKey,
        'Year': Year,
        'Month': Month,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1410(
    APIKey='AP8DA23',
    Year='2021',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1410/v1'
):
    """Installed Generation Capacity Aggregated
    """
    
    params = { 
        'APIKey': APIKey,
        'Year': Year,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1420(
    APIKey='AP8DA23',
    Year='2021',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1420/v1'
):
    """Installed Generation Capacity per Unit
    """
    
    params = { 
        'APIKey': APIKey,
        'Year': Year,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1430(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1430/v1'
):
    """Day-Ahead Aggregated Generation
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1440(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ProcessType='Day Ahead',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1440/v1'
):
    """Generation forecasts for Wind and Solar
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ProcessType': ProcessType,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1510(
    APIKey='AP8DA23',
    StartDate='2021-01-01',
    EndDate='2021-01-02',
    StartTime='00:00:00',
    EndTime='23:59:59',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1510/v1'
):
    """Planned Unavailability of Generation Units
    """
    
    params = { 
        'APIKey': APIKey,
        'StartDate': StartDate,
        'EndDate': EndDate,
        'StartTime': StartTime,
        'EndTime': EndTime,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1520(
    APIKey='AP8DA23',
    StartDate='2021-01-01',
    EndDate='2021-01-02',
    StartTime='00:00:00',
    EndTime='23:59:59',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1520/v1'
):
    """Changes In Actual Availability of Generation Units
    """
    
    params = { 
        'APIKey': APIKey,
        'StartDate': StartDate,
        'EndDate': EndDate,
        'StartTime': StartTime,
        'EndTime': EndTime,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1530(
    APIKey='AP8DA23',
    StartDate='2021-01-01',
    EndDate='2021-01-02',
    StartTime='00:00:00',
    EndTime='23:59:59',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1530/v1'
):
    """Planned Unavailability of Production Units
    """
    
    params = { 
        'APIKey': APIKey,
        'StartDate': StartDate,
        'EndDate': EndDate,
        'StartTime': StartTime,
        'EndTime': EndTime,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1540(
    APIKey='AP8DA23',
    StartDate='2021-01-01',
    EndDate='2021-01-02',
    StartTime='00:00:00',
    EndTime='23:59:59',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1540/v1'
):
    """Changes In Actual Availability of Production Units
    """
    
    params = { 
        'APIKey': APIKey,
        'StartDate': StartDate,
        'EndDate': EndDate,
        'StartTime': StartTime,
        'EndTime': EndTime,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1610(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    NGCBMUnitID='*',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1610/v2'
):
    """Actual Generation Output per Generation Unit
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'NGCBMUnitID': NGCBMUnitID,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1620(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1620/v1'
):
    """Actual Aggregated Generation per Type
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1630(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1630/v1'
):
    """Actual Or Estimated Wind and Solar Power Generation
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1720(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1720/v1'
):
    """Amount Of Balancing Reserves Under Contract Service
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1730(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1730/v1'
):
    """Prices Of Procured Balancing Reserves Service
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1740(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1740/v1'
):
    """Accepted Aggregated Offers
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1750(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1750/v1'
):
    """Activated Balancing Energy
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1760(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1760/v1'
):
    """Prices Of Activated Balancing Energy
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1770(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1770/v1'
):
    """Imbalance Prices
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1780(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1780/v1'
):
    """Aggregated Imbalance Volumes
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1790(
    APIKey='AP8DA23',
    Year='2021',
    Month='MAR',
    ServiceType='csv/xml/CSV/XML',
    endpoint='https://api.bmreports.com/BMRS/B1790/v1'
):
    """Financial Expenses and Income For Balancing
    """
    
    params = { 
        'APIKey': APIKey,
        'Year': Year,
        'Month': Month,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1810(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1810/v1'
):
    """Cross-Border Balancing Volumes of Exchanged Bids and Offers
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1820(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1820/v1'
):
    """Cross-Border Balancing Prices
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_B1830(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    Period='1',
    ServiceType='csv',
    endpoint='https://api.bmreports.com/BMRS/B1830/v1'
):
    """Cross-border Balancing Energy Activated
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_BOD(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    SettlementPeriod='12',
    BMUnitId='2__AEENG000, G, E.ON Energy, Solutions Limited, EAS-EST01',
    BMUnitType='G, S, E, I, T, etc',
    LeadPartyName='AES New Energy Limited',
    NGCBMUnit='EAS-ASP01, AES New Energy Limited, G, 2__AAEPD000',
    Name='2__AAEPD000',
    ServiceType='csv/xml/CSV/XML',
    endpoint='https://api.bmreports.com/BMRS/BOD/v1'
):
    """Bid Offer Level Data
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'SettlementPeriod': SettlementPeriod,
        'BMUnitId': BMUnitId,
        'BMUnitType': BMUnitType,
        'LeadPartyName': LeadPartyName,
        'NGCBMUnit': NGCBMUnit,
        'Name': Name,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_CDN(
    APIKey='AP8DA23',
    FromClearedDate='2021-01-01',
    ToClearedDate='2021-01-02',
    ServiceType='xml/XML/csv/CSV',
    endpoint='https://api.bmreports.com/BMRS/CDN/v1'
):
    """Credit Default Notice Data
    """
    
    params = { 
        'APIKey': APIKey,
        'FromClearedDate': FromClearedDate,
        'ToClearedDate': ToClearedDate,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_DETSYSPRICES(
    APIKey='AP8DA23',
    SettlementDate='2014-01-02',
    SettlementPeriod='2',
    ServiceType='xml/XML/csv/CSV',
    endpoint='https://api.bmreports.com/BMRS/DETSYSPRICES/v1'
):
    """Detailed System Prices
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'SettlementPeriod': SettlementPeriod,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_DEVINDOD(
    APIKey='AP8DA23',
    FromDate='2021-01-01',
    ToDate='2021-01-02',
    ServiceType='xml/XML/csv/CSV',
    endpoint='https://api.bmreports.com/BMRS/DEVINDOD/v1'
):
    """Daily Energy Volume Data
    """
    
    params = { 
        'APIKey': APIKey,
        'FromDate': FromDate,
        'ToDate': ToDate,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_DISBSAD(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    SettlementPeriod='1',
    ServiceType='xml/XML/csv/CSV',
    endpoint='https://api.bmreports.com/BMRS/DISBSAD/v1'
):
    """Balancing Services Adjustment Action Data
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'SettlementPeriod': SettlementPeriod,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_FORDAYDEM(
    APIKey='AP8DA23',
    ZoneIdentifier='N',
    FromDate='2021-01-01',
    ToDate='2021-01-02',
    ServiceType='csv/xml/CSV/XML',
    endpoint='https://api.bmreports.com/BMRS/FORDAYDEM/v1'
):
    """Forecast Day and Day Ahead Demand Data
    """
    
    params = { 
        'APIKey': APIKey,
        'ZoneIdentifier': ZoneIdentifier,
        'FromDate': FromDate,
        'ToDate': ToDate,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_FREQ(
    APIKey='AP8DA23',
    FromDateTime='2021-01-01 00:01:00',
    ToDateTime='2021-02-01 23:59:00',
    ServiceType='xml/XML/csv/CSV',
    endpoint='https://api.bmreports.com/BMRS/FREQ/v1'
):
    """Rolling System Frequency
    """
    
    params = { 
        'APIKey': APIKey,
        'FromDateTime': FromDateTime,
        'ToDateTime': ToDateTime,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_FUELHH(
    APIKey='AP8DA23',
    FromDate='44197',
    ToDate='44228',
    ServiceType='csv/xml/CSV/XML',
    endpoint='https://api.bmreports.com/BMRS/FUELHH/v1'
):
    """Half Hourly Outturn Generation by Fuel Type
    """
    
    params = { 
        'APIKey': APIKey,
        'FromDate': FromDate,
        'ToDate': ToDate,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_MELIMBALNGC(
    APIKey='AP8DA23',
    ZoneIdentifier='N',
    FromDate='2021-01-01',
    ToDate='2021-01-02',
    ServiceType='csv/xml/CSV/XML',
    endpoint='https://api.bmreports.com/BMRS/MELIMBALNGC/v1'
):
    """Forecast Day and Day Ahead Margin and Imbalance Data
    """
    
    params = { 
        'APIKey': APIKey,
        'ZoneIdentifier': ZoneIdentifier,
        'FromDate': FromDate,
        'ToDate': ToDate,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_MID(
    APIKey='AP8DA23',
    FromSettlementDate='2021-01-01',
    ToSettlementDate='2021-01-02',
    Period='*',
    ServiceType='csv/CSV/XML/xml',
    endpoint='https://api.bmreports.com/BMRS/MID/v1'
):
    """Market Index Data
    """
    
    params = { 
        'APIKey': APIKey,
        'FromSettlementDate': FromSettlementDate,
        'ToSettlementDate': ToSettlementDate,
        'Period': Period,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_MessageDetailRetrieval(
    APIKey='AP8DA23',
    MessageId='',
    ParticipantId='',
    SequenceId='',
    ActiveFlag='N',
    ServiceType='xml/XML/csv/CSV.',
    endpoint='https://api.bmreports.com/BMRS/MessageDetailRetrieval/v1'
):
    """REMIT Flow - Message List Retrieval
    """
    
    params = { 
        'APIKey': APIKey,
        'MessageId': MessageId,
        'ParticipantId': ParticipantId,
        'SequenceId': SequenceId,
        'ActiveFlag': ActiveFlag,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_MessageListRetrieval(
    APIKey='AP8DA23',
    EventStart='2021-01-01',
    EventEnd='2021-01-02',
    PublicationFrom='2021-01-01',
    PublicationTo='2021-01-02',
    ParticipantId='',
    MessageID='',
    AssetID='',
    EventType='',
    FuelType='',
    MessageType='',
    UnavailabilityType='',
    ServiceType='xml/XML/csv/CSV',
    endpoint='https://api.bmreports.com/BMRS/MessageListRetrieval/v1'
):
    """REMIT Flow - Message List Retrieval
    """
    
    params = { 
        'APIKey': APIKey,
        'EventStart': EventStart,
        'EventEnd': EventEnd,
        'PublicationFrom': PublicationFrom,
        'PublicationTo': PublicationTo,
        'ParticipantId': ParticipantId,
        'MessageID': MessageID,
        'AssetID': AssetID,
        'EventType': EventType,
        'FuelType': FuelType,
        'MessageType': MessageType,
        'UnavailabilityType': UnavailabilityType,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_NETBSAD(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    SettlementPeriod='1',
    isTwoDayWindow='FALSE',
    ServiceType='xml/XML/csv/CSV',
    endpoint='https://api.bmreports.com/BMRS/NETBSAD/v1'
):
    """Balancing Service Adjustment Data
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'SettlementPeriod': SettlementPeriod,
        'isTwoDayWindow': isTwoDayWindow,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_NONBM(
    FromDate='2021-01-01',
    ToDate='2021-01-02',
    APIKey='AP8DA23',
    ServiceType='csv/CSV/XML/xml',
    endpoint='https://api.bmreports.com/BMRS/NONBM/v1'
):
    """Non BM STOR Instructed Volume Data
    """
    
    params = { 
        'FromDate': FromDate,
        'ToDate': ToDate,
        'APIKey': APIKey,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_PHYBMDATA(
    APIKey='AP8DA23',
    SettlementDate='2021-01-01',
    SettlementPeriod='12',
    BMUnitId='',
    BMUnitType='',
    LeadPartyName='',
    NGCBMUnit='',
    Name='',
    ServiceType='csv/xml/CSV/XML',
    endpoint='https://api.bmreports.com/BMRS/PHYBMDATA/v1'
):
    """Physical Data
    """
    
    params = { 
        'APIKey': APIKey,
        'SettlementDate': SettlementDate,
        'SettlementPeriod': SettlementPeriod,
        'BMUnitId': BMUnitId,
        'BMUnitType': BMUnitType,
        'LeadPartyName': LeadPartyName,
        'NGCBMUnit': NGCBMUnit,
        'Name': Name,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_SYSDEM(
    APIKey='AP8DA23',
    FromDate='2021-01-01',
    ToDate='2021-01-02',
    ServiceType='csv/xml/CSV/XML',
    endpoint='https://api.bmreports.com/BMRS/SYSDEM/v1'
):
    """System Demand
    """
    
    params = { 
        'APIKey': APIKey,
        'FromDate': FromDate,
        'ToDate': ToDate,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_SYSWARN(
    APIKey='AP8DA23',
    FromDate='2021-01-01',
    ToDate='2021-01-02',
    ServiceType='csv/CSV/xml/XML',
    endpoint='https://api.bmreports.com/BMRS/SYSWARN/v1'
):
    """System Warnings
    """
    
    params = { 
        'APIKey': APIKey,
        'FromDate': FromDate,
        'ToDate': ToDate,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_TEMP(
    APIKey='AP8DA23',
    FromDate='2021-01-01',
    ToDate='2021-01-02',
    ServiceType='csv/CSV/xml/XML',
    endpoint='https://api.bmreports.com/BMRS/TEMP/v1'
):
    """Temperature Data
    """
    
    params = { 
        'APIKey': APIKey,
        'FromDate': FromDate,
        'ToDate': ToDate,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r


def get_WINDFORFUELHH(
    APIKey='AP8DA23',
    FromDate='2021-01-01',
    ToDate='2021-01-02',
    ServiceType='csv/xml/CSV/XML',
    endpoint='https://api.bmreports.com/BMRS/WINDFORFUELHH/v1'
):
    """Wind Generation Forecast and Out-turn Data
    """
    
    params = { 
        'APIKey': APIKey,
        'FromDate': FromDate,
        'ToDate': ToDate,
        'ServiceType': ServiceType,
    }
    
    r = requests.get(endpoint, params=params)
    
    return r

