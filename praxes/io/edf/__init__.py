"""
pychess.edffile is an interface to ESRF Data Format (EDF) files, which are
commonly used in synchrotron labs. Data are loaded into 1, 2, or 3-dimensional
arrays.

Interface:

  load:
      load the data and return an array
  save:
      save the data to disk

Use:

  >>> imageList = load("datafile.edf")
  >>> image0, image4 = load("datafile.edf", 0, 4)
"""

import copy
import exceptions
import os.path
import shutil
import string
import sys
import tempfile
import warnings

import numpy as np

__all__ = ('load', 'save')

def load(filename, *args):
    '''
    Return a list of images contained in `filename`

    filename:
        a string

    Use:

      >>> imageList = load("datafile.edf")
      >>> image0, image1 = load("datafile.edf", 0, 1)

    images are accessed with a Zero-based index
    '''
    edf = EdfFile(filename)
    if args:
        images = [edf.getData(arg) for arg in args]
    else:
        nb_images = edf.getNumImages()
        images = [edf.getData(arg) for arg in xrange(nb_images)]
    return images

def save(filename, array, append=False, header={}):
    '''
    Save an array to `filename`

    filename:
        A string
    array:
        A numpy array containing the data to be saved
    append:
        If False, overwrites the file (overwrites by default)
    header:
        A dictionary to be written in the

    Use:

      >>> save("datafile.edf", data, append=False, header={})
    '''
    edf = EdfFile(filename)
    if not isinstance(header, dict):
        raise TypeError('header must be a python dictionary')
    edf.writeImage(header, args[0], append=append)

#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------

HEADER_BLOCK_SIZE = 1024

STATIC_HEADER_KEYS = {"headerid": "HeaderID",
                      "image": "Image",
                      "byteorder": "ByteOrder",
                      "datatype": "DataType",
                      "dim_1": "Dim_1",
                      "dim_2": "Dim_2",
                      "dim_3": "Dim_3",
                      "offset_1": "Offset_1",
                      "offset_2": "Offset_2",
                      "offset_3": "Offset_3",
                      "size": "Size"}

NUMPY_TYPE_TO_EDF_TYPE = {np.dtype(np.int8): 'SignedByte',
                          np.dtype(np.uint8): 'UnsignedByte',
                          np.dtype(np.int16): 'SignedShort',
                          np.dtype(np.uint16): 'UnsignedShort',
                          np.dtype(np.int32): 'SignedInteger',
                          np.dtype(np.uint32): 'UnsignedInteger',
                          np.dtype(np.int64): 'Signed64',
                          np.dtype(np.uint64): 'Unsigned64',
                          np.dtype(np.float32): 'FloatValue',
                          np.dtype(np.float64): 'DoubleValue'}

EDF_TYPE_TO_NUMPY_TYPE = {'SIGNEDBYTE': np.int8,
                          'UNSIGNEDBYTE': np.uint8,
                          'SIGNEDSHORT': np.int16,
                          'UNSIGNEDSHORT': np.uint16,
                          'SIGNEDINTEGER': np.int32,
                          'UNSIGNEDINTEGER': np.uint32,
                          'SIGNEDLONG': np.int32,
                          'UNSIGNEDLONG': np.uint32,
                          'SIGNED64': np.int64,
                          'UNSIGNED64': np.uint64,
                          'FLOATVALUE': np.float32,
                          'DOUBLEVALUE': np.float64}

if sys.byteorder == 'big': SYS_BYTE_ORDER = "HighByteFirst"
else: SYS_BYTE_ORDER = "LowByteFirst"

#---------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------

def getDefaultEdfType(numpyType):
    """Given a numpy dtype object, return the corresponding edf type"""
    return NUMPY_TYPE_TO_EDF_TYPE[numpyType]

def getDefaultNumpyType(edfType, itemSize=None):
    """Returns NumPy type according Edf type

    ESRF data acquisition is 32bit, so edf longs are 32 bit by convention
    """
    edfType = string.upper(edfType)
    # An unfortunate hack to handle ambiguity with longs:
    if edfType == "SIGNEDLONG" and itemSize == 8: return np.int64
    elif edfType == "UNSIGNEDLONG" and itemSize == 8: return np.uint64
    # Otherwise robust:
    try: return EDF_TYPE_TO_NUMPY_TYPE[edfType]
    except KeyError: raise TypeError, "unknown EdfType %s" % EdfType

def convertDataType(data, newDatatype):
    """ Internal method: array type convertion"""
    try: toNumpyType = getDefaultNumpyType(newDatatype)
    except: toNumpyType = newDataType
    if not data.dtype == toNumpyType: return data.astype(toNumpyType)
    return data

#---------------------------------------------------------------------------
# Exception Handling
#---------------------------------------------------------------------------

class EdfFileError(exceptions.Exception):
    pass


class EdfFormatError(exceptions.Exception):
    pass

#---------------------------------------------------------------------------
# Classes
#---------------------------------------------------------------------------

class Image:

    """
    """

    def __init__(self):
        """ Constructor
        """
        self._header = {}
        self._staticHeader = {}
        self._headerPosition = None
        self._dataPosition = None
        self._itemSize = None

    def getDataPosition(self):
        if self._dataPosition: return self._dataPosition
        else: raise ValueError('Location of data is unknown')

    def setDataPosition(self, pos):
        self._dataPosition = pos

    def getNumDimensions(self):
        return len(self.getShape)

    def getFilePosition(self, pos):
        shape = self.getShape()
        dims = self.getNumDimensions()
        if dims == 1:
            p = pos[0]
        elif dims == 2:
            p = pos[0] + pos[1] * shape[0]
        else:
            p = pos[0] + pos[1] * shape[0] + pos[2] * shape[1] * shape[0]
        return p * self.getItemSize + self.getDataPosition()

    def getHeaderPosition(self):
        if self._headerPosition: return self._headerPosition
        else: raise ValueError('Location of header is unknown')

    def setHeaderPosition(self, pos):
        self._headerPosition = pos

    def getHeader(self):
        return copy.deepcopy(self._header)

    def setHeader(self, key, val):
        self._header[key] = val

    def getHeaderID(self):
        return self._staticHeader.get('HeaderID', None)

    def setHeaderID(self, id):
        self.setStaticHeader('HeaderID', str(id))

    def getImage(self):
        i = self._staticHeader.get('Image', None)
        if i is not None: i = int(i)
        return i

    def setImage(self, index):
        self.setStaticHeader('Image', index)

    def getStaticHeader(self):
        return copy.deepcopy(self._staticHeader)

    def setStaticHeader(self, key, val):
        self._staticHeader[key] = val

    def getItemSize(self):
        if self._itemSize is None:
            self._itemSize = self.getSize()/np.product(self.getShape())
        return self._itemSize

    def setItemSize(self, size):
        self._itemSize = size
        try:
            size = self._itemSize * np.product(self.getShape())
            self.setStaticHeader('Size', size)
        except:
            pass

    def getByteOrder(self):
        try: return self._staticHeader['ByteOrder']
        except KeyError: raise ValueError("ByteOrder not reported")

    def setByteorder(self, byteorder):
        self.setStaticHeader('ByteOrder', byteorder)

    def getEdfDataType(self):
        try: return self._staticHeader['DataType']
        except KeyError: raise ValueError("DataType not reported")

    def setEdfDataType(self, datatype):
        self.setStaticHeader('DataType', datatype)
        self.setItemSize(np.nbytes[getDefaultNumpyType(datatype)])

    def getNumpyDataType(self):
        return getDefaultNumpyType(self.getEdfDataType(), self.getItemSize())

    def setNumpyDataType(self, datatype):
        self.setStaticHeader('DataType', getDefaultEdfType(datatype))
        self.setItemSize(np.nbytes[datatype])

    def getOffsets(self):
        ret = []
        for i in (1, 2, 3):
            try: ret.append(int(self._staticHeader['Offset_%d'%i]))
            except KeyError: break
        if not ret: ret = [0 for i in self.getShape()]
        return ret

    def getShape(self):
        ret = []
        for i in (1, 2, 3):
            try: ret.append(int(self._staticHeader['Dim_%d'%i]))
            except KeyError: break
        if not ret: raise ValueError("Data dimensions not reported")
        if len(ret) > 3:
            raise EdfFormatError("4-dimensional data and higher not supported")
        return ret

    def setShape(self, shape):
        if len(shape) > 3:
            raise ValueError('Dimensions greater than 3 not supported')
        for i, s in enumerate(shape):
            i += 1
            dim = 'Dim_%d'%i
            self._staticHeader[dim] = s
        try:
            size = self.getItemSize * np.product(shape)
            self.setStaticHeader('Size', size)
        except:
            pass

    def getSize(self):
        try: return int(self._staticHeader['Size'])
        except: raise ValueError("Size of data not reported")


class EdfFile:

    """
    """

    def __init__(self, filename):
        """filename: Name of the file (either existing or to be created)"""
        self._images = []
        self._file = None

        if not os.path.isfile(filename):
                self._file = open(filename, "wb")
                self._file.close()
        if os.access(filename, os.W_OK):
            self._file = open(filename, "a+b")
        else :
            self._file = open(filename, "rb")

        f = self._file
        while 1:
            line = f.readline()
            if line.startswith('{'):
                image = Image()
                self._images.append(image)
                image.setHeaderPosition(f.tell())
            elif '=' in line:
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.split(';', 1)[0].strip()
                try:
                    staticKey = STATIC_HEADER_KEYS[key.lower()]
                    image.setStaticHeader(staticKey, val)
                except KeyError:
                    image.setHeader(key, val)
            elif line.endswith("}\n"):
                image.setDataPosition(f.tell())
                # Move to the end of the data block
                try:
                    dataSize = image.getSize()
                    if dataSize > 0:
                        f.seek(dataSize, 1)
                except ValueError:
                    pass
            elif line == "":
                break
            else:
                raise EdfFileError('File format not recognized')

    def GetNumImages(self):
        """See getNumImages"""
        warnings.warn('GetNumImages is deprecated. Use getNumImages.',
                      DeprecationWarning)
        return self.getNumImages()

    def getNumImages(self):
        """ Return the number of images of the object (and associated file)"""
        return len(self._images)

    def GetData(self, Index, DataType="", Pos=None, Size=None):
        """See getData"""
        warnings.warn('GetData is deprecated. Use getData.',
                      DeprecationWarning)
        return self.getData(Index, datatype=DataType, pos=Pos, size=Size)

    def getData(self, index, datatype=None, pos=None, size=None):
        """ return a numpy array containing the image data

            index:
                The zero-based index of the image in the file
            datatype:
                The edf type of the array to be returned. If
                omitted, it uses the type indicated in the image header.
                Relation between Edf types and NumPy's typecodes:

                  - SignedByte      S{->} int8
                  - UnsignedByte    S{->} uint8
                  - SignedShort     S{->} int16
                  - UnsignedShort   S{->} uint16
                  - SignedInteger   S{->} int32
                  - UnsignedInteger S{->} uint32
                  - SignedLong      S{->} int32
                  - UnsignedLong    S{->} uint32
                  - Signed64        S{->} int64
                  - Unsigned64      S{->} uint64
                  - FloatValue      S{->} float32
                  - DoubleValue     S{->} float64

            pos:
                List or tuple (x), (x,y) or (x,y,z) indicating the
                begining of the data to be read. If ommited, set to the origin.
            size:
                List or tuple (x), (x,y) or (x,y,z) indicating the
                size of the data to be read. If ommited, returns data from Pos
                to the end.

            If pos and size are both None, returns the entire block of data.
        """
        im = self._images[index]
        shape = im.getShape()
        dims = len(shape)
        requestedDatatype = datatype
        numpyType = im.getNumpyDataType()
        itemSize = im.getItemSize()

        if pos is None and size is None:
            sizeToRead = np.product(shape)*itemSize
            self._file.seek(im.getDataPosition())
            data = np.fromstring(self._file.read(sizeToRead), numpyType)
            data.shape = shape[::-1]
        else:
            if pos is None: pos = [0 for i in shape]
            if size is None: size = [0 for i in shape]
            if not len(size) == len(pos):
                raise ValueError('size and pos must have the same dimensions')
            def getSize(pos, size, shape):
                if size == 0: size = shape - pos
                return size
            size = [getSize(p, s, sh) for p, s, sh in zip(pos, size, shape)]

            data = np.array([], numpyType)
            sizeToRead = size[0] * itemSize
            if dims == 1:
                self._file.seek(im.getFilePosition(pos))
                data = np.fromstring(self._file.read(sizeToRead),
                                        numpyType)
            elif dims == 2:
                for y in xrange(pos[1], pos[1] + size[1]):
                    self._file.seek(im.getFilePosition([pos[0], y]))
                    line = np.fromstring(self._file.read(sizeToRead),
                                            numpyType)
                    data = np.concatenate((data, line))
                data.shape = size[::-1]
            elif dims == 3:
                data = np.array([], numpyType)
                for z in range(pos[2], pos[2] + size[2]):
                    for y in range(pos[1], pos[1] + size[1]):
                        self._file.seek(im.getFilePosition([pos[0], y, z]))
                        line = np.fromstring(self._file.read(sizeToRead),
                                                numpyType)
                        data = np.concatenate((data, line))
                data.shape = size[::-1]

        if not SYS_BYTE_ORDER.upper() == im.getByteOrder().upper():
            data = data.byteswap()
        if requestedDatatype:
            data = convertDataType(data, requestedDatatype)
        return data

    def GetPixel(self, Index, Position):
        """See getPixel"""
        warnings.warn('GetPixel is deprecated. Use getPixel.',
                      DeprecationWarning)
        return self.getPixel(Index, Position)

    def getPixel(self, index, pos):
        """ Returns double value of the pixel, regardless the format of the
            array

            Index: The zero-based index of the image in the file
            Position: Tuple with the coordinete (x), (x,y) or (x,y,z)
        """
        im = self._images[index]
        itemSize = im.getItemSize()
        numpyType = im.getNumpyDataType()

        self._file.seek(im.getFilePosition(pos))
        data = np.fromstring(self._file.read(itemSize), numpyType)
        if not SYS_BYTE_ORDER.upper() == im.getByteOrder().upper():
            data = data.byteswap()
        return data.astype(np.float64)

    def GetHeader(self, index):
        """See getHeader"""
        warnings.warn('GetHeader is deprecated. Use getHeader.',
                      DeprecationWarning)
        return self.getHeader(index)

    def getHeader(self, index):
        """ Returns a dictionary with image header fields, but not including the
            basic fields (static) defined by data shape, type and file position,
            which are accessed with GetStaticHeader method.

            Index: The zero-based index of the image in the file
        """
        return self._images[index].getHeader()

    def GetStaticHeader(self, index):
        """See getHeader"""
        warnings.warn('GetStaticHeader is deprecated. Use getStaticHeader.',
                      DeprecationWarning)
        return self.getStaticHeader(index)

    def getStaticHeader(self, index):
        """ Returns dictionary with static parameters
            Data format and file position dependent information
            (dim1,dim2,size,datatype,byteorder,headerId,Image)
            Index:          The zero-based index of the image in the file
        """
        return self._images[index].getStaticHeader()

    def WriteImage(self, Header, Data, Append=1, DataType="", ByteOrder=""):
        """See writeImage"""
        warnings.warn('WriteImage is deprecated. Use writeImage.',
                      DeprecationWarning)
        return self.writeImage(Header, Data, append=Append,
                               edfDatatype=DataType, byteorder=ByteOrder)

    def writeImage(self, header, data, append=True, edfDatatype=None,
                   byteorder=None):
        """Save the image to disk.

        header:
            Dictionary containing the non-static header information.
            Static information is generated according to position of image and
            data format
        append:
            If False, overwrites the file. Appends otherwise
        edfDatatype:
            The data type to be saved to the file, defaults to
            current the numpy type:

              - SignedByte      S{->} int8
              - UnsignedByte    S{->} uint8
              - SignedShort     S{->} int16
              - UnsignedShort   S{->} uint16
              - SignedInteger   S{->} int32
              - UnsignedInteger S{->} uint32
              - SignedLong      S{->} int32
              - UnsignedLong    S{->} uint32
              - Signed64        S{->} int64
              - Unsigned64      S{->} uint64
              - FloatValue      S{->} float32
              - DoubleValue     S{->} float64

        byteorder:
            Byte order of the data in file, defaults to the system byteorder:

              - HighByteFirst
              - LowByteFirst
        """
        if not append:
            self._file.truncate(0)
            self._images = []
        im = Image()
        self._images.append(im)
        im.setShape(data.shape[::-1])
        if edfDatatype:
            im.setEdfDataType(edfDatatype)
            data = convertDataType(data, edfDatatype)
        else:
            im.setNumpyDataType(data.dtype)

        itemSize = np.nbytes[data.dtype]

        if byteorder: im.setByteorder(byteorder)
        else: im.setByteorder(SYS_BYTE_ORDER)

        im.setImage(self.getNumImages())
        im.setHeaderID("EH:%06d:000000:000000"%im.getImage())

        self._file.seek(0,2)
        staticHeader = im.getStaticHeader()
        strHeader = "{\n"
        for key in STATIC_HEADER_KEYS.itervalues():
            if key in staticHeader:
                strHeader = strHeader + ("%s = %s ;\n"%(key, staticHeader[key]))
        for key, val in header.iteritems():
            if not key in STATIC_HEADER_ELEMENTS:
                strHeader = strHeader + ("%s = %s ;\n" % (i, val))
                im.setHeader(key, val)
        newSize = ((len(strHeader) + 1) / HEADER_BLOCK_SIZE + 1) * \
                    HEADER_BLOCK_SIZE - 2
        strHeader = strHeader.ljust(newSize)
        strHeader = strHeader+"}\n"

        im.setHeaderPosition = self._file.tell()
        self._file.write(strHeader)
        im.setDataPosition = self._file.tell()
        if not SYS_BYTE_ORDER.upper() == im.getByteOrder().upper():
            self._file.write((data.byteswap()).tostring())
        else:
            self._file.write(data.tostring())




if __name__ == "__main__":
    from numpy import arange
    a = arange(50).reshape(5, 10)
    save('temp.edf', a)
    b = load('temp.edf')[0]
    save('temp.edf', b, append=True)
    c, d = load('temp.edf')
    for i in range(5):
        print a[i]
        print b[i]
        print c[i]
        print d[i]
        print '\n'
