
import os
import sys
import json
import subprocess
from gitz import git

# Ensure Rez is reachable
try:
    subprocess.check_output(["rez-build", "-h"])
except OSError:
    print("Rez not found. Is rez bin in $PATH ?")
    sys.exit(1)

# GitHub repository inventory
with open("inventory.json", "r") as inventory:
    pkg_repos = json.load(inventory)

# Cache installed package family names
installed_packages = set(
    subprocess.check_output(
        ["rez-search"],
        universal_newlines=True
    ).split()
)


def is_installed(name):
    return name in installed_packages


def git_build(data, release=False):
    name = data["rez_name"]
    if is_installed(name):
        # This deploy script currently meant for fresh install, not for
        # version update. So no versions check.
        print("Rez package %s exists, skipping." % name)
        return

    def _git_build(build_options):
        git.build(data["git_url"],
                  clone_dst=data["name"],
                  install=True,
                  release=release,
                  build_options=build_options)

    print("Installing %s .." % name)

    setups_json = "setups/%s.json" % name
    if os.path.isfile(setups_json):
        # The requirement was listed by `rez-context --so`
        with open(setups_json, "r") as fp:
            setups = json.load(fp)

        print("  has setups...")
        for arg in setups:
            for dep_pkg in arg["requires"]:
                git_build(pkg_repos[dep_pkg], release)

            _git_build(build_options=arg["options"])

    else:
        _git_build(build_options=None)

    installed_packages.add(name)


def deploy_package(names, release=False):
    for data in [pkg_repos[n] for n in names]:
        git_build(data, release)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("packages", nargs="*",
                        help="Package names to deploy.")
    parser.add_argument("--release", action="store_true",
                        help="Deploy to package releasing location.")

    opt = parser.parse_args()

    deploy_package(opt.packages, opt.release)

    print("=" * 30)
    print("SUCCESS!\n")
