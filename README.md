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

### ncurses
#### Some tutorials to learn
1. https://www.youtube.com/watch?v=pjT5wq11ZSE&list=PL2U2TQ__OrQ8jTf0_noNKtHMuYlyxQl4v
1. https://www.gnu.org/software/ncurses/ncurses-intro.html
1. http://www.cs.ukzn.ac.za/~hughm/os/notes/ncurses.html
