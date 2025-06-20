import cartopy.io.shapereader as shpreader

datasets = [
    ('50m', 'physical', 'coastline'),
    ('50m', 'physical', 'land'),
    ('50m', 'cultural', 'admin_0_countries'),
    ('50m', 'cultural', 'admin_0_boundary_lines_land'),
    ('50m', 'physical', 'rivers_lake_centerlines'),
    ('50m', 'physical', 'lakes'),
    ('10m', 'physical', 'coastline'),
    ('10m', 'physical', 'land'),
    ('10m', 'cultural', 'admin_0_countries'),
    ('10m', 'cultural', 'admin_0_boundary_lines_land'),
    ('10m', 'physical', 'rivers_lake_centerlines'),
    ('10m', 'physical', 'lakes'),
]

for resolution, category, name in datasets:
    print(f"Downloading {category} {name} at {resolution} resolution...")
    shpreader.natural_earth(resolution=resolution, category=category, name=name)
print("All downloads complete!")
