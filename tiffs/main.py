from pytiff import Tiff
import numpy as np

__all__ = ['Tiffs']


def indices2slices(item):
    if isinstance(item, int):
        if item == -1:
            item = slice(-1, None)
        else:
            item = slice(item, item + 1)
    elif isinstance(item, tuple):
        item = tuple([indices2slices(i) for i in item])
    return item


class Tiffs:
    def __init__(self, *filenames, collate=np.stack, axis=-1, **kwargs):
        """Tiffs.

        Tiffs supports lazy loading from disk.

        Examples:
            >>> with Tiffs('grayscale_slice0.tif', 'grayscale_slice1.tif') as t:
            >>>     crop = t[100:200, 100:201]  # reads only crop region from disk
            >>> print(crop.shape)
            (100, 101, 2)
            >>> with Tiffs('grayscale_slice0.tif', 'grayscale_slice1.tif', collate=np.min) as t:
            >>>     crop = t[100:200, 100:201]  # reads only crop region from disk
            >>> print(crop.shape)
            (100, 101)

        Args:
            *filenames: File names.
            collate: Collate callback. `np.stack` stacks the files. `np.min` takes the minimum of all files per pixel.
            axis: Axis. Only used for `method=np.stack`.
        """
        if len(filenames) == 1 and isinstance(filenames[0], (list, tuple)):
            filenames, = filenames
        self.filenames = filenames
        self.handles = [Tiff(f, 'r', **kwargs) for f in self.filenames]
        self.axis = axis  # axis only used for np.stack
        self.collate = collate
        self.shape = self.handles[0].shape
        self.size = self.handles[0].size
        if isinstance(self.size, tuple):
            self.size = np.multiply.reduce(self.size)

    def __getitem__(self, item):
        assert len(self.handles) > 0
        item = indices2slices(item)
        if ... is item or (isinstance(item, list) and ... in item):
            raise ValueError(f'Ellipsis not allowed for {type(self)} objects.')
        elif isinstance(item, tuple) and len(item) > 2:
            raise ValueError(f'To many dimensions: {item}. Selections only work for y and x axis at this stage.')
        res = [h[item] for h in self.handles]
        if self.collate is not None:
            res = self.collate(res, **{'axis': (self.axis if self.collate == np.stack else 0)})
        return res

    def __enter__(self):
        return self

    def __exit__(self, *a, **k):
        while len(self.handles) > 0:
            self.handles.pop().close()

    def __len__(self):
        return len(self.handles)

    close = __exit__
