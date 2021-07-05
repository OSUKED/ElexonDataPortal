import os
from ElexonDataPortal.dev import orchestrator

class Client:
    def __init__(self, api_key: str=None, n_retry_attempts: int=3):
        if api_key is None:
            assert 'BMRS_API_KEY' in os.environ.keys(), 'If the `api_key` is not specified during client initialisation then it must be set to as the environment variable `BMRS_API_KEY`'
            api_key = os.environ['BMRS_API_KEY']
            
        self.api_key = api_key
        self.n_retry_attempts = n_retry_attempts
        
        self.set_method_descs()
        
        return
        
    def set_method_descs(self):
        get_methods_names = [attr for attr in dir(self) if attr[:4]=='get_']
        get_method_descs = [getattr(self, get_methods_name).__doc__.split('\n')[1].strip() for get_methods_name in get_methods_names]

        self.methods = dict(zip(get_methods_names, get_method_descs))
        
    
    def get_B0610(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Actual Total Load per Bidding Zone
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B0610',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B0620(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Day-Ahead Total Load Forecast per Bidding Zone
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B0620',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B0630(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-06-01',
    ):
        """
        Week-Ahead Total Load Forecast per Bidding Zone
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B0630',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='year_and_week',
            kwargs_map={'year': 'Year', 'week': 'Week'},
            func_params=['APIKey', 'year', 'week', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B0640(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-06-01',
    ):
        """
        Month-Ahead Total Load Forecast Per Bidding Zone
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B0640',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='year_and_month',
            kwargs_map={'year': 'Year', 'month': 'Month'},
            func_params=['APIKey', 'year', 'month', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B0650(
        self,
        start_date: str='2019-01-01', 
        end_date: str='2021-01-01',
    ):
        """
        Year Ahead Total Load Forecast per Bidding Zone
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B0650',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='year',
            kwargs_map={'year': 'Year'},
            func_params=['APIKey', 'year', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B0710(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Planned Unavailability of Consumption Units
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B0710',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_time_range',
            kwargs_map={'end_time': 'EndTime', 'start_time': 'StartTime', 'start_date': 'StartDate', 'end_date': 'EndDate'},
            func_params=['APIKey', 'end_time', 'start_time', 'start_date', 'end_date', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B0720(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Changes In Actual Availability Of Consumption Units
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B0720',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_time_range',
            kwargs_map={'start_date': 'StartDate', 'start_time': 'StartTime', 'end_date': 'EndDate', 'end_time': 'EndTime'},
            func_params=['APIKey', 'start_date', 'start_time', 'end_date', 'end_time', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B0810(
        self,
        start_date: str='2019-01-01', 
        end_date: str='2021-01-01',
    ):
        """
        Year Ahead Forecast Margin
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B0810',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='year',
            kwargs_map={'year': 'Year'},
            func_params=['APIKey', 'year', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B0910(
        self,
        start_date: str='2019-01-01', 
        end_date: str='2021-01-01',
    ):
        """
        Expansion and Dismantling Projects
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B0910',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='year',
            kwargs_map={'year': 'Year'},
            func_params=['APIKey', 'year', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1010(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Planned Unavailability In The Transmission Grid
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1010',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_time_range',
            kwargs_map={'start_date': 'StartDate', 'end_date': 'EndDate', 'start_time': 'StartTime', 'end_time': 'EndTime'},
            func_params=['APIKey', 'start_date', 'end_date', 'start_time', 'end_time', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1020(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Changes In Actual Availability In The Transmission Grid
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1020',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_time_range',
            kwargs_map={'start_date': 'StartDate', 'end_date': 'EndDate', 'start_time': 'StartTime', 'end_time': 'EndTime'},
            func_params=['APIKey', 'start_date', 'end_date', 'start_time', 'end_time', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1030(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Changes In Actual Availability of Offshore Grid Infrastructure
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1030',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_time_range',
            kwargs_map={'start_date': 'StartDate', 'end_date': 'EndDate', 'start_time': 'StartTime', 'end_time': 'EndTime'},
            func_params=['APIKey', 'start_date', 'end_date', 'start_time', 'end_time', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1320(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Congestion Management Measures Countertrading
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1320',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1330(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-06-01',
    ):
        """
        Congestion Management Measures Costs of Congestion Management
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1330',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='year_and_month',
            kwargs_map={'year': 'Year', 'month': 'Month'},
            func_params=['APIKey', 'year', 'month', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1410(
        self,
        start_date: str='2019-01-01', 
        end_date: str='2021-01-01',
    ):
        """
        Installed Generation Capacity Aggregated
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1410',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='year',
            kwargs_map={'year': 'Year'},
            func_params=['APIKey', 'year', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1420(
        self,
        start_date: str='2019-01-01', 
        end_date: str='2021-01-01',
    ):
        """
        Installed Generation Capacity per Unit
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1420',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='year',
            kwargs_map={'year': 'Year'},
            func_params=['APIKey', 'year', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1430(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Day-Ahead Aggregated Generation
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1430',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1440(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
        ProcessType: str='Day Ahead',
    ):
        """
        Generation forecasts for Wind and Solar
        
        Parameters:
            start_date (str)
            end_date (str)
            ProcessType (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1440',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ProcessType', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
            ProcessType=ProcessType,
        )
        
        return df
    
    
    def get_B1510(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Planned Unavailability of Generation Units
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1510',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_time_range',
            kwargs_map={'start_date': 'StartDate', 'end_date': 'EndDate', 'start_time': 'StartTime', 'end_time': 'EndTime'},
            func_params=['APIKey', 'start_date', 'end_date', 'start_time', 'end_time', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1520(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Changes In Actual Availability of Generation Units
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1520',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_time_range',
            kwargs_map={'start_date': 'StartDate', 'end_date': 'EndDate', 'start_time': 'StartTime', 'end_time': 'EndTime'},
            func_params=['APIKey', 'start_date', 'end_date', 'start_time', 'end_time', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1530(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Planned Unavailability of Production Units
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1530',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_time_range',
            kwargs_map={'start_date': 'StartDate', 'end_date': 'EndDate', 'start_time': 'StartTime', 'end_time': 'EndTime'},
            func_params=['APIKey', 'start_date', 'end_date', 'start_time', 'end_time', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1540(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Changes In Actual Availability of Production Units
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1540',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_time_range',
            kwargs_map={'start_date': 'StartDate', 'end_date': 'EndDate', 'start_time': 'StartTime', 'end_time': 'EndTime'},
            func_params=['APIKey', 'start_date', 'end_date', 'start_time', 'end_time', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1610(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
        NGCBMUnitID: str='*',
    ):
        """
        Actual Generation Output per Generation Unit
        
        Parameters:
            start_date (str)
            end_date (str)
            NGCBMUnitID (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1610',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'NGCBMUnitID', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
            NGCBMUnitID=NGCBMUnitID,
        )
        
        return df
    
    
    def get_B1620(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Actual Aggregated Generation per Type
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1620',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1630(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Actual Or Estimated Wind and Solar Power Generation
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1630',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1720(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Amount Of Balancing Reserves Under Contract Service
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1720',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1730(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Prices Of Procured Balancing Reserves Service
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1730',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1740(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Accepted Aggregated Offers
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1740',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1750(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Activated Balancing Energy
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1750',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1760(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Prices Of Activated Balancing Energy
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1760',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1770(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Imbalance Prices
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1770',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1780(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Aggregated Imbalance Volumes
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1780',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1790(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-06-01',
    ):
        """
        Financial Expenses and Income For Balancing
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1790',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='year_and_month',
            kwargs_map={'year': 'Year', 'month': 'Month'},
            func_params=['APIKey', 'year', 'month', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1810(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Cross-Border Balancing Volumes of Exchanged Bids and Offers
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1810',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1820(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Cross-Border Balancing Prices
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1820',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_B1830(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Cross-border Balancing Energy Activated
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_B1830',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_BOD(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
        BMUnitId: str='2__AEENG000, G, E.ON Energy, Solutions Limited, EAS-EST01',
        BMUnitType: str='G, S, E, I, T, etc',
        LeadPartyName: str='AES New Energy Limited',
        NGCBMUnit: str='EAS-ASP01, AES New Energy Limited, G, 2__AAEPD000',
        Name: str='2__AAEPD000',
    ):
        """
        Bid Offer Level Data
        
        Parameters:
            start_date (str)
            end_date (str)
            BMUnitId (str)
            BMUnitType (str)
            LeadPartyName (str)
            NGCBMUnit (str)
            Name (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_BOD',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'SettlementPeriod'},
            func_params=['APIKey', 'date', 'SP', 'BMUnitId', 'BMUnitType', 'LeadPartyName', 'NGCBMUnit', 'Name', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
            BMUnitId=BMUnitId,
            BMUnitType=BMUnitType,
            LeadPartyName=LeadPartyName,
            NGCBMUnit=NGCBMUnit,
            Name=Name,
        )
        
        return df
    
    
    def get_CDN(
        self,
        FromClearedDate: str='2021-01-01',
        ToClearedDate: str='2021-01-02',
    ):
        """
        Credit Default Notice Data
        
        Parameters:
            FromClearedDate (str)
            ToClearedDate (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_CDN',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='non_temporal',
            kwargs_map={},
            func_params=['APIKey', 'FromClearedDate', 'ToClearedDate', 'ServiceType'],
            FromClearedDate=FromClearedDate,
            ToClearedDate=ToClearedDate,
        )
        
        return df
    
    
    def get_DETSYSPRICES(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Detailed System Prices
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_DETSYSPRICES',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'SettlementPeriod'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_DEVINDOD(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Daily Energy Volume Data
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_DEVINDOD',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_range',
            kwargs_map={'start_date': 'FromDate', 'end_date': 'ToDate'},
            func_params=['APIKey', 'start_date', 'end_date', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_DISBSAD(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
    ):
        """
        Balancing Services Adjustment Action Data
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_DISBSAD',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'SettlementPeriod'},
            func_params=['APIKey', 'date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_FORDAYDEM(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
        ZoneIdentifier: str='N',
    ):
        """
        Forecast Day and Day Ahead Demand Data
        
        Parameters:
            start_date (str)
            end_date (str)
            ZoneIdentifier (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_FORDAYDEM',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_range',
            kwargs_map={'start_date': 'FromDate', 'end_date': 'ToDate'},
            func_params=['APIKey', 'ZoneIdentifier', 'start_date', 'end_date', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
            ZoneIdentifier=ZoneIdentifier,
        )
        
        return df
    
    
    def get_FREQ(
        self,
        FromDateTime: str='2021-01-01 00:01:00',
        ToDateTime: str='2021-02-01 23:59:00',
    ):
        """
        Rolling System Frequency
        
        Parameters:
            FromDateTime (str)
            ToDateTime (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_FREQ',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='non_temporal',
            kwargs_map={},
            func_params=['APIKey', 'FromDateTime', 'ToDateTime', 'ServiceType'],
            FromDateTime=FromDateTime,
            ToDateTime=ToDateTime,
        )
        
        return df
    
    
    def get_FUELHH(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Half Hourly Outturn Generation by Fuel Type
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_FUELHH',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_range',
            kwargs_map={'start_date': 'FromDate', 'end_date': 'ToDate'},
            func_params=['APIKey', 'start_date', 'end_date', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_LOLPDRM(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Loss of Load Probability and De-rated Margin
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_LOLPDRM',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_range',
            kwargs_map={'start_date': 'FromSettlementDate', 'end_date': 'ToSettlementDate'},
            func_params=['APIKey', 'start_date', 'end_date', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_MELIMBALNGC(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
        ZoneIdentifier: str='N',
    ):
        """
        Forecast Day and Day Ahead Margin and Imbalance Data
        
        Parameters:
            start_date (str)
            end_date (str)
            ZoneIdentifier (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_MELIMBALNGC',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_range',
            kwargs_map={'start_date': 'FromDate', 'end_date': 'ToDate'},
            func_params=['APIKey', 'ZoneIdentifier', 'start_date', 'end_date', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
            ZoneIdentifier=ZoneIdentifier,
        )
        
        return df
    
    
    def get_MID(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Market Index Data
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_MID',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_range',
            kwargs_map={'start_date': 'FromSettlementDate', 'end_date': 'ToSettlementDate', 'SP': 'Period'},
            func_params=['APIKey', 'start_date', 'end_date', 'SP', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_MessageDetailRetrieval(
        self,
        MessageId: str='',
        ParticipantId: str='',
        SequenceId: str='',
        ActiveFlag: str='N',
    ):
        """
        REMIT Flow - Message List Retrieval
        
        Parameters:
            MessageId (str)
            ParticipantId (str)
            SequenceId (str)
            ActiveFlag (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_MessageDetailRetrieval',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='non_temporal',
            kwargs_map={},
            func_params=['APIKey', 'MessageId', 'ParticipantId', 'SequenceId', 'ActiveFlag', 'ServiceType'],
            MessageId=MessageId,
            ParticipantId=ParticipantId,
            SequenceId=SequenceId,
            ActiveFlag=ActiveFlag,
        )
        
        return df
    
    
    def get_MessageListRetrieval(
        self,
        EventStart: str='2021-01-01',
        EventEnd: str='2021-01-02',
        PublicationFrom: str='2021-01-01',
        PublicationTo: str='2021-01-02',
        ParticipantId: str='',
        MessageID: str='',
        AssetID: str='',
        EventType: str='',
        FuelType: str='',
        MessageType: str='',
        UnavailabilityType: str='',
    ):
        """
        REMIT Flow - Message List Retrieval
        
        Parameters:
            EventStart (str)
            EventEnd (str)
            PublicationFrom (str)
            PublicationTo (str)
            ParticipantId (str)
            MessageID (str)
            AssetID (str)
            EventType (str)
            FuelType (str)
            MessageType (str)
            UnavailabilityType (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_MessageListRetrieval',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='non_temporal',
            kwargs_map={},
            func_params=['APIKey', 'EventStart', 'EventEnd', 'PublicationFrom', 'PublicationTo', 'ParticipantId', 'MessageID', 'AssetID', 'EventType', 'FuelType', 'MessageType', 'UnavailabilityType', 'ServiceType'],
            EventStart=EventStart,
            EventEnd=EventEnd,
            PublicationFrom=PublicationFrom,
            PublicationTo=PublicationTo,
            ParticipantId=ParticipantId,
            MessageID=MessageID,
            AssetID=AssetID,
            EventType=EventType,
            FuelType=FuelType,
            MessageType=MessageType,
            UnavailabilityType=UnavailabilityType,
        )
        
        return df
    
    
    def get_NETBSAD(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
        isTwoDayWindow: str='FALSE',
    ):
        """
        Balancing Service Adjustment Data
        
        Parameters:
            start_date (str)
            end_date (str)
            isTwoDayWindow (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_NETBSAD',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'SettlementPeriod'},
            func_params=['APIKey', 'date', 'SP', 'isTwoDayWindow', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
            isTwoDayWindow=isTwoDayWindow,
        )
        
        return df
    
    
    def get_NONBM(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Non BM STOR Instructed Volume Data
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_NONBM',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_range',
            kwargs_map={'start_date': 'FromDate', 'end_date': 'ToDate'},
            func_params=['start_date', 'end_date', 'APIKey', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_PHYBMDATA(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-01 1:30',
        BMUnitId: str='',
        BMUnitType: str='',
        LeadPartyName: str='',
        NGCBMUnit: str='',
        Name: str='',
    ):
        """
        Physical Data
        
        Parameters:
            start_date (str)
            end_date (str)
            BMUnitId (str)
            BMUnitType (str)
            LeadPartyName (str)
            NGCBMUnit (str)
            Name (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_PHYBMDATA',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='SP_and_date',
            kwargs_map={'date': 'SettlementDate', 'SP': 'SettlementPeriod'},
            func_params=['APIKey', 'date', 'SP', 'BMUnitId', 'BMUnitType', 'LeadPartyName', 'NGCBMUnit', 'Name', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
            BMUnitId=BMUnitId,
            BMUnitType=BMUnitType,
            LeadPartyName=LeadPartyName,
            NGCBMUnit=NGCBMUnit,
            Name=Name,
        )
        
        return df
    
    
    def get_SYSDEM(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        System Demand
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_SYSDEM',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_range',
            kwargs_map={'start_date': 'FromDate', 'end_date': 'ToDate'},
            func_params=['APIKey', 'start_date', 'end_date', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_SYSWARN(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        System Warnings
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_SYSWARN',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_range',
            kwargs_map={'start_date': 'FromDate', 'end_date': 'ToDate'},
            func_params=['APIKey', 'start_date', 'end_date', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_TEMP(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Temperature Data
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_TEMP',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_range',
            kwargs_map={'start_date': 'FromDate', 'end_date': 'ToDate'},
            func_params=['APIKey', 'start_date', 'end_date', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    
    def get_WINDFORFUELHH(
        self,
        start_date: str='2020-01-01', 
        end_date: str='2020-01-07',
    ):
        """
        Wind Generation Forecast and Out-turn Data
        
        Parameters:
            start_date (str)
            end_date (str)
        """
        
        df = orchestrator.query_orchestrator(
            method='get_WINDFORFUELHH',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='date_range',
            kwargs_map={'start_date': 'FromDate', 'end_date': 'ToDate'},
            func_params=['APIKey', 'start_date', 'end_date', 'ServiceType'],
            start_date=start_date,
            end_date=end_date,
        )
        
        return df
    
    