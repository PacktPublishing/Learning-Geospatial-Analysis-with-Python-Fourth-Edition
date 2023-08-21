import numpy as np

# Read XYZ file (ignoring the fourth field)
xyz_data = np.loadtxt('bathymetry.xyz', usecols=(0, 1, 2))

# Define grid resolution
resolution = 1.0

# Get min and max coordinates
x_min, y_min = xyz_data[:, 0].min(), xyz_data[:, 1].min()
x_max, y_max = xyz_data[:, 0].max(), xyz_data[:, 1].max()

# Create bins for x and y
x_bins = np.arange(x_min, x_max + resolution, resolution)
y_bins = np.arange(y_min, y_max + resolution, resolution)

# Create a 2D histogram to represent the grid
grid, _, _ = np.histogram2d(xyz_data[:, 1], xyz_data[:, 0], bins=(y_bins, x_bins), weights=xyz_data[:, 2])
count, _, _ = np.histogram2d(xyz_data[:, 1], xyz_data[:, 0], bins=(y_bins, x_bins))

# Divide grid by count, but only where count is not zero
grid[count != 0] /= count[count != 0]

# Replace NaN values and cells where count was zero with NoData value
grid[np.isnan(grid) | (count == 0)] = -9999


# Flip the grid along the Y-axis to correct the orientation
grid = np.flipud(grid)

# Write to ASCIIGrid file
nrows, ncols = grid.shape
header = f"ncols {ncols}\nnrows {nrows}\nxllcorner {x_min}\nyllcorner {y_min}\ncellsize {resolution}\nNODATA_value -9999\n"
with open('bathymetry.asc', 'w') as file:
    file.write(header)
    np.savetxt(file, grid, fmt="%f")

