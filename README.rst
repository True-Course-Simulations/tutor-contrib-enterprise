enterprise plugin for `Tutor <https://docs.tutor.overhang.io>`__
================================================================

Original plugin by Dicey-Tech. Updated and maintained by Cannon Smith for Tutor v16+ compatibility.

This lightweight plugin exposes the LMS Enterprise Django apps in Tutor-based Open edX deployments.
It turns on the enterprise feature flag, configures default settings/URLs, and creates a dedicated
Enterprise service user during ``tutor init`` so the integration is ready immediately after install.

Installation
------------

Install from source:

.. code-block:: bash

    pip install git+https://github.com/Dicey-Tech/tutor-contrib-enterprise

Then enable the plugin:

.. code-block:: bash

    tutor plugins enable enterprise

Usage
-----

Regenerate your Tutor config/environment with the plugin enabled:

.. code-block:: bash

    tutor config save --extra-plugin enterprise
    tutor local quickstart  # or `tutor dev start` in dev mode

Key settings (override in ``config.yml`` or via ``TUTOR_`` env vars):

- ``ENTERPRISE_USER``: username for the service account that is created in the LMS (default: ``enterprise``).

The LMS init hook ensures the user exists, has a matching ``@openedx`` email, and is both staff and superuser.
Enterprise API URLs are automatically derived from your deployment hostnames for both development and production modes.

License
-------

This software is licensed under the terms of the AGPLv3.
