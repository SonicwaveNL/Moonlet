# Moonlet
Is a turing-complete programming language, which at it's core replaces the buzz-keywords from most programming languages with strong and straight forward 'operational symbols'. Each 'symbol' is centered around the `=` (equal sign).

> 🚀 — *Note that this was made for a school project!*

## Table of Content

- [Moonlet](#moonlet)
  - [Table of Content](#table-of-content)
  - [Grammer](#grammer)
    - [Variables](#variables)
      - [Binary Operations](#binary-operations)
    - [Operation and Assignment](#operation-and-assignment)
    - [Functions](#functions)
    - [Return](#return)
    - [If-statements](#if-statements)
    - [Comments](#comments)
    - [Printing](#printing)
  - [Code Structure](#code-structure)
    - [Launcher](#launcher)
    - [Lexer](#lexer)
    - [Parser](#parser)
    - [Program (Interpeter)](#program-interpeter)
    - [Errors](#errors)
  - [Testing](#testing)
  - [Tuning Complete](#tuning-complete)
  - [Higher Order Functions](#higher-order-functions)
  - [Decorator](#decorator)
  - [Examples](#examples)

## Grammer

> *Click on a description to go to a more detail explanation.*

| Symbol | Description                                | Syntax                                                           | Example                                              |
| :----- | :----------------------------------------- | :--------------------------------------------------------------- | :--------------------------------------------------- |
| `=:`   | [Variables](#variables)                    | <pre> =: \<label\> \<value\> </pre>                              | <pre> =: x 10 </pre>                                 |
| `=+`   | [Add and Assign](#binary-operations)       | <pre> =+ \<label\> \<value\> </pre>                              | <pre> =+ x 3 </pre>                                  |
| `=-`   | [Substract and Assign](#binary-operations) | <pre> =- \<label\> \<value\> </pre>                              | <pre> =- x 3 </pre>                                  |
| `=*`   | [Multiply and Assign](#binary-operations)  | <pre> =* \<label\> \<value\> </pre>                              | <pre> =* x 3 </pre>                                  |
| `=/`   | [Divide and Assign](#binary-operations)    | <pre> =/ \<label\> \<value\> </pre>                              | <pre> =/ x 3 </pre>                                  |
| `=\|`  | [Functions](#functions)                    | <pre> =\| \<label\> (\<params\>) ={ <br>  \<body\> <br> } </pre> | <pre> =\| func_name (x) ={ <br>    ... <br> } </pre> |
| `=>`   | [Return](#return)                          | <pre> => \<value\|call\> </pre>                                  | <pre> => x </pre>                                    |
| `=?`   | [If-statement](#if-statement)              | <pre> =? \<comperation\> \<true\> : \<false\> </pre>             | <pre> =? x == y =! "TRUE" : =! "FALSE" </pre>        |
| `=#`   | [Comments](#comments)                      | <pre> =# \<content\> </pre>                                      | <pre> =# comment </pre>                              |
| `=!`   | [Priting](#printing)                       | <pre> =! \<content\> </pre>                                      | <pre> =# "Hello World!" </pre>                       |

### Variables
`=: <name> <value>`

Variable assignment is done using the `=:` symbols, followed by the name/label of the variable. The name/label is followed by any value that needs to be stored within the variable. This could be a variable id, an integer, a float, a string or a boolean value.

> *Note: The type of the variable is determined by the interpeter.*

```
=: x 10
```

#### Binary Operations
`<label> <operation> <value>`

Any binary mathematical operations is done by defining a left and right value with an operational symbol in between.

| Symbol | Operation    | Example            |
| :----- | :----------- | :----------------- |
| `+`    | Adding       | <pre> x + y </pre> |
| `-`    | Substracting | <pre> x - y </pre> |
| `*`    | Multiplying  | <pre> x * y </pre> |
| `/`    | Dividing     | <pre> x / y </pre> |


### Operation and Assignment
`=<operation> <label> <value>`

When performing a mathematical calculation, their is an option to use a shortcut to perform an operation and directly assign or override a variable with the result of this calculation.

To perform an operation and assign the result to the left value, by using the `=` symbol followed by the math operator symbol,
which defines the operation to perform. To perform 'add and assign' operation:

```
=+ x 10
```

### Functions
`=| <name> (<params>) ={ <body> }`

To write a function definition the `=|` sybols are used, followed by the name, the parameters and the `={` to define the body of the function. A function is closed off by a closing bracket `}`.

```
=| sum (x, y) ={
    =+ x y
    => x
}
```

### Return

When declaring or calling a function it's a must to return a created result, caused by this declared/called function. The return statement could be either: a value created within the function, another call from a different function, or calling the function again recursively.

`=> <value|call>`

```
=> x
```

### If-statements
`=? <comperation> <true>` or `=? <comperation> <true> : <false>`

When performing certain operations, it's sometimes prefered to create a certain decision based on a given certain comperation. To make this happen the `=?` is used, followed by the comperation to make. After the execution of this comperation, the left- or right side of the if-statement is executed, based on it's result is either True/False.

*Note: The 'else' section at the end is optional and not necessary to declare the if-statement.*

```
=? x == y =! "TRUE" : =! "FALSE"
```

### Comments
`=# <content>`

To make things more readable within the written code, it's possible to declare an comment to improve the readability of the code.

Comments within the code are done by using the `=#` symbol, followed by the content of the comment.

```
=# This is a usefull comment
```

### Printing
`=! <content>`

When working on the code it's sometimes wanted to print a result of an action in the console of the written application. To print either the result, a custom message or anything else: use the `=!` symbols followed by the content to print.

```
=! "Printing this!"
```

## Code Structure

The structure of the code can be divided in certain sections: launcher, lexer, parser and the program itself.

> *Note: The code includes a rich documentation, to make certain parts and combinations more clear to the developer. Please read the 'docstring' or 'inline documentation' for a more in depth explanation.*

| file          | description                                                                                                                                                |
| :------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `errors.py`   | File containing the different errors that could happen when launching, lexing, parsing or running the code.                                                |
| `launcher.py` | File containing the launcher of the code strucuture, which passes on either the plain text of a file, or the input of the console command.                   |
| `lexer.py`    | File containing the Lexer, who scans the given text and turns it into Tokens, which are passed to Parser.                                                  |
| `nodes.py`    | File containing the different Nodes that are created when the Parser parses the given tokens coming from the Lexer.                                        |
| `parser.py`   | File containing the Parser, who recognizes the Tokens, given by the Lexer and transforms those into Nodes. These nodes form the ATS (Abstract syntax Tree) |
| `position.py` | File containing the Position class, which is being used to not the position of a certain Token, Node or Action within the input file.                      |
| `program.py`  | File containing the Program with the interpreter code. The Program reads the ATS (Abstract syntax Tree) and performs certain actions accordingly           |

### Launcher
`/interpreter/launcher.py`

The first step in the process when running/launching the written Moonlet code or given console command is that: the launcher receives either an action to use i/o to open file with the `.mnl` extension, which include the written Moonlet code.

The code is then passed to the lexer for furter tokenization. 

### Lexer
`/interpreter/lexer.py`

When being passed the plain text, recieved by the launcher of the Moonlet interpreter, the Lexer scans the written code line by line. After recognizing certain patterns and/or expressions, the Lexer transforms the plain text to Tokens. These different tokens can be found in the `/interpreter/tokens.py` file.

### Parser
`/interpreter/parser.py`

...

### Program (Interpeter)
`/interpreter/program.py`

...

### Errors

When either launching, lexing, parsing or running the program/interpreter of the Moonlet programming languages, it possible to stumble upon an Error message with an explantion who/which thing caused it.

| error                 | description                                                                                                                                                                                                             |
| :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Error`               | This is the default error, this is used a the most basic error and mainly used as a subclass of the other errors who go more in depth.                                                                                  |
| `InvalidSyntaxError`  | This is caused when the given input is not recognized as valid syntax. Moonlet hints the user the format which makes the input valid.                                                                                   |
| `NotImplementedError` | This hints any user and mostly the developer(s) of Moonlet that this certain use of the Moonlet programming languages is not yet implemented and acts as a placeholder for future expantion of the Moonlet interpreter. |
| `RunTimeError`        | This is caused when the given input resulted in an invalid state at runtime. This has many reasons to cause this and are explained with more detail by the Moonlet interpreter at runtime.                              |
| `ZeroDivisionError`   | This is caused when the user is trying to divide a certain value from either a variable or a constant with zero.                                                                                                        |
| `FileNotFoundError`   | This is caused when the CLI application recieved a invalid 'path to file' input.                                                                                                                                        |

## Testing
---

To validate the working and quality of the written code for this interpreter language, 3 types of tests (levels) are written. These can be found within the `/tests` folder. 

- **System Tests** — `/tests/system_tests.py`
- **Integration Tests** — `/tests/integration_tests.py`
- **Unit Tests** — `/tests/unit_tests.py`

To run a test, for example the 'unit' tests, run the following within the console while being in the root folder:

```bash
python3 -m tests.unit_tests
```

## Tuning Complete

> *Note: see the [Examples](#examples) section to learn about how to run the examples, who showcases the working of this 'Turing Complete' interpreter lanuage.*

Moonlet is a Turing Complete language. This is determined by the fact the language supports important functions who are necessary to proclaim as a Turing Complete language.

- [x] **I/O** — Moonlet supports a format which asks the user for an input, and shows/uses this as an output.    
- [x] **Functions** — Moonlet supports a format for defining functions and a way to call these defined functions. 
- [x] **Recursion** — Moonlet supports recursion within functions. This could either be the same or another function.
- [x] **Loops** — Moonlet supports a format of creating a iteration over certain values with the power of recursion.
- [x] **If-statements** — Moonlet supports conditional statements by using the if-else format.

## Higher Order Functions

When developing the code of the Moonlet programming language, certain HOF (Higher-order functions). These include:

- `map`
- `reduce`
- `zip`

Besides the use of these functions, an own standalone HOF (Higher-order function) is written: the `format_args()` function.

The sole purpose of this function is to format the (key) parameters of the given object, and return it as a `dict`. This became quite usefull for the loggers, used withint the development enviroment. This function can be found within the `/interpreter/utils.py` file.

The power of the concept of any HOF (Higher-order function) are being used at it's fullest potential when looking at the different state classes for each step of the flow from beginning to end. For example the `ProgramState` class uses the `success` and `fail` functions to pass on either a state, a result or an error message.

## Decorator

When setting the `--debug` flag while executing a Moonlet program from a valid file, an in depth 'debug message' will be displayed during the execution of the different steps. This is been made possible by the `@debug_log()` decorator from file: `/interpreter/utils.py`.

As an example, the decorator has being used within the `Program` class, above the `exec(...)` function:

```python
@debug_log('Program.exec')
def exec(self, node: BaseNode, scope: Scope) -> ProgramState:
  ...
```

As a result of using the decorator in combination with the `--debug` flag, a debug message will be displayed witin the console:

```bash
Program.exec                   VarNode('=:' x 10), <Program>
```

## Examples

To showcase the strength of the interpeter language, a couple examples can be found within the `/examples` folder.

To run an example, for example the '' example, run the following within the console while being in the root folder:

```bash
python3 -m Moonlet.py examples.test_operations
```