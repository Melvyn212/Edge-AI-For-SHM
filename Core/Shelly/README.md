# Shelly Utilities

[Shelly API Documentation page](https://shelly-api-docs.shelly.cloud/)

## Commands

- Give Switch Status: `./shelly.py -p switch status `
- Eval Script: `./shelly.py -p scripts exec <script-id> "<code>"`
- Call Script API: `./shelly.py -p scripts call <script-id> "<endpoint>"`

## Scripts

### hello-world.js

Usual script test

```bash
$ ./shelly.py -p scripts create hello-world.js test
1
$ ./shelly.py -p scripts getcode 1
function hello_world() {\n    return \"hello world !\"\n}
$ ./shelly.py -p scripts start 1
{
    "was_running": false
}
$ ./shelly.py -p scripts eval 1 "hello_world()"
hello world !
$ ./shelly.py -p scripts stop 1
{
    "was_running": true
}
$ ./shelly.py -p scripts list
[
    {
        "enable": false,
        "id": 1,
        "name": "test",
        "running": false
    }
]
$ ./shelly.py -p scripts delete 1
```

### simple-powermeter.js

Show single measurement power meter

### PowerTracker.js

Show complex power meter which keeps track of the last power measurement on yield them if asked

```bash
$ ./shelly.py -p scripts create PowerTracker.js power
1
$ ./shelly.py -p scripts start 1
{
    "was_running": false
}
$ ./shelly.py -p scripts call 1 "api?yield"
[
    {
        "current": 0.035,
        "power": 3.5,
        "timestamp": 1700840114,
        "voltage": 226.1
    },
    ...
]
$ ./shelly.py -p scripts stop 1
$ ./shelly.py -p scripts delete 1
```

## Miscellaneous

Activate debug:

```bash
$ export SHELLY=10.0.0.250 # IP of your device
$ curl -X POST -d '{"id":1, "method":"Sys.SetConfig", "params":{"config":{"debug":{"websocket":{"enable":true}}}}}' http://${SHELLY}/rpc
```

Contact debug websocket:

```bash
$ curl --include -o - --http1.1 --no-buffer \
       -H "Connection: Upgrade" \
       -H "Upgrade: websocket" \
       -H "Host: $SHELLY" \
       -H "Origin: http://$SHELLY/debug/log" \
       -H "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
       -H "Sec-WebSocket-Version: 13"\
  http://$SHELLY/debug/log
```