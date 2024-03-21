import json
import sys
import subprocess
import os


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
            var_type = variable["type"]
            if var_type == "str":
                var_value = f'"{var_value}"'
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

            implementation = func_details.get("implementation", "")
            if isinstance(implementation, list):
                for impl_step in implementation:
                    if impl_step["type"] == "function":
                        args = ", ".join(f'"{arg["value"]}"' if arg["type"] == "str" else arg["value"] for arg in impl_step["args"])
                        code += f"        {impl_step['name']}({args})\n"
            else:
                implementation_lines = implementation.split("\n")
                for line in implementation_lines:
                    code += f"        {line}\n"

        if "main" in json_data["Class"]["functions"]:
            code += f"\nif __name__ == '__main__':\n"
            code += f"    {class_name}().main()\n"

        return code


    @staticmethod
    def execute_python_code(python_code):
        try:
            with open("generated_code.py", "w") as f:
                f.write(python_code)
            output = subprocess.run(["python", "generated_code.py"], capture_output=True, text=True)
            os.remove("generated_code.py")
            return output.stdout
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <jsonscr_file>")
        sys.exit(1)

    jsonscr_file = sys.argv[1]

    try:
        with open(jsonscr_file, 'r') as file:
            json_input = file.read()
            parsed_json = json.loads(json_input)
            python_code = ScriptRunner.generate_python_code(parsed_json)
            output = ScriptRunner.execute_python_code(python_code)
            print(output)
    except FileNotFoundError:
        print(f"Error: File '{jsonscr_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        sys.exit(1)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
