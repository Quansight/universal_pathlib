from upath.universal_path import _FSSpecAccessor, UniversalPath


class _MemoryAccessor(_FSSpecAccessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MemoryPath(UniversalPath):
    _default_accessor = _MemoryAccessor

    def iterdir(self):
        """Iterate over the files in this directory.  Does not yield any
        result for the special paths '.' and '..'.
        """
        if self._closed:
            self._raise_closed()
        for name in self._accessor.listdir(self):
            # fsspec returns dictionaries
            if isinstance(name, dict):
                name = name.get("name")
            if name in {".", ".."}:
                # Yielding a path object for these makes little sense
                continue
            # only want the path name with iterdir
            name = name.rstrip("/")
            name = self._sub_path(name)
            yield self._make_child_relpath(name)
            if self._closed:
                self._raise_closed()
