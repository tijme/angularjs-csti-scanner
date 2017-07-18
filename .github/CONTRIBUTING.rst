Contributing
============

Getting Started
---------------

-  Submit a ticket for your issue, assuming one does not already exist.

   -  Clearly describe the issue including steps to reproduce when it is
      a bug.
   -  Make sure you fill in the earliest version that you know has the
      issue.

-  Fork the repository on GitHub.

Making Changes
--------------

-  Create a topic branch from where you want to base your work.

   -  This is usually the develop branch.
   -  To quickly create a topic branch based on master;

      -  ``git checkout -b bugfix_my_contribution``,
      -  ``git checkout -b feature_my_contribution``.

   -  Please avoid working directly on the ``master`` branch.

-  Make sure your code complies with the `Google Python Style Guide`_.
-  Make commits of logical units and make sure your commit messages are
   in the proper format.
-  Make sure you have added the necessary tests for your changes.
-  Run *all* the tests to assure nothing else was accidentally broken.

Submitting Changes
------------------

-  Push your changes to the topic branch in your fork of the repository.
-  Submit a pull request to the main repository
   (``tijme/detective``).

.. _Google Python Style Guide: https://google.github.io/styleguide/pyguide.html