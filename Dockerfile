FROM dockerfile/elasticsearch

ADD elasticsearch.yml /data/elasticsearch.yml

EXPOSE 9200
EXPOSE 9300

VOLUME ["/data"]

CMD ["/elasticsearch/bin/elasticsearch", "-Des.config=/data/elasticsearch.yml"]
