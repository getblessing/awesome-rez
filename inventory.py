
import sys
import json


PY3 = sys.version_info[0] == 3
if PY3:
    import urllib.request as urllib
else:
    import urllib2 as urllib


def fetch_pkg_repos():
    per_page = 100  # currently we have 84 repos
    api_url = "https://api.github.com/users"
    org_url = "%s/getblessing/repos?per_page=%d" % (api_url, per_page)

    pkg_repos = dict()
    pkg_prefix = "rez-"

    result = urllib.urlopen(org_url)
    for repo in json.loads(result.read()):
        is_public = not (repo["archived"] or repo["private"])
        name = repo["name"]
        if name.startswith(pkg_prefix) and is_public:
            data = {
                key: repo[key] for key in [
                    "url",
                    "clone_url",
                    "html_url",
                    "full_name",
                    "name",
                ]
            }
            rez_name = name[len(pkg_prefix):]
            data["rez_name"] = rez_name
            pkg_repos[rez_name] = data

    return pkg_repos


if __name__ == "__main__":
    with open("inventory.json", "w") as inventory:
        json.dump(fetch_pkg_repos(), inventory, indent=4)
