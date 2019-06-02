#################################
## BMRS API Data Stream Caller ##
#################################

"""
To Do:

* Watch out for max returns, e.g. 200 on WINDFORFUELHH but way more for FUELHH

"""

## Imports
import pandas as pd
import numpy as np
from datetime import timedelta, datetime, date

from collections import OrderedDict
import warnings
import xmltodict

import requests
from urllib import parse


def create_df_dt_rng(start_date, end_date, freq='30T', tz='Europe/London', dt_str_template='%Y-%m-%d'):
    ## Creating localised datetime index
    s_dt_rng = pd.date_range(start_date, end_date, freq=freq, tz=tz)
    s_dt_SP_count = pd.Series(0, index=s_dt_rng).resample('D').count()

    ## Creating SP column
    SPs = []
    for num_SPs in list(s_dt_SP_count):
        SPs += list(range(1, num_SPs+1))

    ## Creating datetime dataframe
    df_dt_rng = pd.DataFrame(index=s_dt_rng)
    df_dt_rng.index.name = 'local_datetime'

    ## Adding query call cols
    df_dt_rng['SP'] = SPs
    df_dt_rng['date'] = df_dt_rng.index.strftime(dt_str_template)

    return df_dt_rng

def get_missing_dates(s_datetime, df_dt_rng):
    s_unique_dts = s_datetime.astype('datetime64[ns]').unique() 
    missing_dates = list(set(df_dt_rng.index.values) - set(s_unique_dts))

    return missing_dates

def get_start_end_date(local_kws):
    start_and_end_date_given = len(set(['start_date', 'end_date']) - set(local_kws.keys())) == 0

    if start_and_end_date_given:
        start_date = local_kws['start_date']
        end_date = local_kws['end_date']
    else:
        raise ValueError('No start or end date was provided')
        
    return start_date, end_date

def add_local_datetime(df_dt_rng, df, date_col='settlementDate', SP_col='settlementPeriod'):
    s_dt_rng_date_SP = df_dt_rng['date'].astype(str) + ' ' + df_dt_rng['SP'].astype(str)
    s_df_date_SP = df[date_col] + ' ' + df[SP_col]
    
    dt_rng_map = dict(zip(s_dt_rng_date_SP, df_dt_rng.index))

    s_local_datetime = s_df_date_SP.map(dt_rng_map)
    df['local_datetime'] = s_local_datetime
    
    return df

def format_date(_date):
    if isinstance(_date, datetime):
        _date = _date.date()
        return _date
    elif isinstance(_date, date):
        return _date
    else:
        raise ValueError(f'end and start date should be given as date objects, instead were given: {type(_date)}')


## Classes
class Caller(object):
    
    """
    This is an API caller object for the BMRS data streams.
    
    Given an API key and data stream ID the Caller is initialized.
    The Caller's query function is then called with the relevant kwargs for the data stream.
    The url is constructed using the kwargs and the request made, returning the response
    
    """ 
    
    
    ## ~~~~~~~~~~~~ Core Call Functions ~~~~~~~~~~~~
        
    def create_url(self, *args, **kwargs):
        ## Creating a mapper for the url template using the kwargs passed in to the query function and the API key
        url_mapper = locals()['kwargs']
        url_mapper['api_key'] = self.key
            
        ## Mapping the kwargs and key onto the url template from the 'stream_url_dict'
        url = self.stream_url_dict[self.stream]['url'].format_map(url_mapper).replace(' ', '')
        
        return url
        
    def make_call(self, url):
        header = { 'Accept': 'application/xml' }
        response = requests.get(url, headers=header)
        
        return response
    
    def query(self, *args, **kwargs):
        url = self.create_url(*args, **kwargs)
        response = self.make_call(url)
        
        self.latest_response = response
        return response
    
    
    ## ~~~~~~~~~~~~ Dataframe Parser ~~~~~~~~~~~~
        
    def call_2_df(self, *args, **kwargs):
        response = self.query(self, *args, **kwargs) # Run the query, response is saved
        df = self.response_2_df(response) # Converts the response to a dataframe
        
        return df
    
    def response_2_df(self, response):
        
        response_2_API_response = self.check_response(response)
    
        if response_2_API_response != 'OK':
            ## Should log if this is the case
            return response_2_API_response
        
        ## Converting response to df
        r_dict = xmltodict.parse(response.text)['response']['responseBody']['responseList']['item']

        if isinstance(r_dict, OrderedDict):
            df = pd.DataFrame(r_dict, index=[1])
        else:
            df = pd.DataFrame(r_dict)

        return df
    
    
    ## ~~~~~~~~~~~~ Query Managers ~~~~~~~~~~~~

    def call(self, *args, **kwargs):
        caller_name = self.stream_url_dict[self.stream]['caller']
        caller_func = self.caller_dict[caller_name]
        
        df = caller_func(*args, **kwargs)

        return df
    
    def SP_date_range_to_df(self, *args, **kwargs):
        ## Collecting start and end date from keywords
        local_kws = locals()['kwargs']
        start_date, end_date = get_start_end_date(local_kws)
        
        ## Creating datetime range with dates and SPs
        start_date, end_date = format_date(start_date), format_date(end_date)
        df_dt_rng = create_df_dt_rng(start_date, end_date)
        comb_df = pd.DataFrame()

        ## Pulling out SP, date and datetime values
        SPs = df_dt_rng['SP'].values
        dates = df_dt_rng['date'].values
        local_datetimes = df_dt_rng.index

        ## Iterating over dates and SPs
        for i in range(SPs.size):
            SP = SPs[i]
            date = dates[i]
            local_datetime = local_datetimes[i]
                
            try:
                df_gen_SP = self.call_2_df(SP=SP, query_date=date, **kwargs) # Temp dataframe is made from json at url
                
                if df_gen_SP is not None:
                    df_gen_SP['local_datetime'] = local_datetime
                    comb_df = comb_df.append(df_gen_SP) # Temp dataframe is appended to the main dataframe
                
            except:
                warnings.warn(f'API Call failed at SP: {SP}, Date: {date}')

        ## Checking if any dates are missing
        missing_dates = get_missing_dates(comb_df['local_datetime'], df_dt_rng)

        if len(missing_dates) > 0:
            warnings.warn(f'Missing dates: {missing_dates}')

        ## Setting and returning the combined dataframe       
        comb_df = comb_df.reset_index(drop=True)
        return comb_df

    def non_SP_date_range_to_df(self, num_missing_dt=-1, *args, **kwargs):
        local_kws = locals()['kwargs']
        start_date, end_date = get_start_end_date(local_kws)
        df_dt_rng = create_df_dt_rng(start_date, end_date)

        kwargs.update(start_date = format_date(start_date))
        kwargs.update(end_date = format_date(end_date))

        df = self.call_2_df(self, *args, **kwargs)
        
        ## Adding local_datetime col
        if 'datetime_cols' in self.stream_url_dict[self.stream].keys():
            date_col = self.stream_url_dict[self.stream]['datetime_cols']['date_col']
            SP_col = self.stream_url_dict[self.stream]['datetime_cols']['SP_col']
            df = add_local_datetime(df_dt_rng, df, date_col=date_col, SP_col=SP_col)
        else:
            df = add_local_datetime(df_dt_rng, df)

        ## Checking missing dates
        missing_dates = get_missing_dates(df['local_datetime'], df_dt_rng)
        new_num_missing_dt = len(missing_dates)

        ## Handle missing dates
        if new_num_missing_dt == 0:
            df = df.reset_index(drop=True)
            return df

        elif (new_num_missing_dt > 0) and (new_num_missing_dt == num_missing_dt):
            warnings.warn(f'Returned {df_dt_rng.shape[0] - num_missing_dt} datetimes\nMissing: {missing_dates}')
            
            df = df.reset_index(drop=True)
            return df

        else:
            s_bool_missing_match = df_dt_rng.index.isin(pd.to_datetime(missing_dates))
            df_dt_rng_new = df_dt_rng[s_bool_missing_match]

            kwargs.update(start_date = format_date(df_dt_rng_new.index.min()))
            kwargs.update(end_date = format_date(df_dt_rng_new.index.max()))
            kwargs.update(num_missing_dt = num_missing_dt)

            missing_df = self.non_SP_date_range_to_df(self, *args, **kwargs)
            df = df.append(missing_df)

            df = df.reset_index(drop=True)
            return df
          
        
    ## ~~~~~~~~~~~~ Initializer & Helper Functions ~~~~~~~~~~~~
    
    def info(self):
        info_dict = {
            'key' : self.key,
            'stream' : self.stream
        }
        
        return info_dict
    
    def check_response(self, response):
        ## Checking http code in response
        
        http_code = xmltodict.parse(response.text)['response']['responseMetadata']['httpCode']
        
        def f_pass():
            return 'OK'
        def f_return_blank_df():
            return pd.DataFrame()
        
        http_code_response_dict = {
            '200' : f_pass(),
            '204' : f_return_blank_df(),
        }
        
        if http_code in http_code_response_dict.keys():
            response_2_API_response = http_code_response_dict[http_code]
            return response_2_API_response
        else:
            warnings.warn(f'HTTP code {http_code} could not be handled.')
    
    def __init__(self, key, stream):
        self.key = key
        self.stream = stream

        self.caller_dict = {
            'date_range_to_df' : self.SP_date_range_to_df,
            'non_SP_call' : self.non_SP_date_range_to_df,
        }
    
        
    ##  Data Objects 
    
    ## Dictionary containing the urls for the different data streams
    ## Long term look into using 'urllib.parse.urlencode' to create the url template
    stream_url_dict = {

        ## Actual Generation Output per Generation Unit
        'B1610' : {
            'url' : '\
            https://api.bmreports.com/BMRS/B1610/v1?\
            APIKey={api_key}&\
            SettlementDate={query_date}&\
            Period={SP}&\
            NGCBMUnitID={unit_id}&\
            ServiceType=xml',
            'freq' : '30T',
            'caller' : 'date_range_to_df'
        },

        ## Half Hourly Outturn Generation by Fuel Type
        'FUELHH' : {
            'url' : '\
            https://api.bmreports.com/BMRS/FUELHH/v1?\
            APIKey={api_key}&\
            FromDate={start_date}&\
            ToDate={end_date}&\
            ServiceType=xml',
            'freq' : '30T',
            'caller' : 'non_SP_call',
            'datetime_cols' : {
                'date_col' : 'startTimeOfHalfHrPeriod',
                'SP_col' : 'settlementPeriod',
            }            
        },

        ## Bid Offer Level Data
        'BOD' : {
            'url' : '\
            https://api.bmreports.com/BMRS/BOD/v1?\
            APIKey={api_key}&\
            SettlementDate={query_date}&\
            SettlementPeriod={SP}&\
            BMUnitId={unit_id}&\
            ServiceType=xml',
            'freq' : '30T',
            'caller' : 'date_range_to_df'
        },
        
        ## Imbalance Prices
        'B1770' : {
            'url' : '\
            https://api.bmreports.com/BMRS/B1770/v1?\
            APIKey={api_key}&\
            SettlementDate={query_date}&\
            Period={SP}&\
            ServiceType=xml',
            'freq' : '30T',
            'caller' : 'date_range_to_df'
        },
        
        ## Aggregated Imbalance Volumes
        'B1780' : {
            'url' : '\
            https://api.bmreports.com/BMRS/B1780/v1?\
            APIKey={api_key}&\
            SettlementDate={query_date}&\
            Period={SP}&\
            ServiceType=xml',
            'freq' : '30T',
            'caller' : 'date_range_to_df'
        },
        
        ## Detailed System Prices
        'DETSYSPRICES' : {
            'url' : '\
            https://api.bmreports.com/BMRS/DETSYSPRICES/v1?\
            APIKey={api_key}&\
            SettlementDate={query_date}&\
            SettlementPeriod={SP}&\
            ServiceType=xml',
            'freq' : '30T',
            'caller' : 'date_range_to_df'
        },
        
        ## Wind Generation Forecast and Out-turn Data
        'WINDFORFUELHH' : {
            'url' : '\
            https://api.bmreports.com/BMRS/WINDFORFUELHH/v1?\
            APIKey={api_key}&\
            FromDate={start_date}&\
            ToDate={end_date}&\
            ServiceType=xml',
            'freq' : '30T',
            'caller' : 'non_SP_call',
        },
        
        ##  Day-Ahead Generation forecasts for Wind and Solar
        'B1440' : {
            'url' : '\
            https://api.bmreports.com/BMRS/B1440/v1?\
            APIKey={api_key}&\
            SettlementDate={query_date}&\
            Period={SP}&\
            ServiceType=xml',
            'freq' : '30T',
            'caller' : 'date_range_to_df'
        },
        
        ## Actual Or Estimated Wind and Solar Power Generation
        'B1630' : {
            'url' : '\
            https://api.bmreports.com/BMRS/B1630/v1?\
            APIKey={api_key}&\
            SettlementDate={query_date}&\
            Period={SP}&\
            ServiceType=xml',
            'freq' : '30T',
            'caller' : 'date_range_to_df'
        },
        
        # Demand Forecast
        'B0620' : {
            'url' : '\
            https://api.bmreports.com/BMRS/B0620/v1?\
            APIKey={api_key}&\
            SettlementDate={query_date}&\
            Period={SP}&\
            ServiceType=xml',
            'freq' : '30T',
            'caller' : 'date_range_to_df'
        },
        
        # Forecast Day and Day Ahead Margin and Imbalance
        'MELIMBALNGC' : {
            'url' : '\
            https://api.bmreports.com/BMRS/MELIMBALNGC/v1?\
            APIKey={api_key}&\
            ZoneIdentifier={zone}&\
            FromDate={start_date}&\
            ToDate={end_date}&\
            ServiceType=xml',
            'freq' : '30T',
            'caller' : 'non_SP_call',
        },

    } 

    
