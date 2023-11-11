# Proxy_List

`Proxy_list` Implement the retrieval of free proxy IP addresses through a network channel by providing proxy addresses. Perform initial filtering by validating the proxies, and then conduct a second round of screening before using them. The goal is to obtain stable and reliable proxy IP addresses along with their corresponding ports.



# Sources

| Source         | Succeed |
| -------------- | ------- |
| Do not list... | ...     |



# Note

Before starting the program, it is necessary to modify the parameters in the configuration file

1. Permission related
2. Storage related(redis)



# Usage method

## Start Flask project

Using Python to execute the main file or launching the Flask program through a terminal

```bash
# -p post -h access
flask run -p 8888 -h 0.0.0.0
```

| address                       | describe                                                     |
| ----------------------------- | ------------------------------------------------------------ |
| /proxy/get                    | Get Proxy Pool Proxy                                         |
| /proxy/all                    | Obtain all proxies in the proxy pool                         |
| /proxy/verify/?url={url}      | Generate available proxies for the specified URL address     |
| /proxy/confirm/get/?url={url} | Obtain the available proxy for verifying the specified URL   |
| /proxy/confirm/all/?url={url} | Obtain all available proxies for verifying the specified URL |



# Schedule List

| function            | state       | notes |
| ------------------- | ----------- | ----- |
| address display     | Not Started |       |
| Persistence Storage | Not Started |       |
| optimize api        | Not Started |       |

