# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/vis-00-gen.ipynb (unless otherwise specified).

__all__ = ['rgb_2_plt_tuple', 'get_vis_func', 'get_vis_md_text', 'get_rerun_vis_bool', 'update_vis_configs',
           'update_vis', 'generate_vis', 'app']

# Cell
import json
import pandas as pd

import typer
import croniter
import importlib
from tqdm import tqdm

import matplotlib.pyplot as plt

# Cell
def rgb_2_plt_tuple(r, g, b):
    """converts a standard rgb set from a 0-255 range to 0-1"""

    plt_tuple = tuple([x/255 for x in (r, g, b)])

    return plt_tuple

# Cell
def get_vis_func(func_path):
    *lib_path, func_name = func_path.split('.')
    lib_obj = importlib.import_module('.'.join(lib_path))

    func = getattr(lib_obj, func_name)

    return func

def get_vis_md_text(vis_config, docs_dir=None, update_time=None):
    func_path = vis_config['function']
    kwargs = vis_config['kwargs']

    if (docs_dir is not None) and ('docs_dir' in kwargs.keys()):
        kwargs['docs_dir'] = docs_dir

    if (update_time is not None) and ('update_time' in kwargs.keys()):
        kwargs['update_time'] = update_time

    vis_func = get_vis_func(func_path)
    vis_md_text = vis_func(**kwargs)
    plt.close()

    return vis_md_text

# Cell
def get_rerun_vis_bool(vis_config):
    if 'last_update_time' not in vis_config.keys():
        return True
    else:
        last_update_time = pd.to_datetime(vis_config['last_update_time']).tz_localize('Europe/London')

    cron = croniter.croniter(vis_config['cron'], pd.Timestamp.now()-pd.Timedelta(weeks=1))
    cron_dts = pd.to_datetime([cron.get_next() for i in range(2*24*7)], unit='s').tz_localize('UTC').tz_convert('Europe/London')

    s_cron_dts_time_delta_to_now = pd.Series((cron_dts - pd.Timestamp.now(tz='Europe/London')).total_seconds())
    assert (s_cron_dts_time_delta_to_now<0).sum()>0 and (s_cron_dts_time_delta_to_now>0).sum()>0, 'The cron dts being assessed do not cross the current time'

    s_cron_dts_time_delta_to_last_update_time = pd.Series((cron_dts - last_update_time).total_seconds())
    if s_cron_dts_time_delta_to_now.abs().idxmin() == s_cron_dts_time_delta_to_last_update_time.abs().idxmin():
        return False

    avg_adj_dt_time_delta_s = pd.Series(cron_dts).diff(1).dropna().dt.total_seconds().mean()
    min_time_delta_s = s_cron_dts_time_delta_to_now.abs().min()

    rerun_vis = avg_adj_dt_time_delta_s >= min_time_delta_s

    return rerun_vis

# Cell
def update_vis_configs(
    vis_configs,
    docs_dir: str='docs',
    override_rerun_vis_bool: bool=False
):
    for i, vis_config in enumerate(vis_configs):
        update_time = pd.Timestamp.now().round('5min').strftime('%Y-%m-%d %H:%M')
        rerun_vis = get_rerun_vis_bool(vis_config)

        if override_rerun_vis_bool == True:
            rerun_vis = True

        if rerun_vis == True:
            vis_md_text = get_vis_md_text(vis_config, docs_dir=docs_dir, update_time=update_time)
            vis_configs[i]['md_text'] = vis_md_text
            vis_configs[i]['last_update_time'] = update_time

    return vis_configs

# Cell
app = typer.Typer()

@app.command()
def update_vis(
    docs_dir: str='docs',
    data_dir: str='data',
    override_rerun_vis_bool: bool=False
):
    with open(f'{data_dir}/vis_configs.json', 'r') as f:
        vis_configs = json.load(f)

    vis_configs = update_vis_configs(vis_configs, docs_dir=docs_dir, override_rerun_vis_bool=override_rerun_vis_bool)

    with open(f'{data_dir}/vis_configs.json', 'w') as f:
        json.dump(vis_configs, f)

    prefix_text = """# Visualisations

On this page you can view visualisations of key phenomena in the GB power sector, ranging from long-term trends in the generation-mix and market prices to information on excess capacity in the grid. All data used in these visualisations was either sourced directly from BMRS using the `ElexonDataPortal` client, or has been derived from BMRS data streams. As with the other components of the `ElexonDataPortal` the code to generate these visualisations is open-source and users are welcome to contribute their own visualisations, for more detail on how to do this please refer to the [user contribution guide](#contributor-guide)
    """

    suffix_text = """### Contributor Guide

We encourage users to contribute their own visualisations which the `ElexonDataPortal` will then update automatically. To this end the library adopts a standardised format for generating visualisations, the core component of which is the `data/vis_configs.json` file to which you will have to add detail on your visualisation function:

```javascript
[
    ...
    {
        "cron": "0 * * * *", # the update schedule, in this instance to run at midnight every monday
        "function": "path_to_function", # e.g. ElexonDataPortal.vis.generate_vis
        "kwargs": {
            'api_key': null,  # if no api_key is passed then the client will try and look for the `BMRS_API_KEY` environment variable
            'update_time': null, # if no update_time is passed you should generate it yourself, e.g. with `pd.Timestamp.now().round('5min').strftime('%Y-%m-%d %H:%M')`
            'docs_dir': 'docs', # in almost all circumstances this should just be `docs`
            "optional_kwarg": "optional_value" # you can specify any additional keyword arguments that your function requires
        }
    },
    ...
]
```

<br>

The other core component is writing the function that generates the visualisation. This function should require parameters for the `docs_dir`, `api_key`, and `update_time` but can include optional parameters that you wish to specify, it should then return markdown text which will be used to populate the *Visualisations* page. These functions will normally contain three steps: data retrieval, generating the visualisation, and generating the accompanying text - an example can be seen below.

```python
import pandas as pd
import matplotlib.pyplot as plt
from ..api import Client

def generate_vis(
    docs_dir: str='docs',
    api_key: str=None,
    update_time: str=pd.Timestamp.now().round('5min').strftime('%Y-%m-%d %H:%M'),
) -> str:

    # Data Retrieval
    client = Client(api_key=api_key)
    df = client.get_data_stream(param1, param2)

    # Generating the Visualisation
    fig, ax = plt.subplots(dpi=150)
    df.plot(ax=ax)
    fig.savefig(f'{docs_dir}/img/vis/great_vis_name.png')

    # Generating the Text
    md_text = f\"\"\"### Title

Explanation of what your visualisation shows

![](img/vis/great_vis_name.png)
\"\"\"

    return md_text
```

N.b. the path to the image should be relative to the `docs` directory.

If you require any assistance in this process please start a discussion [here](https://github.com/OSUKED/ElexonDataPortal/discussions) and we'll endeavour to help as best we can.
"""

    all_vis_md_texts = [prefix_text] + [vis_config['md_text'] for vis_config in vis_configs] + [suffix_text]
    combined_md_text = '\n\n<br>\n\n'.join(all_vis_md_texts)

    with open(f'{docs_dir}/vis-contrib.md', 'w', encoding='utf-8') as f:
        f.write(combined_md_text)

    return

if __name__ == '__main__' and '__file__' in globals():
    app()