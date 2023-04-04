import ast
import re


def get_lines_of_code(node):
    function_name = node.name

    function_body = ast.unparse(node.body).strip()
    lines = function_body.split('\n')
    return function_name, lines


def deterministic_algorithm_option_not_used(libraries, filename, node):
    if "pytorch" in libraries:
        function_name = node.name
        function_body = ast.unparse(node.body).strip()
        deterministic_algorithms = function_body.count("torch.use_deterministic_algorithms(True)")
        message = "Please consider to remove the option 'torch.use_deterministic_algorithms(True)'. It can cause " \
                  "performance issues"
        if deterministic_algorithms > 0:
            to_return = [filename, function_name, deterministic_algorithms, message]
            return to_return
        return None
    return None


def merge_api_parameter_not_explicitly_set(libraries, filename, node):
    if "pandas" in libraries:
        function_name, lines = get_lines_of_code(node)
        number_of_merge_not_explicit = 0
        for line in lines:
            if "merge" in line:
                if "how" or "on" not in line:
                    number_of_merge_not_explicit += 1
        if number_of_merge_not_explicit > 0:
            message = "merge not explicit"
            to_return = [filename, function_name, number_of_merge_not_explicit, message]
            return to_return
        return None
    return None


def columns_and_datatype_not_explicitly_set(libraries, filename, node):
    if "pandas" in libraries:
        function_name = node.name
        function_body = ast.unparse(node.body).strip()
        call_function = function_body.split('\n')
        # get functions call of read_csv
        read_csv = []
        for line in call_function:
            if ('read_csv(' in line) or ('DataFrame(') in line:
                read_csv.append(line)
        number_of_apply = 0
        for line in read_csv:
            if 'dtype=' not in line:
                number_of_apply += 1
        message = "If the datatype is not set explicitly, it may silently continue the next step even though the input is unexpected, which may cause errors later." \
                  "It is recommended to set the columns and DataType explicitly in data processing."
        if number_of_apply > 0:
            to_return = [filename, function_name, number_of_apply, message]
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
    if "pandas" in libraries:
        function_name = node.name
        function_body = ast.unparse(node.body).strip()
        call_function = function_body.split('\n')
        # get functions call of read_csv
        read_csv = []
        variables = []
        number_of_apply = 0
        # get all defined variables that are dataframes
        for line in call_function:
            if ('read_csv(' in line) or ('DataFrame(') in line:
                read_csv.append(line)
                variables.append(line.split('=')[0].strip())
        variables = set(variables)

        # for each assignment of a variable
        for line in function_body.split('\n'):
            assign_pattern = r'(\w)+(\[.*\])+\s*=\s*(\w*)'
            if re.match(assign_pattern, line):
                # get the variable name
                variable = line.split('=')[0].strip().split('[')[0].strip()
                # check if the variable is a dataframe
                if variable in variables:
                    # check if the line is an assignment of a column of the dataframe
                    if (variable in line) and ('[' in line):
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
            to_return = [filename, function_name, number_of_apply, message]
            return to_return
        return []
    return []
