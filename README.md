# SearchKicks [To be renamed]
## How to use

### Toolbox use

In a script or python interpreter, you have access to some generic tools
(load, save files) in the module `search_kicks.tools`, and to the core functions
in `search_kicks.core`.

## Dependencies

### Packaged
* python2.7 or above, or python3
* numpy
* scipy

### From source
* pyepics
* PyML

#### pyepics
```
$ wget http://pypi.python.org/packages/source/p/pyepics/pyepics-3.2.4.tar.gz
$ tar xzvf pyepics-3.2.4.tar.gz
$ cd pyepics-3.2.4
$ python setup.py build
```

To install locally (but in Python path)
```
$ python setup.py install --user 
```

To install system-wide:

```
$ sudo python setup.py install
```
#### PyML
```
$git clone aragon.acc.bessy.de:/opt/repositories/controls/git/tools/PyML.git
```

TODO: validate `setup.py`
Follow same procedure as above.
