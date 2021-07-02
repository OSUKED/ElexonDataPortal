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
        
    {% for stream in streams %}
    def {{ stream['name'] }}(
        self,{% if stream['request_type'] not in ['non_temporal'] %}
        start_date: str='{{ stream['date_range_example'][0] }}', 
        end_date: str='{{ stream['date_range_example'][1] }}',{% endif %}{% for kwarg in stream['extra_kwargs'] %}
        {{ kwarg['name'] }}: str='{{ kwarg['example'] }}',{% endfor %}
    ):
        """
        {{ stream['description'] }}
        
        Parameters:{% if stream['request_type'] not in ['non_temporal'] %}
            start_date (str)
            end_date (str){% endif %}{% for kwarg in stream['extra_kwargs'] %}
            {{ kwarg['name'] }} (str){% endfor %}
        """
        
        df = orchestrator.query_orchestrator(
            method='{{ stream['name'] }}',
            api_key=self.api_key,
            n_attempts=self.n_retry_attempts,
            request_type='{{ stream['request_type'] }}',
            kwargs_map={{ stream['kwargs_map'] }},
            func_params={{ stream['func_params'] }},{% if stream['request_type'] not in ['non_temporal'] %}
            start_date=start_date,
            end_date=end_date,{% endif %}{% for kwarg in stream['extra_kwargs'] %}
            {{ kwarg['name'] }}={{ kwarg['name'] }},{% endfor %}
        )
        
        return df
    
    {% endfor %}