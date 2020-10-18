FROM ubuntu:18.04

VOLUME /golem/work /golem/output /golem/resources

RUN apt-get update 
RUN apt-get install -y john

# a sample passwd passwd file
COPY passwd.txt /golem/hash-bundles/passwd.txt

WORKDIR /golem/work

