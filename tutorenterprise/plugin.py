import importlib.resources as importlib_resources
import os
from glob import glob

from tutor import hooks

from .__about__ import __version__

PACKAGE_NAME = "tutorenterprise"


########################################
# CONFIGURATION
########################################
hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Secret for the enterprise backend service OAuth client
        ("ENTERPRISE_BACKEND_SERVICE_EDX_OAUTH2_SECRET", "{{ 8|random_string }}"),
    ]
)

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        ("ENTERPRISE_VERSION", __version__),
        ("ENTERPRISE_USER", "enterprise"),
        # OAuth client id for the enterprise backend service
        ("ENTERPRISE_BACKEND_SERVICE_EDX_OAUTH2_KEY", "enterprise-backend-service-key"),
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


########################################
# MFE APPS
########################################
from tutormfe.hooks import MFE_APPS

@MFE_APPS.add()
def add_enterprise_mfes(mfes):
    # Enterprise Admin Portal
    mfes["admin-portal"] = {
        #"repository": "https://github.com/openedx/frontend-app-admin-portal.git",
        "repository": "https://github.com/True-Course-Simulations/frontend-app-admin-portal.git", # Added Company fork to work on fixing some config issues 
        "port": 8734,
        #"version": "master",
        "version": "fix/admin-portal-runtime-config",
    }

    # Enterprise Learner Portal
    mfes["learner-portal-enterprise"] = {
        "repository": "https://github.com/openedx/frontend-app-learner-portal-enterprise.git",
        "port": 8735,
        "version": "master",
    }

    return mfes