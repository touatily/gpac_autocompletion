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
        "options": {
            "filter1": [list of all options for filter1],
            "filter2": [list of all options for filter2],
            ...
        },
        "modules": [list of all modules],
        "type_option_filter": {
            "filter1.option1": {
                "type": "type_of_option1",
                "values": [list of all values for option1 of filter1],
            },
            "filter2.option2": {
                "type": "type_of_option2",
                "values": [list of all values for option2 of filter2],
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
        }
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
        temp = subprocess.check_output(["gpac", "-h", "filters", "-logs=ncl"], stderr=subprocess.DEVNULL).decode().strip("\n ").split("\n")[1:]
        self.content["cache"]["filters"] = [e.split(":")[0] for e in temp]
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
        temp = subprocess.check_output(["gpac", "-logs=ncl", "-h", "modules"], stderr=subprocess.DEVNULL).decode().strip("\n ").split("\n")[1:]
        self.content["cache"]["modules"] = [e.split(":")[0] for e in temp]
        self.save()
        return self.content["cache"]["modules"]


    def get_cache_list_options(self, filter: str):
        curr_version = self.get_gpac_version()
        if self.content["version"] == curr_version:
            if self.content.get("cache", None) is not None:
                if self.content["cache"].get("options", None) is not None:
                    if self.content["cache"].get("options", None).get(filter, None) is not None:
                        return self.content["cache"]["options"][filter]
                else:
                    self.content["cache"]["options"] = {}
            else:
                self.content["cache"] = {"options": {}}
        else:
            self.content = {
                "version": curr_version,
                "cache": {"options": {}}
            }
        temp = subprocess.check_output(["gpac", "-h", filter+".*", "-logs=ncl"], stderr=subprocess.DEVNULL).decode().strip("\n ").split("\n")
        self.content["cache"]["options"][filter] = [e.split(" ")[0] for e in temp if e!="" and e[0] not in {' ', '-'} and e[0]!= "\t"]
        self.save()
        return self.content["cache"]["options"][filter]
    

    def get_cache_type_option_filter(self, filter: str, option: str)-> tuple:
        curr_version = self.get_gpac_version()
        if self.content["version"] == curr_version:
            if self.content.get("cache", None) is not None:
                if self.content["cache"].get("type_option_filter", None) is not None:
                    if self.content["cache"]["type_option_filter"].get(filter+"."+option, None) is not None:
                        return self.content["cache"]["type_option_filter"][filter+"."+option]["type"], self.content["cache"]["type_option_filter"][filter+"."+option]["values"]
                else:
                    self.content["cache"]["type_option_filter"] = {}
            else:
                self.content["cache"] = {"type_option_filter": {}}
        else:
            self.content = {
                "version": curr_version,
                "cache": {"type_option_filter": {}}
            }

        help_option = subprocess.check_output(["gpac", "-h", filter+"."+option, "-logs=ncl"], stderr=subprocess.DEVNULL).decode().strip("\n ").split("\n")
        pattern = re.compile(pattern = fr"^{option}\s*\(([^,\)]+)[,\)]")
        type = ""; values = []
        if pattern.match(help_option[0]):
            type = pattern.match(help_option[0]).group(1)
        if type == "enum":
            values = [e.strip('\t* ').split(':')[0] for e in help_option[1:] if e!='']
        self.content["cache"]["type_option_filter"][filter+"."+option] = {"type": type, "values": values}
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

