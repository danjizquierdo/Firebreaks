import geopandas as gpd
import geoplot as gplt
import pandas as pd
import matplotlib.pyplot as plt
from geopandas.tools import sjoin
import json
import os
import warnings
warnings.filterwarnings("ignore")
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


def get_country(name):
    return world[world.name == name.title()]

def process_gis(fn):
    with open(fn) as f:
        points = json.loads(f.read())
    # Process date information
    df['date'] = pd.to_datetime(df['acq_date'] + ':' + df['acq_time'], format='%Y-%m-%d:%H%M', utc=True)
    df = df.set_index('date')
    df['month'] = df.index.month
    df['year'] = df.index.year
    df.confidence = df.confidence.apply(int)
    df.brightness = df.brightness.apply(lambda x: x - 273.15)
    gdf = gpd.GeoDataFrame(df[df['confidence']>90],
                           geometry=gpd.points_from_xy(df.longitude, df.latitude))

def filter_country(c_df, g_df):
    return sjoin(g_df, c_df, how='left')

def get_brightness_scale(df):
    IQR = df.brightness.quantile(.75) - df.brightness.quantile(.25)
    top = min(df.brightness.quantile(.75) + 1.5*IQR, df.brightness.max())
    bot = max(df.brightness.quantile(.25) - 1.5*IQR, df.brightness.min())
    return [bot, top]

def plot_years(first_year, last_year, plot_gdf, country='Australia', output_path = 'charts/maps'):

    list_of_years = range(first_year, last_year+1)
    list_of_months = range(1, 13)
    months = {1: 'Jan ', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
              6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
              11: 'Nov', 12: 'Dec'}
    vmin, vmax = get_brightness_scale(plot_gdf)
    extent = get_country(country).total_bounds
    data = []

    # start the for loop to create one map per year
    for year in list_of_years:
        for month in list_of_months:
            annual = plot_gdf.query(f'year=={year}')
            datum = annual.query(f'month=={month}')
            if isinstance(data, list):
                data = datum
            else:
                data = pd.concat([data, datum])
            if len(datum) != 0:
                # create map, UDPATE: added plt.Normalize to keep the legend range the same for all maps
                ax = aus.plot(color='darkgreen', edgecolor='black')
                gplt.kdeplot(data, ax=ax, clip=aus, cmap='inferno_r', opacity=.2, shade=True, shade_lowest=False)
                fig = gplt.pointplot(datum, ax=ax, cmap='Reds', hue='brightness', figsize=(10, 10),
                                     linewidth=0.8, edgecolor='black', legend=True, vmin=vmin, vmax=vmax,
                                     norm=plt.Normalize(vmin=vmin, vmax=vmax), extent=extent)

                # remove axis of chart
                fig.axis('off')

                # add a title
                fig.set_title(f'Fires in {country}', \
                              fontdict={'fontsize': '25',
                                        'fontweight': '5'})

                fig.annotate(str(year) + ': ' + months[month],
                             xy=(0.1, .225), xycoords='figure fraction',
                             horizontalalignment='left', verticalalignment='top',
                             fontsize=18, fontweight=3)

                # this will save the figure as a high-res png in the output path. you can also save as svg if you prefer.
                filepath = os.path.join(output_path, str(year) + str(month) + '_fire.png')
                chart = fig.get_figure()
                plt.show()
                chart.savefig(filepath, dpi=200)