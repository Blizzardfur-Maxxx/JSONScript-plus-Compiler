import json
import subprocess
import os
import sys
import random

class ScriptRunner:
    @staticmethod
    def generate_python_code(json_data):
        code = ""

        for module in json_data.get("Imports", []):
            if module.get("type") == "module":
                code += f"import {module['name']}\n"
            elif module.get("type") == "from":
                code += f"from {module['name']} import {module['import_name']}\n"
        code += "\n"

        for variable in json_data.get("Variables", []):
            var_name = variable["name"]
            var_value = variable["value"]
            code += f"{var_name} = {var_value}\n"
        code += "\n"

        class_name = json_data["Class"]["name"]
        code += f"class {class_name}:\n"
        for func_name, func_details in json_data["Class"]["functions"].items():
            code += f"    def {func_name}(self"
            if "parameters" in func_details:
                for param in func_details["parameters"]:
                    default_value = param.get("default", None)
                    param_str = f"{param['name']}"
                    if default_value is not None:
                        param_str += f"={default_value}"
                    code += f", {param_str}"
            code += "):\n"

            for step in func_details["implementation"]:
                if step["type"] == "function":
                    args = ", ".join(f'"{arg["value"]}"' if arg["type"] == "str" else arg["value"] for arg in step["args"])
                    code += f"        {step['name']}({args})\n"
                elif step["type"] == "loop":
                    loop_type = step["loop_type"]
                    variable = step["variable"]
                    start = step["start"]
                    end = step["end"]
                    step_value = step["step"]
                    code += f"        for {variable} in range({start}, {end}, {step_value}):\n"
                    for loop_step in step["body"]:
                        args = ", ".join(f'"{arg["value"]}"' if arg["type"] == "str" else arg["value"] for arg in loop_step["args"])
                        code += f"            {loop_step['name']}({args})\n"
                elif step["type"] == "input":
                    var = step["variable"]
                    code += f"        {var} = input()\n"
                elif step["type"] == "conditional":
                    condition = step["condition"]
                    code += f"        if {condition}:\n"
                    for conditional_step in step["body"]:
                        args = ", ".join(f'"{arg["value"]}"' if arg["type"] == "str" else arg["value"] for arg in conditional_step["args"])
                        code += f"            {conditional_step['name']}({args})\n"
                    if "else_body" in step:
                        code += "        else:\n"
                        for else_step in step["else_body"]:
                            args = ", ".join(f'"{arg["value"]}"' if arg["type"] == "str" else arg["value"] for arg in else_step["args"])
                            code += f"            {else_step['name']}({args})\n"
            code += "\n"

        code += "if __name__ == '__main__':\n"
        code += f"    {class_name}().main()\n"

        return code

    @staticmethod
    def execute_python_code(python_code):
        try:
            with open("generated_code.py", "w") as f:
                f.write(python_code)
            process = subprocess.Popen(["python", "generated_code.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            os.remove("generated_code.py")
            if stderr:
                print("Error:", stderr)
            return stdout
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <json_file>")
        sys.exit(1)

    json_file = sys.argv[1]

    try:
        with open(json_file, 'r') as file:
            json_input = file.read()
            parsed_json = json.loads(json_input)
            python_code = ScriptRunner.generate_python_code(parsed_json)
            output = ScriptRunner.execute_python_code(python_code)
            print(output)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        sys.exit(1)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)