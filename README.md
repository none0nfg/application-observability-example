# Observability Stack

* Simple python application, with prometheus exporter and opentelemetry tracer.
* Graylog, Mongo, Elasticsearch, Docker-Compose Gelf log exporter
* Prometheus, Grafana metrics scrape and visualize
* Otel-collector, Jaeger-collector, jaeger-query to get and show traces. ***SPM is enabled***

## How to use

1. Pull repository
2. ```docker compose build```
3. ```docker compose up -d```, Try to run this command few times till each dependency start

application is `app`, `app2` in docker-compose. 
Application routes:
* /500 - return 500 error
* /404 - return 404 error
* / - return 200 code
* /proxy?url="<URL>" - make a request to <URL>

You can get any endpoint of application to produce metrics and logs and traces.

Use this command to generate trace with 2 spans

* ```curl localhost:5000/proxy?url=http://app2:5000/404```
