# Setting up Elastic Search in Docker

1. Turn on docker
2. Pull image of ElasticSearch `docker pull docker.elastic.co/elasticsearch/elasticsearch:7.10.`
3. Run ElasticSearch on docker: `docker run -d --name elasticsearch -p 9200:9200 \
  -e "discovery.type=single-node" \
  docker.elastic.co/elasticsearch/elasticsearch:7.10.1
`
1. Test if ElasticSearch is running: `curl http://localhost:9200`