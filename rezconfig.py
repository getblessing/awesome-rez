
import os


# Rez's default package path excluded
local_packages_path = "~/rez/packages/install"
release_packages_path = os.getenv("SHARE_RELEASE_PACKAGE_PATH",
                                  "~/rez/packages/release")
packages_path = [
    local_packages_path,
    release_packages_path,
]


allow_unversioned_packages = False
# If True, unversioned packages are allowed.
# Solve times are slightly better if this value is False.


package_preprocess_mode = "before"
# "before": Package's preprocess is executed before the global preprocess
# "after": Package's preprocess is executed after the global preprocess
# "override": Package's preprocess completely overrides the global preprocess


def package_preprocess_function(this, data):
    from rez.utils.formatting import PackageRequest
    from rez.exceptions import InvalidPackageError

    # Ozark profile
    # Must be built with ozark profile build tool
    #

    ozark_profile = getattr(this, "ozark_profile", False)
    if ozark_profile and not bool(os.getenv("REZ_OZARK_BUILD")):
        raise InvalidPackageError("This package is an Ozark profile, please "
                                  "use Ozark profile build tool instead.")

    # Must have variant
    #   Unless explicitly set `no_variant=True`
    #   Or it's the 'default' one
    #

    if this.name != "default":
        no_variants = getattr(this, "no_variants", False)

        if not no_variants and not this.variants:
            # Add "default" if no variant
            data["variants"] = [["default"]]

    # Replacing package requirements
    #

    REQUIREMENT_MAP = {
        # Example
        "installing_package_name": {
            "required_request_string": "replacement_request_string",
        },

    }
    if this.name in REQUIREMENT_MAP:

        remapped_requires = list()

        map_ = REQUIREMENT_MAP[this.name]
        for package in this.requires:

            if str(package) in map_:
                package = PackageRequest(map_[str(package)])

            elif package.name in map_:
                package = PackageRequest(map_[package.name])

            remapped_requires.append(package)

        data["requires"] = remapped_requires


platform_map = {
    "os": {
        r"windows-6.1(.*)": r"windows-7",
        r"windows-6.2(.*)": r"windows-8",
        r"windows-6.3(.*)": r"windows-8.1",
        r"windows-10(.*)": r"windows-10.0",
    },
}
