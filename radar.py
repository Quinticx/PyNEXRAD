import nexradaws
import tempfile
import logging
import numpy as np


import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


from datetime import date
from metpy.io import Level2File
from metpy.plots import add_timestamp, colortables
from metpy.plots import USCOUNTIES
from matplotlib.colors import Normalize

logging.basicConfig(level=logging.INFO)

#radar_root = tempfile.TemporaryDirectory()
radar_root = '/tmp'

# Download scans that are not MDM
def download(site):
    today = date.today()
    logging.info("Downloading radar for {} on {}".format(site, today))

    conn = nexradaws.NexradAwsInterface()
    availscans = conn.get_avail_scans(today.year, today.month, today.day, site)

    suffix = "MDM"
    scans = [x for x in availscans if (not x.filename.endswith(suffix))][-5:]

    if scans:
        result = conn.download(scans, radar_root)
        return result.success

    return []

def plot(scan):
    filename = "{}/{}".format(radar_root, scan.filename)
    
    logging.info("Opening scan {}".format(filename))
    f = Level2File(filename)

    logging.info("Done")

    # lon=-90.6828
    # lat=38.6986

    lat = f.sweeps[0][0][1].lat
    lon = f.sweeps[0][0][1].lon

    # Pull data out of the file
    sweep = 0
    
    # First item in ray is header, which has azimuth angle
    az = np.array([ray[0].az_angle for ray in f.sweeps[sweep]])
    
    # 5th item is a dict mapping a var name (byte string) to a tuple
    # of (header, data array)
    ref_hdr = f.sweeps[sweep][0][4][b'REF'][0]
    ref_range = np.arange(ref_hdr.num_gates) * ref_hdr.gate_width + ref_hdr.first_gate
    ref = np.array([ray[4][b'REF'][1] for ray in f.sweeps[sweep]])

    proj = ccrs.LambertConformal(central_longitude=lon, central_latitude=lat)

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(projection=proj)
    
    # Turn into an array, then mask
    data = np.ma.array(ref)
    data[np.isnan(data)] = np.ma.masked

    logging.info("Finished MetPY")

    # Convert az,range to x,y
    xlocs = (ref_range/111)  * np.sin(np.deg2rad(az[:, np.newaxis])) + lon
    ylocs = (ref_range/111) * np.cos(np.deg2rad(az[:, np.newaxis])) + lat

    ax.set_extent([lon - 3.5, lon + 3.5, lat - 3.5, lat + 3.5], ccrs.Geodetic())
    ax.add_feature(USCOUNTIES.with_scale('500k'))

    # Plot the data
    # $ax.plot(lat, lon, "or", transform=proj)
    # ax.plot(0, 0, "bo",transform=ccrs.Geodetic())
    # ax.plot(1, 1, "go",transform=ccrs.Geodetic())

    ax.plot(0, 0, "or",transform=proj)
    ax.text(0, 0, f.stid.decode("ascii").upper(),transform=proj)
    cmap = colortables.get_colortable('NWSReflectivity')
    ax.pcolormesh(xlocs, ylocs, data, norm=Normalize(-25, 75), cmap=cmap, transform=ccrs.PlateCarree())


    ax.set_aspect('equal', 'datalim')

    plt.savefig('radar.png')
    return 'radar.png'