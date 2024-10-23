import os 
import json
import subprocess
import re

# structure of the cache file
"""
content = {
    "version": "version_of_gpac_associated_with_cache_content",
    "cache": {
        "filters": [list of all filters],
        "args": {
            "filter1": {dict of all args for filter1 => arg1: type1, arg2: type2, ...},
            "filter2": {dict of all args for filter2 => arg1: type1, arg2: type2, ...},
            ...
        },
        "modules": [list of all modules],
        "type_arg_filter": {
            "filter1.arg1": {
                "type": "type_of_arg1",
                "values": [list of all values for arg1 of filter1],
            },
            "filter2.arg2": {
                "type": "type_of_arg2",
                "values": [list of all values for arg2 of filter2],
            },
            ...
        },
        "protocols": {
            protocol1: {
                "input": [list of all input filters for protocol1],
                "output": [list of all output filters for protocol1],
            },
            protocol2: {
                "input": [list of all input filters for protocol2],
                "output": [list of all output filters for protocol2],
            },
            ...
        },
        props: [list of all properties],
}
"""

class cache:
    def __init__(self, path: str):
        import os
        self.path = path
        if os.path.isfile(path):
            with open(path, "r") as file:
                self.content = json.load(file)
        else:
            self.content = {"version": self.get_gpac_version(), "cache": {}}
            self.save()


    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as file:
            json.dump(self.content, file, indent=4)


    def get_gpac_version(self):
        result = subprocess.check_output(["gpac"], stderr=subprocess.STDOUT).decode().replace("\n", " ")
        pattern = r'.*version\s([\dA-Za-z\.\-]+).*'
        match = re.search(pattern, result)
        if match:
            return match.group(1)
        else:
            return None


    def get_cache_list_filters(self):
        current_version = self.get_gpac_version()
        if self.content["version"] == current_version:
            if self.content.get("cache", None) is not None:
                if self.content["cache"].get("filters", None) is not None:
                    return self.content["cache"]["filters"]
            else:
                self.content["cache"] = {}
        else:
            self.content = {
                "version": current_version,
                "cache": {}
            }
        temp = subprocess.check_output(["gpac", "-h", "filters"], stderr=subprocess.DEVNULL).decode()
        pattern = re.compile('\\x1b\[32m([A-Za-z]*):\\x1b\[0m')
        self.content["cache"]["filters"] = pattern.findall(temp)
        self.save()
        return self.content["cache"]["filters"]


    def get_cache_list_modules(self):
        current_version = self.get_gpac_version()
        if self.content["version"] == current_version:
            if self.content.get("cache", None) is not None:
                if self.content["cache"].get("modules", None) is not None:
                    return self.content["cache"]["modules"]
            else:
                self.content["cache"] = {}
        else:
            self.content = {
                "version": current_version,
                "cache": {}
            }
        temp = subprocess.check_output(["gpac", "-h", "modules"], stderr=subprocess.DEVNULL).decode()
        pattern = re.compile('\\x1b\[32m([A-Za-z0-9\.\_]*):\\x1b\[0m')
        self.content["cache"]["modules"] = pattern.findall(temp)
        self.save()
        return self.content["cache"]["modules"]


    def get_cache_list_args(self, filter: str):
        curr_version = self.get_gpac_version()
        if self.content["version"] == curr_version:
            if self.content.get("cache", None) is not None:
                if self.content["cache"].get("args", None) is not None:
                    if self.content["cache"].get("args", None).get(filter, None) is not None:
                        return self.content["cache"]["args"][filter]
                else:
                    self.content["cache"]["args"] = {}
            else:
                self.content["cache"] = {"args": {}}
        else:
            self.content = {
                "version": curr_version,
                "cache": {"args": {}}
            }
        temp = subprocess.check_output(["gpac", "-h", filter+".*", "-logs=ncl"], stderr=subprocess.DEVNULL).decode().strip("\n ").split("\n")
        self.content["cache"]["args"][filter] = {}
        pattern = re.compile(pattern = r"^(?P<arg_name>\w+)\s*\((?P<arg_type>\w+).*$")
        for line in temp:
            if len(line) > 0 and line[0] not in {' ', '-', '\t'}:
                res = pattern.match(line)
                if res:
                    self.content["cache"]["args"][filter][res.group('arg_name')] = res.group('arg_type')
                    
        self.save()
        return self.content["cache"]["args"][filter]
    

    def get_cache_type_arg_filter(self, filter: str, arg: str)-> tuple:
        curr_version = self.get_gpac_version()
        if self.content["version"] == curr_version:
            if self.content.get("cache", None) is not None:
                if self.content["cache"].get("type_arg_filter", None) is not None:
                    if self.content["cache"]["type_arg_filter"].get(filter+"."+arg, None) is not None:
                        return self.content["cache"]["type_arg_filter"][filter+"."+arg]["type"], self.content["cache"]["type_arg_filter"][filter+"."+arg]["values"]
                else:
                    self.content["cache"]["type_arg_filter"] = {}
            else:
                self.content["cache"] = {"type_arg_filter": {}}
        else:
            self.content = {
                "version": curr_version,
                "cache": {"type_arg_filter": {}}
            }

        type = None; values = []
        if self.content["cache"].get("args", None) is None:
            if self.content["cache"]["args"].get(filter, None) is None:
                if self.content["cache"]["args"][filter].get(arg, None) is None:
                    type = self.content["cache"]["args"][filter][arg]

        if type is not None and type != "enum":
            self.content["cache"]["type_arg_filter"][filter+"."+arg] = {"type": type, "values": values}
            self.save()
            return (type, values)

        help_arg = subprocess.check_output(["gpac", "-h", filter+"."+arg], stderr=subprocess.DEVNULL).decode()
        pattern = re.compile(pattern = f"^\\x1b\[32m{arg}\\x1b\[0m\s*\(([^,\)]+)[,\)]")
        res_match = pattern.match(help_arg)
        if res_match:
            type = res_match.group(1)
        if type == "enum":
            pattern = re.compile('\\x1b\[33m([A-Za-z0-9]+)\\x1b\[0m\:')
            values = pattern.findall(help_arg)
        self.content["cache"]["type_arg_filter"][filter+"."+arg] = {"type": type, "values": values}
        self.save()
        return (type, values)
    

    def get_cache_list_protocols(self):
        current_version = self.get_gpac_version()
        if self.content["version"] == current_version:
            if self.content.get("cache", None) is not None:
                if self.content["cache"].get("protocols", None) is not None:
                    return self.content["cache"]["protocols"]
                else:
                    self.content["cache"]["protocols"] = {}
            else:
                self.content["cache"] = {"protocols": {}}
        else:
            self.content = {
                "version": current_version,
                "cache": {"protocols": {}}
            }

        temp = subprocess.check_output(["gpac", "-ha", "protocols", "-logs=ncl"], stderr=subprocess.DEVNULL).decode().strip("\n").split("\n")[1:]
        pattern = re.compile(r'(?P<protocol>\w+):(?:\s*in\s*\((?P<in_filters>[^\)]*)\))?(?:\s*out\s*\((?P<out_filters>[^\)]*)\))?')
        for line in temp:
            match = pattern.match(line)
            if match:
                protocol = match.group('protocol')
                in_filters = match.group('in_filters')
                out_filters = match.group('out_filters')
                self.content["cache"]["protocols"][protocol] = {"input": in_filters.split(", ") if in_filters else [], "output": out_filters.split(", ") if out_filters else []}

        self.save()
        return self.content["cache"]["protocols"]
    

    def get_cache_list_props(self):
        current_version = self.get_gpac_version()
        if self.content["version"] == current_version:
            if self.content.get("cache", None) is not None:
                if self.content["cache"].get("props", None) is not None:
                    return self.content["cache"]["props"]
                else:
                    self.content["cache"]["props"] = []
            else:
                self.content["cache"] = {"props": []}
        else:
            self.content = {
                "version": current_version,
                "cache": {"props": []}
            }

        temp = subprocess.check_output(["gpac", "-h", "props"], stderr=subprocess.DEVNULL).decode()
        pattern = re.compile('\\x1b\[32m([A-Z][A-Za-z]*)\\x1b\[0m')
        self.content["cache"]["props"] = pattern.findall(temp)
        self.save()
        return self.content["cache"]["props"]

