import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pytz
import ntpath
import warnings
import os
import logging

import tempfile
#suppress deprecation warnings
warnings.simplefilter("ignore", category=DeprecationWarning)

radar_root = tempfile.TemporaryDirectory

ntpath.basename(str(cwd))
dataDir = os.path.join(cwd, "/Data")



def display(images):
    ims = []
    fig = plt.figure()
    #ax = fig.add_subplot(111)
    for i, scan in enumerate(results.iter_success(), start=1):
        head, tail = ntpath.split(str(scan))
        tail = tail[:-1]
        print("Loading ", tail, " scan now...")
        radar = pyart.io.read_nexrad_archive(str(tail))
        # mask out last 10 gates of each ray, this removes the "ring" around the radar.
        radar.fields['reflectivity']['data'][:, -10:] = np.ma.masked
    
        # exclude masked gates from the gridding
        gatefilter = pyart.filters.GateFilter(radar)
        gatefilter.exclude_transition()
        gatefilter.exclude_masked('reflectivity')
    
        # perform Cartesian mapping, limit to the reflectivity field.
        grid = pyart.map.grid_from_radars(
            (radar,), gatefilters=(gatefilter, ),
            grid_shape=(1, 241, 241),
            grid_limits=((2000, 2000), (-123000.0, 123000.0), (-123000.0, 123000.0)),
            fields=['reflectivity'])
        pass
    
    central_timezone = pytz.timezone('US/Central')

    plot.imsave('/tmp/radar')
    plt.show()



# "Load and display"


#     im = ax.imshow(grid.fields['reflectivity']['data'][0], origin='lower', animated=True)
#     ims.append([im])

# ani = animation.ArtistAnimation(fig, ims, interval=50, blit=False,
#                             repeat_delay=1000, repeat=True)
# ani.save('Feb14snow.gif')

