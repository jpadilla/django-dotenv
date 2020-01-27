django-dotenv
=============

|build-status-image| |pypi-version|

`foreman <https://github.com/ddollar/foreman>`__ reads from ``.env``.
``manage.py`` doesn't. Let's fix that.

Original implementation was written by
`@jacobian <https://github.com/jacobian>`__.

Tested on Python 3.5, 3.6, 3.7 and 3.8.

Installation
------------

::

    pip install django-dotenv

Usage
-----

Your ``manage.py`` should look like:

.. code:: python

    #!/usr/bin/env python
    import os
    import sys

    import dotenv


    if __name__ == "__main__":
        dotenv.read_dotenv()

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        execute_from_command_line(sys.argv)

You can also pass ``read_dotenv()`` an explicit path to the ``.env``
file, or to the directory where it lives. It's smart, it'll figure it
out.

By default, variables that are already defined in the environment take
precedence over those in your ``.env`` file.  To change this, call
``read_dotenv(override=True)``.

Check out
`tests.py <https://github.com/jpadilla/django-dotenv/blob/master/tests.py>`__
to see all the supported formats that your ``.env`` can have.

Using with WSGI
~~~~~~~~~~~~~~~

If you're running Django with WSGI and want to load a ``.env`` file,
your ``wsgi.py`` would look like this:

.. code:: python

    import os

    import dotenv
    from django.core.wsgi import get_wsgi_application

    dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

    application = get_wsgi_application()

That's it. Now go 12 factor the crap out of something.

Common problems
---------------

``AttributeError: module 'dotenv' has no attribute 'read_dotenv'``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is another similar package,
`python-dotenv <https://github.com/theskumar/python-dotenv>`__, which also
contains a module called ``dotenv``.  If that package is installed, then you
will see:

::

    AttributeError: module 'dotenv' has no attribute 'read_dotenv'

To resolve this, uninstall python-dotenv.

``read_dotenv`` is not reading from my environment file!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, variables that are already defined in the environment take
precedence over those in your ``.env`` file.  To change this, call
``read_dotenv(override=True)``.

.. |build-status-image| image:: https://travis-ci.org/jpadilla/django-dotenv.svg
   :target: https://travis-ci.org/jpadilla/django-dotenv
.. |pypi-version| image:: https://img.shields.io/pypi/v/django-dotenv.svg
   :target: https://pypi.python.org/pypi/django-dotenv
