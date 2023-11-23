# Scripts Shelly

[Documentation page](https://shelly-api-docs.shelly.cloud/)

## Commands

- Give Switch Status: `./shelly.py -p switch status `
- Exec Script: `./shelly.py -p scripts exec <script-id> "<code>"`

## Example

```bash
$ ./shelly.py -p scripts create hello-world.mjs test
1
$ ./shelly.py -p scripts getcode 1
function hello_world() {\n    return \"hello world !\"\n}
$ ./shelly.py -p scripts start 1
{
    "was_running": false
}
$ ./shelly.py -p scripts exec 1 "hello_world()"
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
abonneau@jetson-nano-1-107:~/Edge-AI-For-SHM/scripts$ ./shelly.py -p scripts delete 1
```