
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
try:
    installed_packages = set(
        subprocess.check_output(
            ["rez-search"],
            universal_newlines=True,
            stderr=subprocess.DEVNULL,
        ).split()
    )
except subprocess.CalledProcessError:
    installed_packages = set()


def is_installed(name):
    return name in installed_packages


def bind_os(release=False):
    if is_installed("os"):
        return

    if release:
        subprocess.check_call(["rez-bind", "--release", "os"])
    else:
        subprocess.check_call(["rez-bind", "os"])

    installed_packages.add("os")


def install_rez(release=False):
    if is_installed("rez"):
        return

    if release:
        subprocess.check_call(["rez-release"], cwd="rezpkg")
    else:
        subprocess.check_call(["rez-build", "--install"], cwd="rezpkg")

    installed_packages.add("rez")


def git_build(data, release=False):
    name = data["rez_name"]
    if is_installed(name):
        # This deploy script currently meant for fresh install, not for
        # version update. So no versions check.
        print("Rez package %s exists, skipping." % name)
        return

    def _git_build(build_options):
        git.build(data["clone_url"],
                  clone_dst="build/%s" % data["name"],
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
    # Installing essential packages
    # os, arch, platform
    bind_os(release)
    # rez itself as  package
    install_rez(release)
    # default, for packages that has no variants
    git_build(pkg_repos["default"], release)
    # python
    git_build(pkg_repos["python"], release)
    # rezcore, for building other rez packages
    git_build(pkg_repos["rezcore"], release)
    # rezutil, for building other rez packages
    git_build(pkg_repos["rezutil"], release)
    # pipz, for pypi packages
    git_build(pkg_repos["pipz"], release)

    # Installing demand packages
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
