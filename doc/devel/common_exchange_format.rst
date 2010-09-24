Common Exchange Format
======================

Some interested parties have been discussing the development of a common
exchange format. What follows is a discussion of the format I developed for
use at CHESS, and some of the considerations that lead to its current design.


Data Organization
-----------------

How to organize the various data that are collected at synchrotron beamlines?

There seems to be general agreement that hdf5 is a good foundation on which
to build a common data format for synchrotron experiments.

One proposal has been to pack all the motor positions, counters, etc., into
a single array. If there are 10 such datasets and a scan is 100 points long,
such an array would have 100 rows and 10 columns. I do not favor this
approach, because it is difficult to convey context. How do we communicate
what names are associated with each column? What about quantum efficiencies
for counters, units for positioners? What about non-scalar data, like images,
and multichannel analyzers? And what about the scalar data associated with
such multidimensional datasets, like dead time?

For this reason, I prefer to make more extensive use of hdf5 groups and
datasets. For simple datasets, like a positioner or a counter, a simple
hdf5 dataset can be used, with additional metadata communicated by the
hdf5 attributes associated with the dataset. For example, using h5py::

   my_group['motor1'] = [0, .5, 1]
   my_group['motor1'].attrs['units'] = 'mm'

   my_group['monitor'] = [1, 1, 1]
   my_group['monitor'].attrs['efficiency'] = 1e-5

For complex datasets, like an energy-dispersive detector, several datasets
usually need to be grouped together in order to provide all the information
required to interpret the data::

   mca_group = my_group.create_dataset('vortex')
   mca_group['counts'] = numpy.zeros(3, 1024)
   mca_group['dead_time'] = [0, 0, 0]
   mca_group['dead_time'].attrs['format'] = 'fraction'
   mca_group['bins'] = numpy.arange(1024)


Data Structure
--------------

How should the datasets be shaped? Some scans are linear, some are
regularly-gridded area scans, some may be more complex, like spiral
tomography. What all scans have in common, however, is that data are acquired
as a stream of points, one after another as time progresses.

For this reason, I have opted for the outer dimension of all datasets to
have the same length as the number of points in the scan. Scalar data from a
linear scan with 100 points will have shape (100,). Vector data, like MCA
counts with 1024 bins, would have shape (100, 1024). Both of these datasets
would have the exact same shape for an area scan with 10 points in each
direction.

An additional benefit is that it simplifies data processing. The same routines
can be used to iterate over scans of any shape.

How the data is interpreted or visualized is up to the application. Simple
area scans can simply reshape the array. For the case of spiral CT, the
application will obviously have to do some work in order to visualize the
data, but what alternative is there for how to store the data in the file?

Context
-------

In order for applications to interpret, analyze, and visualize the data, some
additional context needs to be provided. How to differentiate a 100-point
linear scan from a 10-by-10 area scan? The top-level group for the scan can
contain an attribute like 'acquisition_shape' that communicates this context.

At CHESS, we still use Spec for data acquisition, which allows
arbitrarily-named motors, counters, etc. Scans can be arbitrarily-structured
as well, in the sense that any motor can be scanned. Scans often require
compound motions. The way I have provided this information is to provide
two attributes: "axis" and "primary". The "axis" attribute specifies the order
of the axes: a value of 1 indicates it is the fastest-moving direction, 2
indicates it is the second-fastest-moving direction. The "primary" attribute
communicates the ordering of axes in a scan involving compound motions.

Some datasets contain attributes that are specific to axes (or positioners),
and others contain attributes that are specific to signals. Groups and
datasets therefore have an attribute to communicate what kind of data they
are.

This 
