Example code
------------

Use modules from default datapath
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from pysword.modules import SwordModules
    # Find available modules/bibles in standard data path.
    # For non-standard data path, pass it as an argument to the SwordModules constructor.
    modules = SwordModules()
    # In this case we'll assume the modules found is something like:
    # {'KJV': {'description': 'KingJamesVersion(1769)withStrongsNumbersandMorphology', 'encoding': 'UTF-8', ...}}
    found_modules = modules.parse_modules()
    bible = modules.get_bible_from_module(u'KJV')
    # Get John chapter 3 verse 16
    output = bible.get(books=[u'john'], chapters=[3], verses=[16])

Load module from zip-file
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from pysword.modules import SwordModules
    # Load module in zip
    # NB: the zip content is only available as long as the SwordModules object exists
    modules = SwordModules(u'KJV.zip')
    # In this case the module found is:
    # {'KJV': {'description': 'KingJamesVersion(1769)withStrongsNumbersandMorphology', 'encoding': 'UTF-8', ...}}
    found_modules = modules.parse_modules()
    bible = modules.get_bible_from_module(u'KJV')
    # Get John chapter 3 verse 16
    output = bible.get(books=[u'john'], chapters=[3], verses=[16])

Manually create bible
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from pysword.bible import SwordBible
    # Create the bible. The arguments are:
    # SwordBible(<module path>, <module type>, <versification>, <encoding>, <text formatting>)
    # Only the first is required, the rest have default values which should work in most cases.
    bible = SwordBible(u'/home/me/.sword/modules/texts/ztext/kjv/', u'ztext', u'kjv', u'utf8', u'OSIS')
    # Get John chapter 3 verse 16
    output = bible.get(books=[u'john'], chapters=[3], verses=[16])
