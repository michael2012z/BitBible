FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y subversion build-essential autotools-dev pkg-config libz-dev libclucene-dev libicu-dev libcurl4-gnutls-dev libtool m4 automake subversion
RUN cd /root && svn co https://crosswire.org/svn/sword/trunk --trust-server-cert-failures=unknown-ca --non-interactive && mv trunk sword
RUN cd /root/sword && ./autogen.sh && ./usrinst.sh --enable-shared --enable-examples && make && make install && make install_config
