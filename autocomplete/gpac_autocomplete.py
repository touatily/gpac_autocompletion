#! /usr/bin/python3

from re import findall
from pathlib import Path
from subprocess import check_output, CalledProcessError
import cache_manager as cm


quote_added = False
list_help = ["-h", "-help", "-ha", "-hx", "-hh"]
list_filters = []
list_modules = []
list_props = []
protocols = {}
help_options = ["doc", "alias", "log", "core", "cfg", "net", "prompt", "modules", "module", "creds",
                "filters", "codecs", "formats", "protocols", "props", "colors", "layouts", "links", 
                "defer"]

CACHE_PATH = str(Path.home()) + "/.cache/gpac/gpac_autocomplete.json"
cache = cm.Cache(CACHE_PATH)

# get all possible args for a filter
def get_list_args(gfilter: str) -> dict:
    """
    Retrieve a list of arguments from the cache based on the given filter.
    """
    return cache.get_cache_list_args(gfilter)

# get type and possible values for an arg of a filter
def get_type_arg_filter(gfilter: str, arg: str) -> tuple:
    """
    Retrieve the type and possible values of an argument from the cache.
    """
    return cache.get_cache_type_arg_filter(gfilter, arg)

# lazy loading of filters
def get_list_filters() -> list:
    global list_filters
    if list_filters == []:
        list_filters = cache.get_cache_list_filters()
    return list_filters

# lazy loading of modules
def get_list_modules() -> list:
    """
    Returns the list of modules. If the list is empty, it fetches the list from the cache.

    Returns:
        list: A list of modules.
    """
    global list_modules
    if list_modules == []:
        list_modules = cache.get_cache_list_modules()
    return list_modules

# lazy loading of protocols
def get_list_protocols() -> None:
    global protocols
    if protocols == {}:
        protocols = cache.get_cache_list_protocols()

# lazy loading of props
def get_list_props() -> list:
    global list_props
    if list_props == []:
        list_props = cache.get_cache_list_props()
    return list_props

# get autocompletion list from compgen built-in bash command
def get_list_compgen(current : str, only_dirs : bool) -> list:
    """
    Generates a list of possible completions for a given path prefix using the `compgen` command.

    Args:
        current (str): The current path prefix to complete. 
            If it starts with '~', it will be expanded to the user's home directory.
        only_dirs (bool): If True, only directories will be considered for completion. 
            If False, both files and directories will be considered.

    Returns:
        list: A list of possible completions for the given path prefix. 
            Each completion will have spaces escaped and directories will end with a '/'.
    """
    if current is None:
        return []

    opt = "-d" if only_dirs else "-f"
    sub = 0
    home = str(Path.home())
    if len(current) > 0 and current[0] == "~":
        sub = len(home)
        current = home + current[1:]
    try:
        current_cleaned = current.replace(r"\ ", " ")
        compgen_cmd = f"compgen {opt} -- \"{current_cleaned}\""
        result = check_output(compgen_cmd, shell=True, executable='/bin/bash').decode().split('\n')
        if sub > 0:
            result = ["~" + e[sub:].replace(" ", r"\ ") + "/" if Path(e).is_dir() else "~" + e[sub:].replace(" ", r"\ ") + " " for e in result if e != ""]
        else:
            result = [e.replace(" ", r"\ ") + "/" if Path(e).is_dir() else e.replace(" ", r"\ ") + " " for e in result if e != ""]

    except CalledProcessError as e:
        result = []
    return result

def get_list_values_enum_args(gfilter: str) -> dict:
    return cache.get_cache_list_values_enum_args(gfilter)


def analyze_filter(filter, current_word, help_mode=False):
    list_args = get_list_args(filter)
    list_enum_values = get_list_values_enum_args(filter)

    possiblities = list_args
    completions = []

    if not help_mode:
        args = current_word.split(":")

        opt = [*args]
        used_props = set()
        for i in range(len(opt)):
            temp = opt[i].split("=")[0]
            if temp in list_args:
                opt[i] = temp
            elif opt[i] in list_enum_values:
                # get arg name
                opt[i] = list_enum_values[opt[i]]
            elif len(temp) > 0 and temp[0] == "#":
                used_props.add(temp[1:])


        if args[0] != filter:
            completions = []
        elif current_word[-1] == ":":
            completions = [e for e in possiblities if e not in opt] + [e for e in list_enum_values if list_enum_values[e] not in opt]
        else:
            if len(args) == 1:
                completions = [current_word + " "]
                if len(list_args) > 0:
                    completions += [current_word + ":"]
            elif len(args[-1])>0 and args[-1][0] == "#":
                props = [e for e in get_list_props() if e not in used_props]
                prop_name = args[-1][1:]
                completions = ["#"+e for e in props if e.startswith(prop_name)]
            elif args[-1] in list_enum_values:
                completions = [args[-1] + " ", args[-1] + ":"]
            elif opt[-1] in possiblities:
                # get type of arg
                type, values = get_type_arg_filter(filter, opt[-1])

                if type != "bool":
                    if "=" in args[-1]:
                        s = args[-1].index('=')
                        if type == "strl":
                            if args[-1][-1] == "=":
                                completions = []
                            elif args[-1][-1] == ",":
                                completions = [args[-1][s+1:]]
                            else:
                                completions = [args[-1][s+1:], args[-1][s+1:]+",", args[-1][s+1:]+":"]
                        elif type=="str" or type=="cstr":
                            if not quote_added:
                                if args[-1][s+1:].startswith("\""):
                                    completions = [args[-1][s+1:]+":", args[-1][s+1:]+" "]
                                else:
                                    completions = ['"'+args[-1][s+1:]+'":', "\"" + args[-1][s+1:]+"\" ", "\"" + args[-1][s+1:]]
                            else:
                                value = args[-1][s+1:-1]
                                if value.startswith("\""):
                                    completions = [value, value+"\":", value+"\" "]

                            if opt[-1] == "src":
                                completions += get_list_compgen(current_word, False)
                        elif type == "enum":

                            completions = [e if e!=args[-1][s+1:] else e+" " for e in values if e.startswith(args[-1][s+1:])]
                            if args[-1][s+1:] in values:
                                completions += [args[-1][s+1:] + ":"]
                        else:
                            if args[-1][-1] != "=":
                                completions = [args[-1][s+1:]+':', args[-1][s+1:] + " "]
                    else:
                        completions = [opt[-1] + "="]
                else:
                    if "=" in args[-1]:
                        s = args[-1].index('=')
                        value = args[-1][s+1:]
                        completions = [e if e!=value else e+" " for e in ["true", "false"] if e.startswith(value)]
                        if value in {"true", "false"}:
                            completions += [value + ":"]
                    else:
                        completions = [args[-1]+":", args[-1]+" ", args[-1] + "="]

            completions += [e for e in possiblities if e.startswith(args[-1]) and e not in opt] + \
                            [e for e in list_enum_values if list_enum_values[e] not in opt[:-1] and e.startswith(args[-1]) and e != args[-1]]
    else:
        if current_word == filter:
            completions = [filter + " "]
            if len(list_args) > 0:
                completions += [filter + "."]
        elif current_word.startswith(filter+"."):
            index = current_word.index(".")
            completions = [filter+"."+e+" " for e in possiblities if e.startswith(current_word[index+1:])]

    return completions


def generate_completions(command_line, cursor_position):
    global quote_added

    command_line = command_line[0:cursor_position]

    quote_added = False
    if command_line.count("\"") % 2==1:
        command_line += "\""
        quote_added = True

    pattern = r'(?:[^\s"\\]+|"(?:\\.|[^"\\])*"|\\.)+'
    command_line_words = findall(pattern, command_line)


    if command_line[-1] == " " and command_line[-2] != "\\":
        command_line_words.append("")

    ## check wether help is being requested
    help_mode = False
    for i in range(len(command_line_words)-1):
        if command_line_words[i] in list_help:
            help_mode = True
            break

    completions = []

    ## get current and previous word being typed
    current_word = ""
    previous_word = ""

    if len(command_line_words) > 0:
        current_word = command_line_words[-1]
        if len(command_line_words) > 1:
            previous_word = command_line_words[-2]

    if help_mode:
        if previous_word == "module" or previous_word == "modules":
            completions = [e+" " for e in get_list_modules()+[""] if e.startswith(current_word)]
        elif previous_word == "links":
            completions = [e+" " for e in get_list_filters()+[""] if e.startswith(current_word)]
        elif previous_word == "props":
            completions = [e+" " for e in get_list_props()+[""] if e.startswith(current_word)]
        else:
            if current_word.split('.')[0] in get_list_filters():
                completions = analyze_filter(current_word.split('.')[0], current_word, help_mode)
            if len(completions) == 0:
                completions = [e+" " for e in help_options if e.startswith(current_word)] + \
                                [e for e in get_list_filters() if e.startswith(current_word)]

    else:
        if (previous_word in {'-i', '-src', '-dst', '-o'}) or current_word.startswith('src=') or current_word.startswith('dst='):
            get_list_protocols()
            input_protocols = [p for p in protocols if protocols[p]["input"] != []]
            output_protocols = [p for p in protocols if protocols[p]["output"] != []]

            list_cur = current_word.split(":")
            curr_option = list_cur[-1]
            protocol = list_cur[0]


            if previous_word == "-i" or previous_word == "-src":
                possibilities = [e+"://" for e in input_protocols]
                completions = [e for e in possibilities if e.startswith(current_word)] + get_list_compgen(current_word, False)
            elif previous_word == "-o" or previous_word == "-dst":
                possibilities = [e+"://" for e in output_protocols]
                completions = [e for e in possibilities if e.startswith(current_word)] + get_list_compgen(current_word, True)
            elif current_word.startswith("src="):
                possibilities = [e+"://" for e in input_protocols]
                completions = [e for e in possibilities if e.startswith(current_word[4:])] + get_list_compgen(current_word.split("=")[1], False)
            elif current_word.startswith("dst="):
                possibilities = [e+"://" for e in output_protocols]
                completions = [e for e in possibilities if e.startswith(current_word[4:])] + + get_list_compgen(current_word.split("=")[1], True)


        elif current_word == "":
            completions = ["-h", "-help", "-netcap=", "-graph", "-stats", "-src", "-i", "-logs", "-dst", "-o"] + get_list_filters()
        elif current_word == "-":
            completions = ["-h", "-help", "-netcap=", "-graph", "-stats", "-src", "-i", "-logs", "-dst", "-o"]
        elif current_word[0] == "-":
            completions = [e for e in ["-h", "-hx", "-help", "-netcap=", "-graph", "-stats", "-src", "-i", "-logs", "-dst", "-o"] if e.startswith(current_word)]
        else:

            for gfilter in get_list_filters():
                if current_word.split(':')[0] == gfilter:
                    completions = analyze_filter(gfilter, current_word, help_mode)
                    break
            if len(completions) == 0:
                possibilities = get_list_filters()
                completions = [e for e in possibilities if e.startswith(current_word)]

    return completions



if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        sys.exit(1)

    pos = int(sys.argv[1])
    command_line = sys.argv[2][1:-1]   # Remove the quotes added by Bash script

    # Generate possible completions
    try:
        completions = generate_completions(command_line, pos)
    except Exception as e:
        completions = []

    # Print each completion on a new line, as expected by Bash
    for completion in completions:
        print(completion)
