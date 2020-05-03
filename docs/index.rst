.. heliPypter documentation master file, created by
   sphinx-quickstart on Tue Apr 28 21:02:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to heliPypter's documentation!
======================================

.. image:: https://raw.githubusercontent.com/czarified/helipypter/master/docs/img/banner.png
  :width: 100 %
  :alt: heliPypter
  :align: left

heliPypter is a package for rotorcraft performance evaluation. Rotorcraft attributes are provided as input,
and performance characteristics such as Engine Horsepower, Specific Range, and Fuel consumption are evaluated.

heliPypter has an object oriented philosophy, so different rotorcraft configurations can be built, modified,
and evaluated quickly, with the same methods. The classes have methods for Hover in and out of Ground Effect
(HOGE and HIGE), as well as forward flight.

Under the hood, briefly speaking, the code applies Momentum Theory assuming constant chord ideal twist. 
For forward flight, Glauert's Model is used.


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   analysis
   theory
   api
   license


Attributions
^^^^^^^^^^^^

Huey Graphic by Jetijones - Own work, CC BY 3.0, https://commons.wikimedia.org/w/index.php?curid=15743299
Blade Element graphic by Smilesgiles89 - MS Paint, CC BY-SA 3.0, https://en.wikipedia.org/w/index.php?curid=38336902


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
