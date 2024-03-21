import json
import sys
import subprocess
import os 

class ScriptRunner:
    @staticmethod
    def generate_python_code(json_data):
        code = ""

        if "Imports" in json_data:
            for module in json_data["Imports"]:
                code += f"import {module['name']}\n"
            code += "\n"
        else:
            code += "import random\n\n" 

        class_name = json_data["Class"]["name"]
        code += f"class {class_name}:\n"

        for func_name, func_details in json_data["Class"]["functions"].items():
            code += f"    def {func_name}(self"
            if "parameters" in func_details:
                for param in func_details["parameters"]:
                    code += f", {param['name']}: {param['type']}"
            code += f")"
            if "return_type" in func_details:
                code += f" -> {func_details['return_type']}"
            code += ":\n"

            if "implementation" in func_details:
                implementation_lines = func_details['implementation'].split('\n')
                for line in implementation_lines:
                    code += f"        {line}\n"
            else:
                code += "        raise NotImplementedError()\n"

        if "main" in json_data["Class"]["functions"]:
            main_func_impl = json_data["Class"]["functions"]["main"]["implementation"]
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
