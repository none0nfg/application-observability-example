from python:3.10
workdir /app
copy requirements.txt /app
run pip3 install -r requirements.txt
copy main.py /app
#cmd ["/usr/local/bin/python3", "main.py"]
cmd ["opentelemetry-instrument", "flask", "--app", "main.py", "run", "-h", "0.0.0.0", "-p", "5000"]