MiCoNE - Microbial Co-occurrence Network Explorer
=================================================

|Build Status| |Documentation Status| |codecov| |CodeFactor| |Updates|
|Code style: black|

``MiCoNE`` is a Python package for the exploration of the effects of
various possible tools used during the 16S data processing workflow on
the inferred co-occurrence networks. It is also developed as a flexible
and modular pipeline for 16S data analysis, offering parallelized, fast
and reproducible runs executed for different combinations of tools for
each step of the data processing workflow. It incorporates various
popular, publicly available tools as well as custom Python modules and
scripts to facilitate inference of co-occurrence networks from 16S data.

-  Free software: MIT license
-  Documentation: https://micone.readthedocs.io/

Manuscript can be found on
`bioRxiv <https://www.biorxiv.org/content/10.1101/2020.09.23.309781v2>`__
(to be updated with link to publication).

Features
--------

-  Plug and play architecture: allows easy additions and removal of new
   tools
-  Flexible and portable: allows running the pipeline on local machine,
   compute cluster or the cloud with minimal configuration change
   through the usage of `nextflow <www.nextflow.io>`__
-  Parallelization: automatic parallelization both within and across
   samples (needs to be enabled in the ``nextflow.config`` file)
-  Ease of use: available as a minimal ``Python`` library (without the
   pipeline) or as a full ``conda`` package

Know issues
-----------

1. If you have a version of ``julia`` that is preinstalled, make sure
   that it does not conflict with the version downloaded by the
   ``micone-flashweave`` environment
2. The data directory (``nf_micone/data``) needs to be manually
   downloaded (link here).

Credits
-------

This package was created with
`Cookiecutter <https://github.com/audreyr/cookiecutter>`__ and the
`audreyr/cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`__
project template.

.. |Build Status| image:: https://github.com/segrelab/MiCoNE/workflows/build/badge.svg
.. |Documentation Status| image:: https://readthedocs.org/projects/micone/badge/?version=latest
   :target: https://micone.readthedocs.io/en/latest/?badge=latest
.. |codecov| image:: https://codecov.io/gh/segrelab/MiCoNE/branch/master/graph/badge.svg?token=2tKiI0lUJb
   :target: https://codecov.io/gh/segrelab/MiCoNE
.. |CodeFactor| image:: https://www.codefactor.io/repository/github/segrelab/micone/badge
   :target: https://www.codefactor.io/repository/github/segrelab/micone
.. |Updates| image:: https://pyup.io/repos/github/segrelab/MiCoNE/shield.svg
   :target: https://pyup.io/repos/github/segrelab/MiCoNE/
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
