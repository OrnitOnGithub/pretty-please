# pretty-please

*pretty-please* is a groundbreaking interpreted programming language!

- 🔮 The future of programming
- 🚀 Written in Python
- 😎 Easy to learn
- 🙂 Sentient

## Run it!

You can show the help menu with
```
python3 pretty-please.py help
```
Create your first program by creating a file, i.e. `myprogram.prettyplease`. You can run it with:
```
python3 pretty-please.py myprogram.prettyplease
```

## Learn it!

*pretty-please* is super easy to learn! Everything you need to know is in this README!

### General shape

Instructions follow this structure:
```
opcode arg1 arg2 ... !
```

- `opcode` defines the instruction
- `args` are used by the interpret
- `!` ends the instruction

### comments
Comments start with a slash and end with an exclamation mark, just like every instruction. (Technically, `/` is the opcode here)
```
/ this is a comment !
dosomething!  / this is a comment !
```
Comments can help you make code clearer, but beware: **the interpret can read them**. If your comments are rude, you'll make it grumpier. The opposite applies as well.

### Hello World!

Writing a hello world program is stupidly simple!
```
helloworld!
```
There you go!

Make sure the compiler is happy. Otherwise it might say goobye world instead...

### Segfault

They say you only become a real programmer once you write your first segmentation fault. With pretty-please, this is also a one-liner!

```
segfault!
```

### testing

`test`: An instruction that does nothing relevant. Prints a small response in the terminal.
```
test
```

### REPL
Just use `repl!` to start a REPL.

### Variables
Define public variables using `define us a variable <name> = <integer value>` 
and private variables through `define me a variable <name> = <integer value>`. 
Public variables can be accessed when a module from `./lib/` is `import!`ed, 
private variables can only be accessed from the file (or a file included using `run!`).

### Errors

If something bad happens, you'll make the interpret sadder. Be careful.

### By the way,

If the interpret's mad at you there's a chance it will refuse to follow orders.

### Further opcodes
Look at `startup.prettyplease` for more examples of opcodes.

### Visual Studio Code extension

A vscode extension is available! It will later be added to the marketplace, but for now check it out [right here in the repo](./vscode-extension/README.md).

## Contribute

Check out [the contribution guidelines](CONTRIBUTE.md)
