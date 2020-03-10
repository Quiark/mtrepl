# Minetest REPL

(actually it's not a REPL yet)

This plugin allows sending chunks of code to a running minetest server, possibly replacing
some functions, for the purpose of faster development loop.


## Running

First start the code server

```
python3 server.py
```

Then enable the Minetest mod to make HTTP calls.

Then you can run `python3 cli.py` to send commands directly or you can somehow integrate it into your code
editor to more easily send code blocks.

## Security

This mod is inherently dangerous to run. Anyone who can connect to it can execute Lua code
with extended privileges in Minetest which can probably lead to generic code execution on the machine.
That's why the code server is configured to listen on loopback only and you should make sure
to have your firewall enabled as well.


Need to add mtrepl to 
`secure.trustedmods`
