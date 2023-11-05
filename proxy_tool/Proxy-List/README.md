# Proxy_List

`Proxy_list` Implement the retrieval of free proxy IP addresses through a network channel by providing proxy addresses. Perform initial filtering by validating the proxies, and then conduct a second round of screening before using them. The goal is to obtain stable and reliable proxy IP addresses along with their corresponding ports.



# Sources

| Source                                                       | Succeed |
| ------------------------------------------------------------ | ------- |
| [proxyscrape.com](https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all) | ✅       |
| [proxyscan.io](https://www.proxyscan.io)                     | ✅       |
| ...                                                          | ...     |



# Usage method

The parameters [js_switch, redis_switch, redis_config] in the configuration file setting.py need to be modified in advance.

Launch the Flask web project using the main.py file and access the corresponding URL to retrieve data from Redis.



## Start Flask project

```bash
# -p post -h access
flask run -p 8888 -h 0.0.0.0
```

| address      | describe                                     |
| ------------ | -------------------------------------------- |
| /success/get | Retrieve available proxies.                  |
| /success/all | Retrieve all available proxies.              |
| /proxy/all   | Retrieve all proxies from the proxy pool.    |
| /proxy/get   | Retrieve a single proxy from the proxy pool. |



## Start proxy pool

Start the terminal command to retrieve the proxy pool.

```bash
# Initial retrieval and filtering of proxies.
python run.py crawling 
# Second retrieval and filtering of proxies.
python run.py extract
# The terminal command also provides a way to retrieve proxies.
# Retrieve available proxies.
python run.py obtain get
# Retrieve all available proxies.
python run.py obtain all
```



# Schedule List

| function            | state       | notes |
| ------------------- | ----------- | ----- |
| address display     | Not Started |       |
| Persistence Storage | Not Started |       |
|                     |             |       |

