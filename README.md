# tiffs

```python
from tiffs import Tiffs

# Read from multiple tiff files and stack slices
with Tiffs('grayscale_slice0.tif', 'grayscale_slice1.tif') as t:
  crop = t[100:200, 100:201]  # reads crop region from disk
  # crop.shape: (100, 101, 2)

# Read from multiple tiff files and apply pixelwise minimum
with Tiffs('grayscale_slice0.tif', 'grayscale_slice1.tif', collate=np.min) as t:
  crop = t[100:200, 100:201]  # reads crop region from disk
  # crop.shape: (100, 101)
```
