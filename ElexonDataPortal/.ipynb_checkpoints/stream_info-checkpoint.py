streams = {
    'B1420' : {
        'name' : 'Installed Generation Capacity per Unit',
        'request_type' : 'standalone', # standalone refers to the fact this stream is not distinct on an SP by SP or date range basis
        'data_parse_type' : 'dataframe',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'year' : 'Year',
        },
    },
    'B1440' : {
        'name' : 'Day-Ahead Generation forecasts for Wind and Solar',
        'request_type' : 'SP_by_SP',
        'date_col' : 'settlementDate',
        'SP_col' : 'settlementPeriod',
        'data_parse_type' : 'dataframe',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'query_date' : 'SettlementDate',
            'SP' : 'Period',
        },
    },
    'B1610' : {
        'name' : 'Actual Generation Output per Generation Unit',
        'data_parse_type' : 'dataframe',
        'request_type' : 'SP_by_SP',
        'API_version' : '2',
        'optional_params' : {
            'BMU_id' : 'NGCBMUnitID'
        },
        'required_params' : {
            'query_date' : 'SettlementDate',
            'SP' : 'Period',
        },
    },
    'B1630' : {
        'name' : 'Actual or Estimated Wind and Solar Power Generation',
        'data_parse_type' : 'dataframe',
        'request_type' : 'SP_by_SP',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'query_date' : 'SettlementDate',
            'SP' : 'Period',
        },
    },
    'B1750' : {
        'name' : 'Activated Balancing Energy',
        'request_type' : 'SP_by_SP',
        'data_parse_type' : 'dataframe',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'query_date' : 'SettlementDate',
            'SP' : 'Period',
        },
    },
    'B1760' : {
        'name' : 'Prices Of Activated Balancing Energy',
        'request_type' : 'SP_by_SP',
        'data_parse_type' : 'dataframe',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'query_date' : 'SettlementDate',
            'SP' : 'Period',
        },
    },
    'B1770' : {
        'name' : 'Imbalance Prices',
        'request_type' : 'SP_by_SP',
        'data_parse_type' : 'dataframe',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'query_date' : 'SettlementDate',
            'SP' : 'Period',
        },
    },
    'B1780' : {
        'name' : 'Aggregated Imbalance Volumes',
        'request_type' : 'SP_by_SP',
        'data_parse_type' : 'series',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'query_date' : 'SettlementDate',
            'SP' : 'Period',
        },
    },
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
    'PHYBMDATA' : {
        'name' : 'Physical Data',
        'request_type' : 'SP_by_SP',
        'data_parse_type' : 'dataframe',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'query_date' : 'SettlementDate',
            'SP' : 'SettlementPeriod',
        },
    },
    'FUELHH' : {
        'name' : 'Aggregated Half-Hourly Fuel & Demand',
        'request_type' : 'date_range',
        'date_col' : 'startTimeOfHalfHrPeriod',
        'SP_col' : 'settlementPeriod',
        'data_parse_type' : 'dataframe',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'start_date' : 'FromDate',
            'end_date' : 'ToDate',
        },
    },
    'WINDFORFUELHH' : {
        'name' : 'Aggregated Half-Hourly Wind Generation Forecast and Out-turn',
        'request_type' : 'date_range',
        'date_col' : 'startTimeOfHalfHrPeriod',
        'SP_col' : 'settlementPeriod',
        'data_parse_type' : 'dataframe',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'start_date' : 'FromDate',
            'end_date' : 'ToDate',
        },
    },
    'SYSDEM' : {
        'name' : 'System Demand',
        'request_type' : 'date_range',
        'date_col' : 'startTimeOfHalfHrPeriod',
        'SP_col' : 'settlementPeriod',
        'data_parse_type' : 'dataframe',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'start_date' : 'FromDate',
            'end_date' : 'ToDate',
        },
    },
    'FORDAYDEM' : {
        'name' : 'Forecast Day and Day Ahead Demand Data',
        'request_type' : 'date_range',
        'date_col' : 'settlementDate',
        'SP_col' : 'settlementPeriod',
        'data_parse_type' : 'dataframe',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'start_date' : 'FromDate',
            'end_date' : 'ToDate',
        },
    },
    'MessageListRetrieval' : {
        'name' : 'REMIT Flow – Message List Retrieval',
        'request_type' : 'date_range',
        'date_col' : 'eventStart',
        'data_parse_type' : 'dataframe',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'start_date' : 'EventStart',
            'end_date' : 'EventEnd',
        },
    },
    'MELIMBALNGC' : {
        'name' : 'Forecast Day and Day Ahead Margin and Imbalance Data',
        'request_type' : 'date_range',
        'date_col' : 'settlementDate',
        'SP_col' : 'settlementPeriod',
        'data_parse_type' : 'dataframe',
        'API_version' : '1',
        'optional_params' : None,
        'required_params' : {
            'zone' : 'ZoneIdentifier',
            'start_date' : 'FromDate',
            'end_date' : 'ToDate'
        },
    }, 
}