import requests

{% for function in functions %}
def {{ function['name'] }}({% for parameter in function['parameters'] %}
    {{ parameter['name'] }}='{{ parameter['example'] }}',{% endfor %}
    endpoint='{{ function['endpoint'] }}'
):
    """{{ function['description'] }}
    """
    
    params = { {% for parameter in function['parameters'] %}
        '{{ parameter['name'] }}': {{ parameter['name'] }},{% endfor %}
    }
    
    r = requests.get(endpoint, params=params)
    
    return r

{% endfor %}