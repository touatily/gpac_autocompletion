"""
Module: cache_manager
This module provides a caching mechanism for the GPAC autocompletion script. 
It caches various GPAC components such as filters, modules, arguments, protocols, 
properties, and enum values to improve performance and reduce redundant command executions.
Classes:
    Cache: Manages the caching of GPAC command outputs.

The cache has this structure:
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
        enum_values: {
            "filter1": {dict of all enum values of filter1 args: value1=>arg1, value2=>arg2, ...},
            "filter2": {dict of all enum values of filter2 args: value1=>arg1, value2=>arg2, ...},
        }
    }
}
"""
import os
import json
import subprocess as sp
import re

class Cache:
    """
    A class to manage caching of GPAC autocomplete script.
    Attributes:
    -----------
    path : str
        The file path where the cache is stored.
    """
    def __init__(self, path: str):
        self.path = path
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as file:
                self.content = json.load(file)
        else:
            self.content = {"version": self.get_gpac_version(), "cache": {}}
            self.save()


    def save(self):
        """
        Save the cache content to the file.
        """
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.content, file, indent=4)


    def get_gpac_version(self)-> str|None:
        """
        Get the version of the GPAC binary.
        """
        result = sp.check_output(["gpac"], stderr=sp.STDOUT).decode()
        pattern = r".*version\s([\dA-Za-z\.\-]+).*"
        match = re.search(pattern, result)
        if match:
            return match.group(1)
        return None


    def get_cache_list_filters(self)-> list:
        """
        Get the list of filters from the cache.
        If the cache is not present or the version of GPAC has changed,
        then the list of filters is fetched from the GPAC binary.
        """
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
        temp = sp.check_output(["gpac", "-h", "filters"], stderr=sp.DEVNULL).decode()
        pattern = re.compile(r"\x1b\[32m([A-Za-z0-9]*):\x1b\[0m")
        self.content["cache"]["filters"] = pattern.findall(temp)
        self.save()
        return self.content["cache"]["filters"]


    def get_cache_list_modules(self)-> list:
        """
        Get the list of modules from the cache.
        If the cache is not present or the version of GPAC has changed,
        then the list of modules is fetched from the GPAC binary.
        """
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
        temp = sp.check_output(["gpac", "-h", "modules"], stderr=sp.DEVNULL).decode()
        pattern = re.compile(r"\x1b\[32m([A-Za-z0-9\.\_]*):\x1b\[0m")
        self.content["cache"]["modules"] = pattern.findall(temp)
        self.save()
        return self.content["cache"]["modules"]


    def get_cache_list_args(self, gfilter: str)-> dict:
        """
        Get the list of arguments of a filter from the cache.
        If the cache is not present or the version of GPAC has changed,
        then the list of arguments is fetched from the GPAC binary.
        """
        curr_version = self.get_gpac_version()
        if self.content["version"] == curr_version:
            if self.content.get("cache", None) is not None:
                if self.content["cache"].get("args", None) is not None:
                    if self.content["cache"].get("args", None).get(gfilter, None) is not None:
                        return self.content["cache"]["args"][gfilter]
                else:
                    self.content["cache"]["args"] = {}
            else:
                self.content["cache"] = {"args": {}}
        else:
            self.content = {
                "version": curr_version,
                "cache": {"args": {}}
            }
        temp = sp.check_output(["gpac", "-h", gfilter+".*", "-logs=ncl"], stderr=sp.DEVNULL).decode().strip("\n ").split("\n")
        self.content["cache"]["args"][gfilter] = {}
        pattern = re.compile(pattern = r"^(?P<arg_name>\w+)\s*\((?P<arg_type>\w+).*$")
        for line in temp:
            if len(line) > 0 and line[0] not in {' ', '-', '\t'}:
                res = pattern.match(line)
                if res:
                    self.content["cache"]["args"][gfilter][res.group('arg_name')] = res.group('arg_type')
        self.save()
        return self.content["cache"]["args"][gfilter]


    def get_cache_type_arg_filter(self, gfilter: str, arg: str)-> tuple:
        """
        Get the type and values of an argument of a filter from the cache.
        If the cache is not present or the version of GPAC has changed,
        then the type and values of the argument are fetched from the GPAC binary.
        """
        curr_version = self.get_gpac_version()
        if self.content["version"] == curr_version:
            if self.content.get("cache", None) is not None:
                if self.content["cache"].get("type_arg_filter", None) is not None:
                    if self.content["cache"]["type_arg_filter"].get(gfilter+"."+arg, None) is not None:
                        return self.content["cache"]["type_arg_filter"][gfilter+"."+arg]["type"], self.content["cache"]["type_arg_filter"][gfilter+"."+arg]["values"]
                else:
                    self.content["cache"]["type_arg_filter"] = {}
            else:
                self.content["cache"] = {"type_arg_filter": {}}
        else:
            self.content = {
                "version": curr_version,
                "cache": {"type_arg_filter": {}}
            }

        type_arg = None
        values = []
        if self.content["cache"].get("args", None) is None:
            if self.content["cache"]["args"].get(gfilter, None) is None:
                if self.content["cache"]["args"][gfilter].get(arg, None) is None:
                    type_arg = self.content["cache"]["args"][gfilter][arg]

        f_arg = f"{gfilter}.{arg}"
        if type_arg is not None and type_arg != "enum":
            self.content["cache"]["type_arg_filter"][f_arg] = {"type": type_arg, "values": values}
            self.save()
            return (type_arg, values)

        help_arg = sp.check_output(["gpac", "-h", f_arg], stderr=sp.DEVNULL).decode()
        pattern = re.compile(pattern = rf"^\x1b\[32m{arg}\x1b\[0m\s*\((?P<type>[^,\)]+)[,\)]")
        res_match = pattern.match(help_arg)
        if res_match:
            type_arg = res_match.group('type')
        if type_arg == "enum":
            pattern = re.compile(r"\x1b\[33m([A-Za-z0-9]+)\x1b\[0m\:")
            values = pattern.findall(help_arg)
        self.content["cache"]["type_arg_filter"][f_arg] = {"type": type_arg, "values": values}
        self.save()
        return (type_arg, values)


    def get_cache_list_protocols(self)-> dict:
        """
        Get the list of protocols from the cache.
        If the cache is not present or the version of GPAC has changed,
        then the list of protocols is fetched from the GPAC binary.
        """
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

        temp = sp.check_output(["gpac", "-ha", "protocols", "-logs=ncl"], stderr=sp.DEVNULL).decode().strip("\n").split("\n")[1:]
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


    def get_cache_list_props(self)-> list:
        """
        Get the list of properties from the cache.
        If the cache is not present or the version of GPAC has changed,
        then the list of properties is fetched from the GPAC binary.
        """
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

        temp = sp.check_output(["gpac", "-h", "props"], stderr=sp.DEVNULL).decode()
        pattern = re.compile(r"\x1b\[32m([A-Z][A-Za-z]*)\x1b\[0m")
        self.content["cache"]["props"] = pattern.findall(temp)
        self.save()
        return self.content["cache"]["props"]


    def get_cache_list_values_enum_args(self, gfilter: str)-> dict:
        """
        Retrieve the list of enum values for arguments of a specified filter from the cache.
        If the cache is absent or the GPAC version has changed, recalculate the enum values.
        Duplicate values are removed.
        """
        current_version = self.get_gpac_version()
        if self.content["version"] == current_version:
            if self.content.get("cache", None) is not None:
                if self.content["cache"].get("enum_values", None) is not None:
                    if self.content["cache"]["enum_values"].get(gfilter, None) is not None:
                        return self.content["cache"]["enum_values"][gfilter]
                else:
                    self.content["cache"]["enum_values"] = {}
            else:
                self.content["cache"] = {"enum_values": {}}
        else:
            self.content = {
                "version": current_version,
                "cache": {"enum_values": {}}
            }

        dict_args = self.get_cache_list_args(gfilter)
        list_args_enum = [e for e in dict_args if dict_args[e] == "enum"]
        duplicate = set()
        ans = {}
        for arg in list_args_enum:
            _, values = self.get_cache_type_arg_filter(gfilter, arg)
            for value in values:
                if value not in duplicate:
                    if ans.get(value, None) is not None:
                        duplicate.add(value)
                        del ans[value]
                    elif value not in dict_args:
                        ans[value] = arg

        self.content["cache"]["enum_values"][gfilter] = ans
        self.save()
        return ans
