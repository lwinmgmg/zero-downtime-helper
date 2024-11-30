import os
import re
import sys
from typing import List
pattern = '#{5}(\r\n|\r|\n|.)+#{5}'
ips = ["server:8080", "server1:8080"]

DEFAULT_FILENAME = "app.conf"
STR_FORMATTER = """#####
upstream backend {{
    least_conn;
    {data}
}}
#####"""

# Environments
DEFAULT_HOSTS = "DEFAULT_HOSTS"
TEMP_HOSTS = "TEMP_HOSTS"
FILENAME = "FILENAME"

class FindAndReplace:
    def __init__(self):
        self.default_hosts = os.environ.get(DEFAULT_HOSTS)
        self.temp_hosts = os.environ.get(TEMP_HOSTS)
        self.filename = os.environ.get(FILENAME) or DEFAULT_FILENAME
        self.file_path = f"data/{self.filename}"
        self.validated = False

    def validate(self):
        if not self.default_hosts:
            raise Exception(f"{DEFAULT_HOSTS} env is required")
        if not self.temp_hosts:
            raise Exception(f"{TEMP_HOSTS} env is required")
        self.validated = True

    @property
    def default_str(self):
        return self.format_replace_str(self.default_hosts.split(","))
    
    @property
    def temp_str(self):
        return self.format_replace_str(self.temp_hosts.split(","))

    @classmethod
    def format_replace_str(cls, data_list: List[str]):
        return STR_FORMATTER.format(data="\n    ".join([f"server {data};" for data in data_list]))

    def restore(self):
        if self.validated:
            output: str
            with open(self.file_path, 'r') as rfile:
                output = re.sub(pattern, self.default_str, rfile.read())
            with open(self.file_path, 'w') as wfile:
                wfile.write(output)

    def replace(self):
        if self.validated:
            output: str
            with open(self.file_path, 'r') as file:
                output = re.sub(pattern, self.temp_str, file.read())
            with open(self.file_path, 'w') as wfile:
                wfile.write(output)

if __name__ == "__main__":
    app = FindAndReplace()
    app.validate()
    idx = sys.argv.index("-t")
    if idx + 1 < len(sys.argv):
        if sys.argv[idx+1] == "replace":
            app.replace()
        elif sys.argv[idx+1] == "restore":
            app.restore()
