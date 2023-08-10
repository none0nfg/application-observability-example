#!/usr/bin/python3
import logging
from os import getenv

import requests as re
from flask import Flask, request
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_flask_exporter import PrometheusMetrics

JAEGER_HOST = getenv("JAEGER_HOST", "172.18.11.243:6831")
TRACING_SERVICE = getenv("TRACING_SERVICE", "app")

log_level = logging.DEBUG
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)

app = Flask(__name__)

resource = Resource(attributes={
    SERVICE_NAME: TRACING_SERVICE
})

# provider = TracerProvider(resource=resource)
# processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=JAEGER_HOST))
# provider.add_span_processor(processor)
# trace.set_tracer_provider(provider)

metrics = PrometheusMetrics(app, path="/metrics", export_defaults=True)
metrics.info('app_info', 'Application info', version='1.0.3')


@app.route("/")
def root():
    logging.info("Someone got /")
    return f"Hello world !"


@app.route("/500")
def error():
    params = request.args
    logging.error(f"FATAL ERROR: {params.to_dict()}")
    return "ERROR!", 500


@app.route("/404")
def not_found():
    params = request.args
    logging.warning(f"NOT FOUND: {params.to_dict()}")
    return "ERROR!", 404


@app.route("/proxy")
def proxy():
    url = request.args.get("url")
    tracer = trace.get_tracer("my.tracer")
    with tracer.start_as_current_span("print") as span:
        print("foo")
        span.set_attribute("printed_string", "foo")
    if not url:
        return "ERROR", 400
    resp = re.get(url)
    return resp.content, resp.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0")
