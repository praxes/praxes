Why Python?
===========

Matlab claims to be "The Language of Technical Computing". It really is a nice
collection of software. I learned how to program using Matlab, in order to
settle a controversy relating to my graduate research project. As it turns out,
I no longer use Matlab. There are two reasons: 1) Matlab is expensive, and once
you begin developing tools using Matlab, you can quickly become committed to a
big, long-term investment and 2) Python is much more pleasant to work with.
The expressiveness, flexibility, and elegance are, in the opinion of many
programmers, the most compelling reasons to use Python.

Scientific computing is currently undergoing something of a Renaissance in the
Python community. It is now possible to create a compelling alternative to
Matlab using NumPy, SciPy, IPython, Matplotlib, and a GUI toolkit like PyQt4.
There are many really high-quality python libraries available, for example,
PyTables manages extremely large datasets by interfacing with the standardized
hdf5 libraries, SymPy provides symbolic manipulation, VTK provides 3D
visualization, and PyMol is a popular molecular visualization system which is
frequently used to render the atomic structure of macro-molecules like proteins.

I think it is important to use and contribute to open source software,
especially in the pursuit of science funded by the public. This speaks more
broadly to the current state of scientific publishing, where the public pays for
grants for scientific research, and then pay again to get access to the results
of that research in an academic publication. I think it is important to maintain
a degree of independence, and to have a sense of familiarity with the tools we
depend upon. And finally, it has been my experience that open-source software
development is an extremely efficient and successful, and results in the
highest quality code. Eric Raymond makes a good case for the open-source
development model in his book "The Cathedral and the Bazaar".

It takes much less time to develop and debug a program in Python than it would
in a compiled language. It is true that some routines in Python are slow
compared to compiled languages like C, but it is also true that once you
understand a few Python idioms you can avoid many performance bottlenecks. Some
cases still arise where you really need to squeeze every ounce of performance
out of your hardware, and in that case you can implement a specific algorithm in
a compiled in something like C and then wrap the resulting library for use from
python. So in response to the question "Why Python?", my initial reaction is
"why would anyone want to use anything else?".
