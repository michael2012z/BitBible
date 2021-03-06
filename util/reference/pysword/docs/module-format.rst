Module formats
--------------

I'll use Python's struct module's format strings to describe byte
formatting. See https://docs.python.org/3/library/struct.html

There are current 4 formats for bible modules in SWORD.

ztext format documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Take the Old Testament (OT) for example. Three files:

-  ot.bzv: Maps verses to character ranges in compressed buffers. 10
   bytes ('<IIH') for each verse in the Bible:

   -  buffer\_num (I): which compressed buffer the verse is located in
   -  verse\_start (I): the location in the uncompressed buffer where
      the verse begins
   -  verse\_len (H): length of the verse, in uncompressed characters

These 10-byte records are densely packed, indexed by VerseKey 'Indicies'
(docs later). So the record for the verse with index x starts at byte
10\*x.

-  ot.bzs: Tells where the compressed buffers start and end. 12 bytes
   ('<III') for each compressed buffer:

   -  offset (I): where the compressed buffer starts in the file
   -  size (I): the length of the compressed data, in bytes
   -  uc\_size (I): the length of the uncompressed data, in bytes
      (unused)

These 12-byte records are densely packed, indexed by buffer\_num (see
previous). So the record for compressed buffer buffer\_num starts at
byte 12\*buffer\_num.

-  ot.bzz: Contains the compressed text. Read 'size' bytes starting at
   'offset'.

ztext4 format documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

ztext4 is the same as ztext, except that in the bzv-file the verse\_len
is now represented by 4-byte integer (I), making the record 12 bytes in
all.

rawtext format documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Again OT example. Two files:

-  ot.vss: Maps verses to character ranges in text file. 6 bytes ('<IH')
   for each verse in the Bible:

   -  verse\_start (I): the location in the textfile where the verse
      begins
   -  verse\_len (H): length of the verse, in characters

-  ot: Contains the text. Read 'verse\_len' characters starting at
   'verse\_start'.

rawtext4 format documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

rawtext4 is the same as rawtext, except that in the vss-file the
verse\_len is now represented by 4-byte integer (I), making the record 8
bytes in all.
