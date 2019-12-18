FROM alpine:3.7

WORKDIR /home/tmp

RUN apk add autoconf automake make g++ git \
			libtool curl-dev c-ares-dev zlib-dev sqlite-dev libsodium-dev swig \
			py-pip python-dev &&\
	apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
			crypto++-dev \
			libressl libressl-dev &&\
	apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/community \
			freeimage-dev &&\
	pip install --upgrade pip && pip install wheel &&\
	pip install --upgrade google-api-python-client google-auth-oauthlib 
	
RUN git clone https://github.com/meganz/sdk.git &&\
	cd sdk && sh autogen.sh &&\
	./configure --disable-silent-rules --enable-python --disable-examples &&\
	make && make install

RUN cd sdk/bindings/python && python setup.py bdist_wheel &&\
	pip install dist/megasdk-3.6.3-py2.py3-none-any.whl
