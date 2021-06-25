# Command Line Interface - Library Rebuilding



<br>

### Imports

```python
#exports
import typer
import shutil
import pandas as pd
from fastcore.foundation import Config

from ElexonDataPortal.dev import nbdev, specgen, rawgen, clientgen
```

```python
#exports
app = typer.Typer()
```

```python
#exports
@app.command()
def rebuild_library():
    lib_path = str(Config().path('lib_path'))
    dir_root = f'{lib_path}/..'
    endpoints_fp = f'{dir_root}/data/endpoints.csv'
    
    shutil.rmtree(lib_path)
    nbdev.prepare_nbdev_module()
    nbdev.notebook2script()
    
    df_endpoints = specgen.load_endpoints_df(endpoints_fp)
    API_spec = specgen.construct_spec(df_endpoints)
    
    specgen.save_spec(
        API_spec,
        in_fp=f'{dir_root}/templates/open_api_spec.yaml',
        out_fp=f'{dir_root}/data/BMRS_API.yaml'
    )
    
    rawgen.save_methods(
        functions=rawgen.construct_all_functions(specgen.load_API_yaml(fp=f'{dir_root}/data/BMRS_API.yaml')),
        in_fp=f'{dir_root}/templates/raw_methods.py',
        out_fp=f'{dir_root}/ElexonDataPortal/dev/raw.py'
    )
    
    clientgen.save_api_client(
        API_yaml_fp=f'{dir_root}/data/BMRS_API.yaml',
        in_fp=f'{dir_root}/templates/api.py',
        out_fp=f'{dir_root}/ElexonDataPortal/api.py'
    )
    
    nbdev.add_extra_code_desc_to_mod()
    
    return
```

```python
rebuild_library()
```

    Converted 00-documentation.ipynb.
    Converted 01-utils.ipynb.
    Converted 02-spec-gen.ipynb.
    Converted 03-raw-methods.ipynb.
    Converted 04-client-prep.ipynb.
    Converted 05-orchestrator.ipynb.
    Converted 06-client-gen.ipynb.
    Converted 07-cli-rebuild.ipynb.
    Converted 08-quick-start.ipynb.
    Converted 09-map-gen.ipynb.
    Converted 10-nbdev.ipynb.
    Converted Example Usage.ipynb.
    

```python
#exports
if __name__ == '__main__' and '__file__' in globals():
    app()
```
