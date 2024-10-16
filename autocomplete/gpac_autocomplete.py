#! /usr/bin/python3

import sys
from shlex import split as shplit
from pathlib import Path
import cache_manager as cm

exit_code = 0
quote_added = False
list_help = ["-h", "-help", "-ha", "-hx", "-hh"]
list_filters = []
list_modules = []
protocols = {}
help_options = ["doc", "alias", "log", "core", "cfg", "net", "prompt", "modules", "module", "creds", "filters", 
                "codecs", "formats", "protocols", "props", "colors", "layouts", "links", "defer"]

cache_path = str(Path.home()) + "/.cache/gpac/gpac_autocomplete.json"
cache = cm.cache(cache_path)

# get all possible args for a filter
def get_list_args(filter: str) -> dict:
    return cache.get_cache_list_args(filter)

# get type and possible values for an arg of a filter
def get_type_arg_filter(filter: str, arg: str) -> str:
    return cache.get_cache_type_arg_filter(filter, arg)

# lazy loading of filters
def get_list_filters() -> list:
    global list_filters
    if list_filters == []:
        list_filters = cache.get_cache_list_filters()
    return list_filters

# lazy loading of modules
def get_list_modules() -> list:
    global list_modules
    if list_modules == []:
        list_modules = cache.get_cache_list_modules()
    return list_modules

# lazy loading of protocols
def get_list_protocols()-> None:
    global protocols
    if protocols == {}:
        protocols = cache.get_cache_list_protocols()


def analyze_filter(filter, current_word, help=False):
    global exit_code

    list_args = get_list_args(filter)
    possiblities = list_args
    completions = []

    if not help:
        args = current_word.split(":")

        opt = [*args]
        for i in range(len(opt)):
            temp = opt[i].split("=")[0]
            if len(temp) > 0 and temp[0] == '!':
                temp = temp[1:]
            if temp in list_args:
                opt[i] = temp


        if args[0] != filter:
            completions = []
        elif current_word[-1] == ":":
            completions = [e for e in possiblities if e not in opt]
        else:
            if len(args) == 1:
                completions = [current_word + " "]
                if len(list_args) > 0:
                    completions += [current_word + ":"]
            elif opt[-1][0] == '!':
                completions = ['!'+e for e in possiblities if e.startswith(opt[-1][1:]) and list_args[e] == "bool" and e not in opt]
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
                                completions = ['"'+args[-1][s+1:]+'":', "\"" + args[-1][s+1:]+"\" "]
                            else:
                                completions = ["\"" + args[-1][s+1:]+"\""]
                            if opt[-1] == "src":
                                exit_code = 1
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
                    completions = [args[-1]+":", args[-1]+" "]

            completions += [e for e in possiblities if e.startswith(args[-1]) and e not in opt]
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
    global exit_code

    command_line = command_line[0:cursor_position]

    if command_line.count("\"") % 2==1:
        command_line += "\""
        quote_added = True
    command_line_words = shplit(command_line)[1:]


    if len(command_line) >= cursor_position and command_line[cursor_position-1] == " ":
        command_line_words.append("")

    ## check wether help is being requested
    help = False
    for i in range(len(command_line_words)-1):
        if command_line_words[i] in list_help:
            help = True
            break

    completions = []

    ## get current and previous word being typed
    current_word = ""
    previous_word = ""
    
    if len(command_line_words) > 0:
        current_word = command_line_words[-1]
        if len(command_line_words) > 1:
            previous_word = command_line_words[-2]

    if help:
        if previous_word == "module" or previous_word == "modules":
            completions = [e+" " for e in get_list_modules()+[""] if e.startswith(current_word)]
        elif previous_word == "links":
            completions = [e+" " for e in get_list_filters()+[""] if e.startswith(current_word)]
        elif previous_word == "props": 
            pass
        else:
            for filter in get_list_filters():
                if current_word.split('.')[0] == filter:
                    completions = analyze_filter(filter, current_word, help)
                    break
            if len(completions) == 0:
                completions = [e+" " for e in help_options if e.startswith(current_word)] + [e for e in get_list_filters() if e.startswith(current_word)]

    else:
        if (previous_word in {'-i', '-src', '-dst', '-o'}) or current_word.startswith('src=') or current_word.startswith('dst='):
            get_list_protocols()
            input_protocols = [p for p in protocols if protocols[p]["input"] != []]
            output_protocols = [p for p in protocols if protocols[p]["output"] != []]
            
            list_cur = current_word.split(":")
            curr_option = list_cur[-1]
            protocol = list_cur[0]


            if previous_word == "-i" or previous_word == "-src":
                exit_code = 1
                possibilities = [e+"://" for e in input_protocols]
                completions = [e for e in possibilities if e.startswith(current_word)]
            elif previous_word == "-o" or previous_word == "-dst":
                possibilities = [e+"://" for e in output_protocols]
                completions = [e for e in possibilities if e.startswith(current_word)]
            elif current_word.startswith("src="):
                exit_code = 1
                possibilities = [e+"://" for e in input_protocols]
                completions = [e for e in possibilities if e.startswith(current_word[4:])]
            elif current_word.startswith("dst="):
                possibilities = [e+"://" for e in output_protocols]
                completions = [e for e in possibilities if e.startswith(current_word[4:])]


        elif current_word == "":  
            completions = ["-h", "-help", "-netcap=", "-graph", "-stats", "-src", "-i", "-logs", "-dst", "-o"] + get_list_filters()
        elif current_word == "-":
            completions = ["-h", "-help", "-netcap=", "-graph", "-stats", "-src", "-i", "-logs", "-dst", "-o"]
        elif current_word[0] == "-":
            completions = [e for e in ["-h", "-hx", "-help", "-netcap=", "-graph", "-stats", "-src", "-i", "-logs", "-dst", "-o"] if e.startswith(current_word)]
        else:

            for filter in get_list_filters():
                if current_word.split(':')[0] == filter:
                    completions = analyze_filter(filter, current_word, help)
                    break
            if len(completions) == 0:
                possibilities = get_list_filters()
                completions = [e for e in possibilities if e.startswith(current_word)]

    return completions



if __name__ == "__main__":

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

    sys.exit(exit_code)