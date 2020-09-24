
import os
import sys
import logging
import subprocess


PY3 = sys.version_info[0] == 3
log = logging.getLogger("gitz")


def clone(url, dst, branch=None, single_branch=True):
    # https://stackoverflow.com/a/4568323/14054728

    args = ["git", "clone"]

    if branch:
        args.extend(["-b", branch])

    if single_branch:
        args.append("--single-branch")

    args.extend([url, dst])

    subprocess.check_output(args)


def get_branch(repository):
    branch = subprocess.check_output(["git", "branch"], cwd=repository)
    if PY3:
        branch = branch.decode()

    return branch[len("* "):].strip()


def append_breadcrumb(package_py, branch):
    with open(package_py, "a") as f:
        f.write("gitz = True\n")
        f.write("gitz_from_branch = '%s'\n" % branch)


def build(opt, tempdir):

    clone(opt.url, dst=tempdir, branch=opt.branch)

    branch = get_branch(tempdir)
    log.info("Cloned branch: [%s]" % branch)

    package_py = os.path.join(tempdir, "package.py")
    if not os.path.isfile(package_py):
        raise Exception("Rez package.py not found")

    append_breadcrumb(package_py, branch)

    # build

    if opt.release:
        args = ["rez-release"]
    else:
        args = ["rez-build"]
        if opt.install:
            args.append("--install")

    args.extend(opt.build_options or [])

    subprocess.check_output(args, cwd=tempdir)
