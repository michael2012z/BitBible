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
