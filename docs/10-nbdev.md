# NB-Dev Modification



<br>

### Imports

```python
#exports
from fastcore.foundation import Config, Path
from nbdev import export
import os
import re
```

```python
#exports
_re_version = re.compile('^__version__\s*=.*$', re.MULTILINE)

def update_version():
    "Add or update `__version__` in the main `__init__.py` of the library"
    fname = Config().path("lib_path")/'__init__.py'
    if not fname.exists(): fname.touch()
    version = f'__version__ = "{Config().version}"'
    with open(fname, 'r') as f: code = f.read()
    if _re_version.search(code) is None: code = version + "\n" + code
    else: code = _re_version.sub(version, code)
    with open(fname, 'w') as f: f.write(code)
```

```python
export.update_version = update_version

update_version()
```

```python
#exports
def add_init(path, contents=''):
    "Add `__init__.py` in all subdirs of `path` containing python files if it's not there already"
    for p,d,f in os.walk(path):
        for f_ in f:
            if f_.endswith('.py'):
                if not (Path(p)/'__init__.py').exists(): (Path(p)/'__init__.py').write_text('\n'+contents)
                break

def update_version(init_dir=None, extra_init_contents=''):
    "Add or update `__version__` in the main `__init__.py` of the library"
    version = Config().version
    version_str = f'__version__ = "{version}"'
    
    if init_dir is None: path = Config().path("lib_path")
    else: path = Path(init_dir)
    fname = path/'__init__.py'
    
    if not fname.exists(): add_init(path, contents=extra_init_contents)
        
    code = f'{version_str}\n{extra_init_contents}'
    with open(fname, 'w') as f: f.write(code)
                
export.add_init = add_init
export.update_version = update_version
```

```python
#exports
def prepare_nbdev_module(extra_init_contents=''):
    export.reset_nbdev_module()
    export.update_version(extra_init_contents=extra_init_contents)
    export.update_baseurl()
```

```python
prepare_nbdev_module()
```

```python
#exports
def notebook2script(fname=None, silent=False, to_dict=False, bare=False, extra_init_contents=''):
    "Convert notebooks matching `fname` to modules"
    # initial checks
    if os.environ.get('IN_TEST',0): return  # don't export if running tests
    if fname is None: prepare_nbdev_module(extra_init_contents=extra_init_contents)
        
    files = export.nbglob(fname=fname)
    d = collections.defaultdict(list) if to_dict else None
    modules = export.create_mod_files(files, to_dict, bare=bare)
    
    for f in sorted(files): d = export._notebook2script(f, modules, silent=silent, to_dict=d, bare=bare)
    if to_dict: return d
    else: add_init(Config().path("lib_path"))
    
    return
```

```python
notebook2script()
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
def add_mod_extra_indices(mod, extra_modules_to_source):
    for extra_module, module_source in extra_modules_to_source.items():
        extra_module_fp = export.Config().path("lib_path")/extra_module

        with open(extra_module_fp, 'r') as text_file:
             extra_module_code = text_file.read()

        names = export.export_names(extra_module_code)
        mod.index.update({name: module_source for name in names})
        
    return mod

def add_mod_extra_modules(mod, extra_modules):
    extra_modules = [e for e in extra_modules if e not in mod.modules]
    mod.modules = sorted(mod.modules + extra_modules)
    
    return mod

def add_extra_code_desc_to_mod(
    extra_modules_to_source = {
        'api.py': '06-client-gen.ipynb', 
        'dev/raw.py': '03-raw-methods.ipynb'
    }
):
    mod = export.get_nbdev_module()

    mod = add_mod_extra_indices(mod, extra_modules_to_source)
    mod = add_mod_extra_modules(mod, extra_modules_to_source.keys())

    export.save_nbdev_module(mod)
    
    return
```

```python
# add_extra_code_desc_to_mod()
```
