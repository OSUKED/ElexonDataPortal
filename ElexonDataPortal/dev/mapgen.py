# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/09-map-gen.ipynb (unless otherwise specified).

__all__ = ['clean_route_gdf', 'load_route_gdf', 'construct_df_PN_pivot_dt_rng', 'construct_PN_pivot_df', 'get_PHYBM_df',
           'download_latest_PHYBM_data', 'get_files', 'load_most_recent_PN_data', 'construct_osuked_id_mappings',
           'extract_PN_ts', 'construct_map_df', 'df_to_gdf', 'construct_map_geojson', 'save_map_geojson',
           'get_nearest_dt_idx', 'generate_map_js', 'generate_map_md', 'app', 'generate_map']

# Cell
import json
import numpy as np
import pandas as pd
import geopandas as gpd

import os
import typer
from tqdm import tqdm
from jinja2 import Template

from . import utils, raw

# Cell
def clean_route_gdf(gdf):
    s_LV_routes = gdf['OPERATING_'].astype(float).fillna(0)<=132
    gdf.loc[s_LV_routes, 'OPERATING_'] = '<=132'
    gdf.loc[~s_LV_routes, 'OPERATING_'] = gdf.loc[~s_LV_routes, 'OPERATING_'].astype(int).astype(str)

    return gdf

def load_route_gdf(data_dir='data'):
    gdf_OHL = gpd.read_file(f'{data_dir}/transmission-system/OHL.shp').to_crs('EPSG:4326')
    gdf_cables = gpd.read_file(f'{data_dir}/transmission-system/Cable.shp').to_crs('EPSG:4326')

    gdf_OHL = clean_route_gdf(gdf_OHL)
    gdf_cables = clean_route_gdf(gdf_cables)

    gdf_route = gdf_OHL.append(gdf_cables)[['OPERATING_', 'geometry']].rename(columns={'OPERATING_': 'kV'})
    gdf_route.to_file(f'{data_dir}/network_routes.json', driver='GeoJSON')

    return gdf_route

# Cell
def construct_df_PN_pivot_dt_rng(df_PN):
    no_seconds = (((df_PN['timeFrom'].str.split(':').str[-1]=='00').mean()==1) &
                  ((df_PN['timeTo'].str.split(':').str[-1]=='00').mean()==1))

    if no_seconds == True:
        dt_rng = pd.date_range(df_PN['timeFrom'].min(), df_PN['timeTo'].max(), freq='min', tz='Europe/London')
    else:
        dt_rng = pd.date_range(df_PN['timeFrom'].min(), df_PN['timeTo'].max(), freq='s', tz='Europe/London')

    return dt_rng

def construct_PN_pivot_df(df_PN, resample=None):
    bmu_ids = sorted(list(df_PN['bmUnitID'].unique()))
    df_PN_pivot = pd.DataFrame(index=construct_df_PN_pivot_dt_rng(df_PN), columns=bmu_ids, dtype=float)

    for bmu_id in tqdm(bmu_ids):
        for idx, row in df_PN.query('bmUnitID==@bmu_id').iterrows():
            df_PN_pivot.loc[pd.to_datetime(row['timeFrom']).tz_localize('Europe/London'), bmu_id] = float(row['pnLevelFrom'])
            df_PN_pivot.loc[pd.to_datetime(row['timeTo']).tz_localize('Europe/London'), bmu_id] = float(row['pnLevelTo'])

        df_PN_pivot[bmu_id] = df_PN_pivot[bmu_id].interpolate()

    if resample is not None:
        df_PN_pivot = df_PN_pivot.resample(resample).mean()

    return df_PN_pivot

def get_PHYBM_df(api_key, start_date=None, end_date=None, record_type='PN', resample='30T'):
    if start_date is None and end_date is None:
        start_date = pd.Timestamp.now().round('30min') - pd.Timedelta(minutes=60*1)
        end_date = pd.Timestamp.now().round('30min') + pd.Timedelta(minutes=180)
    elif start_date is not None and end_date is not None:
        pass
    else:
        raise ValueError('Only one of `start_date` and `end_date` was specified')

    df = pd.DataFrame()
    df_local_datetime_to_date_SP = utils.dt_rng_to_SPs(start_date, end_date)

    for idx, (date, SP) in tqdm(df_local_datetime_to_date_SP.iterrows(), total=df_local_datetime_to_date_SP.shape[0]):
        df_SP = utils.parse_xml_response(raw.get_PHYBMDATA(api_key, SettlementDate=date, SettlementPeriod=SP, ServiceType='xml'))
        df = df.append(df_SP)

    df = (df
          .query(f'recordType=="{record_type}"')
          .dropna(how='all', axis=1)
         )

    if resample is not None:
        df = df.pipe(construct_PN_pivot_df, resample=resample)

    df.index.name = 'local_datetime'

    return df

# Cell
get_files = lambda data_dir: [f for f in os.listdir(data_dir) if '.csv' in f]

def download_latest_PHYBM_data(api_key=None, data_dir='data/PN', record_type='PN'):
    if api_key is None:
        if 'BMRS_API_KEY' in os.environ.keys():
            api_key = os.environ['BMRS_API_KEY']
        else:
            raise ValueError('`api_key` must be passed or set as the environment variable `BMRS_API_KEY`')

    files = get_files(data_dir)
    years_months_downloaded = [f.split('.')[0] for f in files]

    current_ts = pd.Timestamp.now(tz='Europe/London')
    current_year_month = current_ts.strftime('%Y-%m')

    if current_year_month not in years_months_downloaded:
        start_date, end_date = f'{current_year_month}-01 00:00', current_ts.strftime('%Y-%m-%d %H:%M')
        df = get_PHYBM_df(api_key, start_date, end_date, record_type=record_type)
        df.to_csv(f'{data_dir}/{current_year_month}.csv')

    else:
        df = pd.read_csv(f'{data_dir}/{current_year_month}.csv')

        df = df.set_index('local_datetime')
        df.index = pd.to_datetime(df.index, utc=True).tz_convert('Europe/London')
        dt_rng = pd.date_range(df.index.max(), current_ts, freq='30T', tz='Europe/London')

        if dt_rng.size > 1:
            start_date = dt_rng[0] - pd.Timedelta(minutes=30)
            end_date = dt_rng[-1] + pd.Timedelta(minutes=60)

            try:
                df_latest = get_PHYBM_df(api_key, start_date, end_date, record_type=record_type)
                df_trimmed = df.drop(list(set(df_latest.index) - (set(df_latest.index) - set(df.index))))
                df_combined = df_trimmed.append(df_latest).sort_index()
                df_combined.to_csv(f'{data_dir}/{current_year_month}.csv')
            except:
                warn(f'Could not retrieve any new data between {start_date} and {end_date}')

# Cell
def load_most_recent_PN_data(data_dir='data/PN', latest_year_month_file=None, df_PN_old=None):
    if latest_year_month_file is None:
        PN_files = sorted(get_files(data_dir))
        latest_year_month_file = PN_files[-1]

    latest_fp = f'{data_dir}/{latest_year_month_file}'

    df_PN = pd.read_csv(latest_fp)

    df_PN['local_datetime'] = pd.to_datetime(df_PN['local_datetime'], utc=True)
    df_PN = df_PN.set_index('local_datetime')
    df_PN.index = df_PN.index.tz_convert('Europe/London')

    if df_PN_old is not None:
        assert latest_year_month_file is not None, 'Should not be appending to the main dataframe if `latest_year_month_file` was not specified'
        df_PN = df_PN_old.append(df_PN)

    if df_PN.shape[0] < (48*7): # want to have at least a week's worth of data
        assert 'PN_files' in locals(), 'The two most recent files combined have less than one week\'s worth of data'
        df_PN = load_most_recent_PN_data(data_dir, latest_year_month_file=PN_files[-2], df_PN_old=df_PN)

    return df_PN

# Cell
def construct_osuked_id_mappings(df_powerdict):
    osuked_id_mappings = dict()

    osuked_id_mappings['bmu_ids'] = (df_powerdict
                                     .set_index('osuked_id')
                                     ['sett_bmu_id']
                                     .str.split(', ')
                                     .dropna()
                                     .to_dict()
                                    )

    osuked_id_mappings['capacity_mw'] = (df_powerdict
                                         .set_index('osuked_id')
                                         ['capacity_mw']
                                         .fillna('Unknown')
                                         .astype(str)
                                         .str.replace('.0', '', regex=False)
                                         .to_dict()
                                        )

    osuked_id_mappings['fuel_type'] = (df_powerdict
                                       .set_index('osuked_id')
                                       ['fuel_type']
                                       .dropna()
                                       .to_dict()
                                      )

    osuked_id_mappings['name'] = (df_powerdict
                                  .set_index('osuked_id')
                                  ['name']
                                  .dropna()
                                  .to_dict()
                                 )

    osuked_id_mappings['lat_lon'] = (df_powerdict
                                     .set_index('osuked_id')
                                     [['latitude', 'longitude']]
                                     .dropna()
                                     .apply(dict, axis=1)
                                     .to_dict()
                                    )

    return osuked_id_mappings

# Cell
def extract_PN_ts(df_PN, bmu_ids, n_SPs=48*7):
    matching_output_bmu_ids = df_PN.columns.intersection(bmu_ids)
    output_match = matching_output_bmu_ids.size > 0

    if output_match == False:
        return None

    s_PN = df_PN[matching_output_bmu_ids].sum(axis=1)
    s_PN.index = (s_PN.index.tz_convert('UTC') - pd.to_datetime(0, unit='s').tz_localize('UTC')).total_seconds().astype(int) * 1000

    s_PN = s_PN.fillna(0)
    s_PN[s_PN<0] = 0
    PN_ts = s_PN.tail(n_SPs).to_dict()

    return PN_ts

def construct_map_df(
    df_PN,
    osuked_id_to_bmu_ids,
    osuked_id_to_capacity_mw,
    osuked_id_to_lat_lon,
    osuked_id_to_fuel_type,
    osuked_id_to_name,
    n_SPs=48*7
):
    sites_data = list()

    for osuked_id, bmu_ids in osuked_id_to_bmu_ids.items():
        lat_lon_match = osuked_id in osuked_id_to_lat_lon.keys()

        PN_ts = extract_PN_ts(df_PN, bmu_ids, n_SPs=n_SPs)

        if lat_lon_match and PN_ts is not None:
            if sum(PN_ts.values()) > 0:
                site_data = osuked_id_to_lat_lon[osuked_id]
                site_data.update({'id': osuked_id})
                site_data.update({'name': osuked_id_to_name[osuked_id]})
                site_data.update({'capacity': osuked_id_to_capacity_mw[osuked_id]})
                site_data.update({'fuel_type': osuked_id_to_fuel_type[osuked_id]})
                site_data.update({'output': PN_ts})

                sites_data += [site_data]

    df_map = pd.DataFrame(sites_data).set_index('id')

    return df_map

# Cell
def df_to_gdf(df, lat_col='latitude', lon_col='longitude'):
    geometry = gpd.points_from_xy(df[lon_col], df[lat_col])
    gdf = gpd.GeoDataFrame(df, geometry=geometry)

    return gdf

# Cell
def construct_map_geojson(
    df_PN,
    df_powerdict,
    n_SPs=48*7
):
    osuked_id_mappings = construct_osuked_id_mappings(df_powerdict)
    osuked_id_to_bmu_ids, osuked_id_to_capacity_mw, osuked_id_to_fuel_type, osuked_id_to_name, osuked_id_to_lat_lon = osuked_id_mappings.values()

    df_map = construct_map_df(df_PN, osuked_id_to_bmu_ids, osuked_id_to_capacity_mw, osuked_id_to_lat_lon, osuked_id_to_fuel_type, osuked_id_to_name, n_SPs=n_SPs)
    gdf_map = df_to_gdf(df_map)

    geojson = json.loads(gdf_map.to_json())
    geojson['timeseries'] = [int(unix_datetime) for unix_datetime in list(geojson['features'][0]['properties']['output'].keys())]

    return geojson

# Cell
def save_map_geojson(geojson, fp='data/power_plants.json'):
    with open(fp, 'w') as f:
        json.dump(geojson, f)

# Cell
def get_nearest_dt_idx(geojson, nearest_half_hour):
    ts = pd.to_datetime([x*1000000 for x in geojson['timeseries']]).tz_localize('UTC').tz_convert('Europe/London')
    nearest_hh_match = [i for i, dt in enumerate(ts) if dt==nearest_half_hour]

    if len(nearest_hh_match) == 1:
        return nearest_hh_match[0]
    else:
        return len(ts)-1

def generate_map_js(
    df_PN: pd.DataFrame,
    df_powerdict: pd.DataFrame,
    zoom: int=5,
    center: list=[54.8, -4.61],
    js_template_fp: str='templates/map.js',
    js_docs_fp: str='docs/js/map.js',
    plants_geojson_fp: str='data/power_plants.json',
    plants_geojson_url: str='https://raw.githubusercontent.com/OSUKED/ElexonDataPortal/master/data/power_plants.json',
    routes_geojson_url: str='https://raw.githubusercontent.com/OSUKED/ElexonDataPortal/master/data/network_routes.json'
):
    geojson = construct_map_geojson(df_PN, df_powerdict)
    save_map_geojson(geojson, fp=plants_geojson_fp)

    nearest_half_hour = (pd.Timestamp.now().tz_localize('Europe/London')+pd.Timedelta(minutes=15)).round('30min')
    nearest_dt_idx = get_nearest_dt_idx(geojson, nearest_half_hour)

    rendered_map_js = Template(open(js_template_fp).read()).render(
        zoom=zoom,
        start_idx=nearest_dt_idx,
        center=center,
        plants_geojson_url=plants_geojson_url,
        routes_geojson_url=routes_geojson_url,
    )

    with open(js_docs_fp, 'w', encoding='utf8') as fp:
        fp.write(rendered_map_js)

    return

# Cell
def generate_map_md(md_template_fp='templates/map.md', md_docs_fp='docs/map.md'):
    update_date = pd.Timestamp.now().round('5min').tz_localize('Europe/London').strftime('%Y-%m-%d %H:%M')
    rendered_map_md = Template(open(md_template_fp).read()).render({'update_date': update_date})

    with open(md_docs_fp, 'w', encoding='utf8') as fp:
        fp.write(rendered_map_md)

    return

# Cell
app = typer.Typer()

# Cell
@app.command()
def generate_map(
    api_key: str=None,
    powerdict_url: str='https://raw.githubusercontent.com/OSUKED/Power-Station-Dictionary/main/data/output/power_stations.csv',
    js_template_fp: str='templates/map.js',
    js_docs_fp: str='docs/js/map.js',
    md_template_fp: str='templates/map.md',
    md_docs_fp: str='docs/map.md',
    data_dir: str='data/PN',
    plants_geojson_fp: str='data/power_plants.json',
    plants_geojson_url: str='https://raw.githubusercontent.com/OSUKED/ElexonDataPortal/master/data/power_plants.json',
    routes_geojson_url: str='https://raw.githubusercontent.com/OSUKED/ElexonDataPortal/master/data/network_routes.json'
):
    if api_key is None:
        assert 'BMRS_API_KEY' in os.environ.keys(), 'If the `api_key` is not specified during client initialisation then it must be set to as the environment variable `BMRS_API_KEY`'
        api_key = os.environ['BMRS_API_KEY']

    download_latest_PHYBM_data(api_key, data_dir)
    df_PN = load_most_recent_PN_data(data_dir)

    df_powerdict = pd.read_csv(powerdict_url)

    generate_map_js(df_PN, df_powerdict, js_template_fp=js_template_fp, js_docs_fp=js_docs_fp, plants_geojson_fp=plants_geojson_fp, plants_geojson_url=plants_geojson_url, routes_geojson_url=routes_geojson_url)
    generate_map_md(md_template_fp=md_template_fp, md_docs_fp=md_docs_fp)

    return

# Cell
if __name__ == '__main__' and '__file__' in globals():
    app()