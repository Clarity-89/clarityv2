
Project layout
==============

The project layout was made in such a way that code is seperated from non-code
files that you typically want to serve in another way (static and media files)
or keep in a different location (like the virtual environment)::

    clarityv2
    |
    +-- bin                 -- Useful scripts (mostly for developers).
    |
    +-- build               -- All Gulp tasks.
    |
    +-- doc                 -- Documentation source and generated files.
    |
    +-- env                 -- Virtual environment files.
    |
    +-- log                 -- All log files are stored here.
    |
    +-- media               -- Default location for uploaded media files.
    |
    +-- requirements        -- Project requirements for each type of installation.
    |
    +-- src                 -- Container for one or more source directories.
    |   |
    |   +-- clarityv2
    |       |
    |       +-- conf        -- Django settings files.
    |       |
    |       +-- js          -- JavaScript source files.
    |       |
    |       +-- sass        -- Sass (css pre-processor) source files.
    |       |
    |       +-- static      -- Default location for project static files.
    |       |
    |       +-- templates   -- Project templates.
    |       |
    |       +-- test        -- Automated tests.
    |       |
    |       +-- utils       -- Project-wide utility functions.
    |       |
    |       +-- ...         -- Project specific applications.
    |
    +-- static              -- Default location for collected static files.
