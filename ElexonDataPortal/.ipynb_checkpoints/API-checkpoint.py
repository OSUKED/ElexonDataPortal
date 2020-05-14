## ~~~~~ Imports ~~~~~

## Data Manipulation
import pandas as pd
import numpy as np

## Plotting
import seaborn as sns
import matplotlib.pyplot as plt

## Scraping
import requests
import xmltodict

## OS Related
import os
from os import listdir
from os.path import isfile, join

## Datetime Handling
from datetime import timedelta, datetime, date
import time

## Miscellaneous
import time
import warnings
import collections
from ipypb import track

## Stream Data
from ElexonDataPortal import stream_info


## ~~~~~ Helper Functions/Classes ~~~~~

class RequestError(Exception):
    def __init__(self, http_code, error_type, description):
        self.message = f'{http_code} - {error_type}\n{description}'
        
    def __str__(self):
        return self.message
    

## ~~~~~ Core Wrapper Class ~~~~~

class Wrapper:
    def dt_rng_2_SPs(self, start_date:datetime, end_date:datetime, freq='30T', tz='Europe/London'):
        dt_rng = pd.date_range(start_date, end_date, freq=freq, tz=tz)
        dt_strs = dt_rng.strftime('%Y-%m-%d')

        dt_SP_counts = pd.Series(dt_strs).groupby(dt_strs).count()
        SPs = []

        for num_SPs in dt_SP_counts.values:
            SPs += [SP+1 for SP in list(range(num_SPs))]

        df_dates_SPs = pd.DataFrame({'date':dt_strs, 'SP':SPs}, index=dt_rng)

        return df_dates_SPs
    
    def add_local_datetime(self, df:pd.DataFrame, start_date:str, end_date:str, stream:str):
        """
        Accepts a dataframe, start and end date, and date and SP columns in the dataframe
        creates a mapping from date and SP columns to the local datetime, 
        then maps the data and adds the new column to the dataframe.
        """
        
        stream_metadata = stream_info.streams[stream]
        
        assert all(col in stream_metadata.keys() for col in ['date_col', 'SP_col']), f'{stream}\'s metadata does not contain the required date_col and SP_col parameters'

        ## Adding End-Date Margin
        end_date = (pd.to_datetime(end_date) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')

        ## Creating Date & SP to Timestamp Map
        ts_2_dt_SPs = self.dt_rng_2_SPs(start_date, end_date)

        date_SP_tuples = list(zip(ts_2_dt_SPs['date'], ts_2_dt_SPs['SP']))
        dt_SP_2_ts = dict(zip(date_SP_tuples, ts_2_dt_SPs.index))

        ## Mapping & Setting Datetimes
        s_dt_SPs = pd.Series(zip(df[stream_info.streams[stream]['date_col']], df[stream_info.streams[stream]['SP_col']].astype(int)), index=df.index)

        df['local_datetime'] = s_dt_SPs.map(dt_SP_2_ts)

        return df
    
    def expand_cols(self, df, cols_2_expand=[]):
        for col in cols_2_expand:
            new_df_cols = df[col].apply(pd.Series)

            df[new_df_cols.columns] = new_df_cols
            df = df.drop(columns=col)

        s_cols_2_expand = df.iloc[0].apply(type).isin([collections.OrderedDict, dict, list, tuple])

        if s_cols_2_expand.sum() > 0:
            cols_2_expand = s_cols_2_expand[s_cols_2_expand].index
            df = self.expand_cols(df, cols_2_expand)

        return df
    
    
    def check_response(self, r_metadata):
        if r_metadata['httpCode'] != '200':
            raise RequestError(r_metadata['httpCode'], r_metadata['errorType'], r_metadata['description'])
            
        if 'cappingApplied' in r_metadata.keys():
            if r_metadata['cappingApplied'] == 'Yes':
                self.capping_applied = True
            else:
                self.capping_applied = False
        else:
            self.capping_applied = 'Could not be determined'
    
    
    def check_and_parse_query_args(self, query_args, stream):
        ## ~~~~~ Parsing args ~~~~~ 
        ## Creating new params dictionary
        stream_params = dict()
        stream_params.update({'APIKey':'APIKey', 'ServiceType':'ServiceType'})

        ## If dictionary of query parameter mappings exist then add it to the stream_params
        for param_type in ['required_params', 'optional_params']:
            if stream_info.streams[stream][param_type]:
                stream_params.update(stream_info.streams[stream][param_type])

        ## ~~~~~ Checking args ~~~~~
        extra_args = list(set(query_args.keys()) - set(stream_params.keys()))
        missing_args = list(set(stream_params.keys()) - set(query_args.keys()) - set(['APIKey', 'ServiceType']))
        
        assert(len(missing_args)) == 0, f'The following arguments were needed but not provided: {", ".join(missing_args)}'
        if len(extra_args) != 0:
            warnings.warn(f'The following arguments were provided but not needed: {", ".join(extra_args)}')
            for key in extra_args:
                query_args.pop(key, None)
        
        ## ~~~~ Mapping args ~~~~~
        ## Mapping the generalised wrapper parameters to the parameter names expected by the API        
        parsed_query_args = dict((stream_params[key], val) for key, val in query_args.items())
        
        return parsed_query_args
    
    
    def parse_response(self, response, stream):
        r_dict = xmltodict.parse(response.text)
        
        r_metadata = r_dict['response']['responseMetadata']
        self.last_request_metadata = r_metadata
        
        if r_metadata['httpCode'] == '204':
            warnings.warn(f'Data request was succesful but no content was returned')
            return pd.DataFrame()
        
        self.check_response(r_metadata)
        
        content_dict = r_dict['response']['responseBody']['responseList']['item']
        
        data_parse_type = stream_info.streams[stream]['data_parse_type']
        data = self.data_parse_types[data_parse_type](content_dict)
        
        if data_parse_type == 'dataframe':
            df = self.expand_cols(data)
        
        if data_parse_type == 'series':
            df = pd.DataFrame(data).T
        
        return df
        
    
    def make_request(self, stream, query_args, service_type='xml'):
        ## Checking inputs
        assert stream in stream_info.streams.keys(), f'Data stream should be one of: {", ".join(stream_info.streams.keys())}'
        query_args = self.check_and_parse_query_args(query_args, stream)
        
        ## Forming url and request parameters
        url_endpoint = f'https://api.bmreports.com/BMRS/{stream}/v{stream_info.streams[stream]["API_version"]}'

        query_args.update({
            'APIKey' : self.API_key,
            'ServiceType' : self.service_type,
        })
        
        ## Making request
        response = requests.get(url_endpoint, params=query_args)
        return response
    
    
    def query(self, stream, query_args, service_type='xml'):
        response = self.make_request(stream, query_args, service_type)
        df = self.parse_response(response, stream)
        
        return df
    
    
    def query_orchestrator(self, stream, query_args, service_type='xml', track_label=None, wait_time=0):
        check_date_rng_args = lambda query_args: all(x in query_args.keys() for x in ['start_date', 'end_date'])
        
        df = pd.DataFrame()
        
        if stream_info.streams[stream]['request_type'] == 'date_range':
            ## Dealing with date range requests - main concern is whether capping has been applied
            assert check_date_rng_args(query_args), 'All date range queries should be provided with a "start_date" and "end_date".'
            
            self.capping_applied = True
            date_col = stream_info.streams[stream]['date_col']
            start_date, end_date = query_args['start_date'], query_args['end_date']
            
            absolute_start_date = start_date
                    
            while self.capping_applied == True:
                response = self.make_request(stream, query_args, service_type)
                df_new = self.parse_response(response, stream)

                df = df.append(df_new)
                
                assert self.capping_applied != None, 'Whether or not capping limits had been breached could not be found in the response metadata'
                if self.capping_applied == True:
                    start_date = pd.to_datetime(df[date_col]).max().tz_localize(None)
                    warnings.warn(f'Response was capped, request is rerunning for missing data from {start_date}')
                    
                    if pd.to_datetime(start_date) >= pd.to_datetime(end_date):
                        warnings.warn(f'End data ({end_date}) was earlier than start date ({start_date})\nThe start date will be set one day earlier.')
                        start_date = (pd.to_datetime(end_date) - pd.Timedelta(days=1)).strftime('%Y-%m-%d')
                        
                    query_args['start_date'] = start_date
    
            response = self.make_request(stream, query_args, service_type)
            df_new = self.parse_response(response, stream)
            
            df = df.append(df_new)
            
            
        elif stream_info.streams[stream]['request_type'] == 'SP_by_SP':
            ## Dealing with SP by SP requests - main concern is handling daylight savings
            assert check_date_rng_args(query_args), 'All date range queries should be provided with a "start_date" and "end_date".'
            
            start_date, end_date = query_args['start_date'], query_args['end_date']
            
            absolute_start_date = start_date
            
            for key in ['start_date', 'end_date']:
                query_args.pop(key, None)
            
            df_dates_SPs = self.dt_rng_2_SPs(start_date, end_date)
            date_SP_tuples = list(df_dates_SPs.reset_index().itertuples(index=False, name=None))
            
            for datetime, query_date, SP in track(date_SP_tuples, label=track_label, total=len(date_SP_tuples)):
                query_args['query_date'] = query_date
                query_args['SP'] = SP
                
                # request and parse
                response = self.make_request(stream, query_args, service_type)
                df_SP = self.parse_response(response, stream)

                if df_SP.shape[0] != 0:

                    # processing
                    df_SP = self.expand_cols(df_SP)
                    df_SP['datetime'] = datetime

                    # saving
                    df = df.append(df_SP, sort=False)

                time.sleep(wait_time)
            
        df = df.reset_index(drop=True)
        
        df = df[~df.duplicated()]
        
        ## Assigning local_datetime for relevant dt_rng streams
        if all(col in stream_info.streams[stream].keys() for col in ['date_col', 'SP_col']):
            df = self.add_local_datetime(df, absolute_start_date, end_date, stream)
        
        return df
    
    
    def __init__(self, API_key, service_type='xml'):
        self.API_key = API_key
        self.service_type = service_type
    
    data_parse_types = {
        'dataframe' : pd.DataFrame,
        'series' : pd.Series,
    }
    
    last_request_metadata = None
    capping_applied = 'Could not be determined'