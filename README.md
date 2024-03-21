# JSONScript

This project consists of a custom domain-specific language (DSL) and a corresponding compiler that translates programs written in the DSL into executable Python code.

## Language Overview

The custom language allows users to define Python classes, methods, imports, variables, loops, conditionals, and user input using a JSON syntax.

### Supported Constructs

- **Imports**: Import modules using `import` or `from ... import ...` syntax.
- **Variables**: Define variables with optional types and initial values.
- **Classes**: Define classes with one or more methods.
- **Methods**: Define methods with optional parameters and implementations.
- **Function Calls**: Call functions with specified arguments.
- **Loops**: Implement loops using `for` loops.
- **User Input**: Obtain user input using the `input()` function.
- **Conditionals**: Implement branching logic using `if-else` statements.

## Compiler Overview

The compiler translates JSON representations of programs written in the custom language into executable Python code. It follows a simple process:

1. **JSON Parsing**: Parse the input JSON file containing the program definition.
2. **Code Generation**: Generate Python code based on the parsed JSON structure.
3. **Error Handling**: Perform type checking and raise appropriate errors for inconsistencies.
4. **Execution**: Write the generated Python code to a temporary file and execute it using a subprocess.

## Usage

To use the compiler, follow these steps:

1. Create a JSON file containing a program written in the custom language.
2. Run the compiler script, passing the path to the JSON file as a command-line argument.
3. The compiler will generate equivalent Python code and execute it, displaying any output produced.

## Example

Here's a simple example of a program written in the custom language:

```json
{
  "Imports": [],
  "Variables": [
    {"name": "x", "type": "int", "value": 10}
  ],
  "Class": {
    "name": "Example",
    "functions": {
      "main": {
        "implementation": [
          {"type": "function", "name": "print", "args": [{"type": "str", "value": "Value of x: "}, {"type": "var", "value": "x"}]}
        ]
      }
    }
  }
}
