import importlib
import importlib.metadata
from os.path import abspath
import re
from pprint import pprint
import plantuml
import sys


def generate_plantuml(init_package_name):
    #print(f"package: {init_package_name}")
    def process_package_metadata(package) -> dict[str, str]:
        def is_a_requirement() -> bool:
            return param == "Requires-Dist" and '(' in value

        dep_list = dict()
        for param, value in package.items():
            param: str; value: str
            #print(param, " >>>>> ", value)
            #print(value)
            if is_a_requirement():
                module: str = value[:value.find(' ')]
                #print(module)
                version: str = value[value.find('=')+1 : value.find(')')]
                #print(version)
                dep_list[module] = version
        return dep_list

    def process_dependency(cur_package_name):
        nonlocal plantuml_objects, plantuml_dependencies
        #print(cur_package_name)
        plantuml_objects += f'object {cur_package_name}\n'
        spec = importlib.metadata.metadata(cur_package_name)

        cur_dependencies = process_package_metadata(spec)

        for dependency_name in cur_dependencies:
            cur_version = cur_dependencies[dependency_name]
            plantuml_dependencies += f'{cur_package_name} --|> {dependency_name} : {cur_version}\n'
            process_dependency(dependency_name)

    plantuml_code = "@startuml\n"

    plantuml_objects = ""
    plantuml_dependencies = ""

    try:
        process_dependency(init_package_name)
    except ModuleNotFoundError as err:
        print(f"Такого пакета нет: {init_package_name}")
        return ""

    plantuml_code += plantuml_objects
    plantuml_code += '\n'
    plantuml_code += plantuml_dependencies
    plantuml_code += "@enduml\n"
    
    #print(f"{plantuml_code=}")
    return plantuml_code


def main():
    package_name = input("Введите название пакета: ")
    #package_name = "flask"
    plantuml_code = generate_plantuml(package_name)

    with open("output_file.txt", 'w') as output_file:
        output_file.write(plantuml_code)

    server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/',
                               basic_auth={},
                               form_auth={}, http_opts={}, request_opts={})

    server.processes_file(abspath('./output_file.txt'))


if __name__ == "__main__":
    main()
