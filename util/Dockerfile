FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -qy curl wget git build-essential autotools-dev pkg-config libz-dev libclucene-dev libicu-dev libcurl4-gnutls-dev libtool m4 automake subversion
RUN apt-get install -qy emacs cscope xcscope-el
RUN apt-get install -qy python3
RUN apt-get install -qy python3-pip tree

RUN cd /root && svn co https://crosswire.org/svn/sword/trunk --trust-server-cert-failures=unknown-ca --non-interactive && mv trunk sword
RUN cd /root/sword && ./autogen.sh && ./usrinst.sh --enable-shared --enable-examples && make && make install && make install_config

RUN cd /root && git clone https://gitlab.com/tgc-dk/pysword.git
RUN pip3 install pysword
