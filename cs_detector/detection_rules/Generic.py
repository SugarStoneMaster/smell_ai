import ast
import re
from ..code_extractor.variables import get_all_set_variables
from ..code_extractor.models import check_model_method
from ..code_extractor.libraries import get_library_of_node, extract_library_name


def get_lines_of_code(node):
    function_name = node.name

    function_body = ast.unparse(node.body).strip()
    lines = function_body.split('\n')
    return function_name, lines


def deterministic_algorithm_option_not_used(libraries, filename, node):
    if [x for x in libraries if 'torch' in x]:
        function_name = node.name
        function_body = ast.unparse(node.body).strip()
        deterministic_algorithms = function_body.count("torch.use_deterministic_algorithms(True)")
        message = "Please consider to remove the option 'torch.use_deterministic_algorithms(True)'. It can cause " \
                  "performance issues"
        if deterministic_algorithms > 0:
            name_smell = "deterministic_algorithm_option_not_used"
            to_return = [filename, function_name, deterministic_algorithms, name_smell, message]
            return to_return
        return []
    return []


def merge_api_parameter_not_explicitly_set(libraries, filename, node):
    if [x for x in libraries if 'pandas' in x]:
        function_name, lines = get_lines_of_code(node)
        number_of_merge_not_explicit = 0
        for line in lines:
            if "merge" in line:
                if "how" or "on" or "validate" not in line:
                    number_of_merge_not_explicit += 1
        if number_of_merge_not_explicit > 0:
            message = "merge not explicit"
            name_smell = "merge_api_parameter_not_explicitly_set"
            to_return = [filename, function_name, number_of_merge_not_explicit, name_smell, message]
            return to_return
        return []
    return []


def columns_and_datatype_not_explicitly_set(libraries, filename, node):
    function_name, lines = get_lines_of_code(node)
    if [x for x in libraries if 'pandas' in x]:
        function_name = node.name

        # get functions call of read_csv
        read_csv = []
        for line in lines:
            if ('read_csv(' in line) or ('DataFrame(') in line:
                read_csv.append(line)
        number_of_apply = 0
        for line in read_csv:
            line = line.replace(' ', '')
            if 'dtype=' not in line or 'columns=' not in line:
                number_of_apply += 1
        message = "If the datatype or the columns are not set explicitly, it may silently continue the next step even though the input is unexpected, which may cause errors later." \
                  "It is recommended to set the columns and DataType explicitly in data processing."
        if number_of_apply > 0:
            name_smell = "columns_and_datatype_not_explicitly_set"
            to_return = [filename, function_name, number_of_apply, name_smell, message]
            return to_return
        return []
    return []


'''
Title: Empty column misinitialization
    Context: Developers may need a new empty column in DataFrame.


Problem: If they use zeros or empty strings to initialize a new empty column in Pandas, 
the ability to use methods such as .isnull() or .notnull() is retained. 
This might also happens to initializations in other data structure or libraries.
Examples: 
    - df['new_col_int'] = 0
    - df['new_col_str'] = ''
    '''


def empty_column_misinitialization(libraries, filename, node):
    # this is the list of values that are considered as smelly empty values
    empty_values = ['0', "''", '""']
    function_name, lines = get_lines_of_code(node)
    if [x for x in libraries if 'pandas' in x]:
        # get functions call of read_csv
        read_csv = []
        variables = []
        number_of_apply = 0
        # get all defined variables that are dataframes
        variables = get_all_set_variables(lines)
        # for each assignment of a variable
        for line in lines:
            assign_pattern = r'(\w)+(\[.*\])+\s*=\s*(\w*)'
            if re.match(assign_pattern, line):
                # get the variable name
                variable = line.split('=')[0].strip().split('[')[0].strip()
                # check if the variable is a dataframe
                if variable in variables:
                    # check if the line is an assignment of a column of the dataframe
                    if '[' in line:
                        # select a line where uses to define a column df.[*] = *
                        pattern = variable + '\[.*\]'
                        # check if the line is an assignment of the value is 0 or ''
                        if re.match(pattern, line):
                            if line.split('=')[1].strip() in empty_values:
                                number_of_apply += 1
        if number_of_apply > 0:
            message = "If they use zeros or empty strings to initialize a new empty column in Pandas" \
                      "the ability to use methods such as .isnull() or .notnull() is retained." \
                      "Use NaN value (e.g. np.nan) if a new empty column in a DataFrame is needed. Do not use “filler values” such as zeros or empty strings."
            name_smell = "empty_column_misinitialization"
            to_return = [filename, function_name, number_of_apply, name_smell, message]
            return to_return
        return []
    return []


def nan_equivalence_comparison_misused(libraries, filename, node):
    if [x for x in libraries if 'pandas' in x or 'numpy' in x]:
        function_name = node.name
        number_of_nan_equivalences = 0
        function_body = ast.unparse(node.body).strip()
        call_function = function_body.split('\n')
        for line in call_function:
            line_without_space = line.replace(" ", "")
            if "==np.nan" in line_without_space:
                number_of_nan_equivalences += 1
        if number_of_nan_equivalences > 0:
            message = "NaN equivalence comparison misused"
            name_smell = "nan_equivalence_comparison_misused"
            to_return = [filename, function_name, number_of_nan_equivalences, name_smell, message]
            return to_return
        return []
    return []


def in_place_apis_misused(libraries, filename, node):
    in_place_apis = 0
    function_name, lines = get_lines_of_code(node)
    if [x for x in libraries if 'pandas' in x]:
        for line in lines:
            if "dropna" in line and "=" not in line:
                in_place_apis += 1
    if [x for x in libraries if 'tensorflow' in x]:
        for l in lines:
            if "clip" in l and "=" not in l:
                in_place_apis += 1
    if in_place_apis > 0:
        message = "We suggest developers check whether the result of the operation is assigned to a variable or the" \
                  " in-place parameter is set in the API. Some developers hold the view that the in-place operation" \
                  " will save memory"
        name_smell = "in_place_apis_misused"
        to_return = [filename, function_name, in_place_apis, name_smell, message]
        return to_return
    return []


# questa secondo me da un botto di falsi positivi
def memory_not_freed(libraries, filename, fun_node, model_dict):
    if [x for x in libraries if 'tensorflow' in x]:
        model_libs = ['tensorflow']
    else:
        return []
    memory_not_freed = 0
    for node in ast.walk(fun_node):
        if isinstance(node, ast.For):  # add while
            model_defined = False
            # check if for contains ml method
            for n in ast.walk(node):
                if isinstance(n, ast.Call):
                    if isinstance(n.func, ast.Attribute):
                        method_name = n.func.attr + str('()')
                    else:
                        if hasattr(n.func, "id"):
                            method_name = n.func.id + str('()')
                            if check_model_method(method_name, model_dict, model_libs):
                                model_defined = True
            if model_defined:
                free_memory = False
                # check if for contains free memory
                for n in ast.walk(node):
                    if isinstance(n, ast.Call):
                        if isinstance(n.func, ast.Attribute):
                            method_name = n.func.attr
                        else:
                            if hasattr(n.func, "id"):
                                method_name = n.func.id
                                print(method_name)
                        if method_name == 'clear_session':
                            free_memory = True
                if not free_memory:
                    memory_not_freed += 1
    if memory_not_freed > 0:
        to_return = [filename, fun_node.name, memory_not_freed, "memory_not_freed", "Memory not freed"]
        return to_return
    return []


def hyperparameters_not_explicitly_set(libraries, filename, fun_node, model_dict):
    model_libs = []
    dict_libs = set(model_dict['library'])
    for lib in dict_libs:
        if [x for x in libraries if lib in x]:
            model_libs.append(lib)
    hyperparameters_not_explicitly_set = 0
    for node in ast.walk(fun_node):
        if isinstance(node, ast.Call):
            while isinstance(node.func, ast.Call):
                node = node.func
            model_defined = False
            if isinstance(node.func, ast.Attribute):
                method_name = node.func.attr + str('()')
            else:
                method_name = node.func.id + str('()')
            if check_model_method(method_name, model_dict, model_libs):
                if get_library_of_node(node, libraries) is None:
                    model_defined = True
                else:
                    if extract_library_name(get_library_of_node(node, libraries)).split(".")[0] in model_libs:
                        model_defined = True
            if model_defined:
                # check if hyperparameters are set
                if node.args == []:
                    hyperparameters_not_explicitly_set += 1
                    print(node.lineno)
    if hyperparameters_not_explicitly_set > 0:
        to_return = [filename, fun_node.name, hyperparameters_not_explicitly_set, "hyperparameters_not_explicitly_set",
                     "Hyperparameters not explicitly set"]
        return to_return

    return []
