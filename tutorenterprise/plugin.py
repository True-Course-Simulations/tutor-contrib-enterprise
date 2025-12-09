import importlib.resources as importlib_resources
import os
from glob import glob

from tutor import hooks

from .__about__ import __version__

PACKAGE_NAME = "tutorenterprise"


########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        ("ENTERPRISE_VERSION", __version__),
        ("ENTERPRISE_USER", "enterprise"),
    ]
)


########################################
# TEMPLATE RENDERING
########################################
templates_dir = str(importlib_resources.files(PACKAGE_NAME) / "templates")
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(templates_dir)
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("enterprise/apps", "plugins"),
        ("enterprise/build", "plugins"),
    ]
)


########################################
# INITIALIZATION TASKS
########################################
hooks_dir = (
    importlib_resources.files(PACKAGE_NAME)
    / "templates"
    / "enterprise"
    / "tasks"
)
task_path = hooks_dir / "lms" / "init"
with open(task_path, encoding="utf-8") as task_file:
    hooks.Filters.CLI_DO_INIT_TASKS.add_item(("lms", task_file.read()))


########################################
# PATCH LOADING
########################################
patches_dir = importlib_resources.files(PACKAGE_NAME) / "patches"
for path in glob(str(patches_dir / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
