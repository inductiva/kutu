import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Create a dummy plot with all common features to force download
fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())

# List of common features to download
features = [
    cfeature.COASTLINE,
    cfeature.BORDERS,
    cfeature.LAKES,
    cfeature.RIVERS,
    cfeature.STATES
]

for feat in features:
    ax.add_feature(feat)

# Save a dummy plot to trigger downloads
plt.savefig("/tmp/cartopy_cache_dummy.png")
