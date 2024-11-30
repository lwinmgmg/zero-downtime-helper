# Zero Downtime Helper
1. Health Checker
2. Nginx Config Patcher

## Health Checker
Health Checker is used to check health of the first instance that is updated image before shutdown all server

#### Environments
REQUEST_URL is the endpoint of the server that we want to do health check
TIMEOUT is duration of health check. It will exit with status 1 if server can't response during TIMEOUT.
Request timeout is 1 sec by default.
SLEEP_TIMEOUT is the duration of each request.
```
REQUEST_URL=https://www.google.com
TIMEOUT=20
SLEEP_TIMEOUT=1
```

#### Script

```
python health_check.py
```

for docker compose
```
docker compose run --rm health_checker python health_check.py
```

## Nginx Config Patcher


#### Environments
DEFAULT_HOSTS is the all server hosts that is used in load balancing.
TEMP_HOSTS is the current available host which are not down yet. Nginx will serve with these hosts.
```
DEFAULT_HOSTS=server:8080,server1:8080
TEMP_HOSTS=server1:8080
```

#### Scripts
Note that you have to use "#####" before after of upstream in nginx config file.
for example:
(app.conf)
```
#####
upstream backend {
    least_conn;
    server server:8080;
    server server1:8080;
}
#####
```

To replace available hosts in Nginx config file.

```
python find_and_replace.py -t replace
```

for docker compose
```
docker compose run --rm health_checker python find_and_replace.py -t replace
```


To restore all hosts in Nginx config file.
```
python find_and_replace.py -t restore
```

for docker compose
```
docker compose run --rm health_checker python find_and_replace.py -t restore
```
