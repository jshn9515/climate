#!/usr/bin/env python

# Metpy Monday
# 62 - Scripting Part 3
# https://www.youtube.com/watch?v=M_SPw8TasPk

import argparse
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from siphon.simplewebservice.ndbc import NDBC

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make a plot of buoy data.')
    parser.add_argument('--cmap', default='Oranges', help='mpl color map')
    parser.add_argument('--var', default='water_temperature', help='variable to plot')
    parser.add_argument('--savefig', action='store_true', help='save a figure instead of displaying')
    parser.add_argument('--imgformat', default='png', help='saved image format')
    parser.add_argument('--min', default=None, type=int, help='Minimum color bar bound.')
    parser.add_argument('--max', default=None, type=int, help='Maximum color bar bound.')
    parser.add_argument('--msize', default=5, type=int, help='Marker size')
    args = parser.parse_args()

    print('Downloading data...')
    df = NDBC.latest_observations()
    print(f'Complete. {len(df)} stations')
    # Drop any rows with NaN for the data we want
    df.dropna(subset=[args.var], inplace=True)
    print(f'{len(df)} stations with variable {args.var}\nPlotting...')
    # Make an LCC map projection
    proj = ccrs.LambertConformal()

    # Plot the map
    fig = plt.figure(1)
    ax = fig.add_subplot(projection=proj)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
    ax.add_feature(cfeature.OCEAN.with_scale('50m'))
    ax.add_feature(cfeature.LAND.with_scale('50m'))
    ax.add_feature(cfeature.BORDERS.with_scale('50m'), linestyle=':')
    ax.add_feature(cfeature.STATES.with_scale('50m'), linestyle=':')
    ax.add_feature(cfeature.LAKES.with_scale('50m'), alpha=0.5)
    ax.add_feature(cfeature.RIVERS.with_scale('50m'), alpha=0.5)

    scatter = ax.scatter(df.longitude, df.latitude,
                         c=df[args.var], transform=ccrs.PlateCarree(),
                         cmap=plt.get_cmap(args.cmap), vmin=args.min, vmax=args.max,
                         s=args.msize)  # cm.Oranges or Use plt.get_cmap(str)

    plt.colorbar(scatter, orientation='horizontal',
                 label=args.var.replace('_', ' ').title(),
                 shrink=0.6, pad=0.05)

    # Save or show figures
    if args.savefig:
        plt.savefig(f'buoys_{datetime.datetime.utcnow():%Y%m%d_%H%MZ}.{args.imgformat}')
    else:
        plt.show()
