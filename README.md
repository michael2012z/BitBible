# BitBible
Collection of my Holy Bible text and tools

## Sword
### Test in sandbox
You can choose to build and test sword in a Docker container. 

I created a Dockerfile in which all the necessary software in dependency are ready.

Follow commands shown below to use it:

* \> cd sword/
* \> docker build -t sword .
* \> docker run -it --volume $(pwd):/sword sword bash

If everything goes well, now you are in a container. Following commands are done in it.

* \> cd /sword
* \> ./autogen.sh 
* \> ./usrinst.sh --enable-shared --enable-examples 
* \> make 
* \> make install 
* \> make install_config

## How will BitBible grow (roadmap)
![](https://raw.githubusercontent.com/michael2012z/BitBible/master/img/BitBible_growth.png)

## Reference
#### OSIS
- http://www.crosswire.org/osis/schemas/osisCore.2.1.1.xsd.html
- http://www.crosswire.org/osis/tutor.jsp
- https://wiki.crosswire.org/OSIS_Tutorial
- https://wiki.crosswire.org/OSIS_Bibles
- https://wiki.crosswire.org/Official_and_Affiliated_Module_Repositories
- http://openscriptures.org/
- https://github.com/openscriptures
#### ncurses
- https://www.youtube.com/watch?v=pjT5wq11ZSE&list=PL2U2TQ__OrQ8jTf0_noNKtHMuYlyxQl4v
- https://www.gnu.org/software/ncurses/ncurses-intro.html
- http://www.cs.ukzn.ac.za/~hughm/os/notes/ncurses.html
