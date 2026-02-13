from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item(
    (
        "common-env-features",
        """
"SKIP_EMAIL_VALIDATION": true 
"ENABLE_BULK_ENROLLMENT_VIEW": true 
"ALLOW_PUBLIC_ACCOUNT_CREATION": false 
"ENABLE_CHANGE_USER_PASSWORD_ADMIN": true 
"SHOW_REGISTRATION_LINKS" : false 
"DEFAULT_COURSE_VISIBILITY_IN_CATALOG": "none"
"COURSES_ARE_BROWSABLE": true
"CERTIFICATES_HTML_VIEW": true
"CUSTOM_CERTIFICATE_TEMPLATES_ENABLED": true
"ENABLE_ENTERPRISE_INTEGRATION": true
"""
    )
)


# DISABLE_UNENROLLMENT


from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-dockerfile-post-python-requirements",
        """
# Bulk user import dependencies
RUN pip install --no-cache-dir django-import-export==4.4.0
RUN pip install --no-cache-dir git+https://github.com/ac-2025-sep/bulk_user_import.git
"""
    )
)


hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        """
# Bulk user CSV import (Django admin)
INSTALLED_APPS += [
    "import_export",
    "bulk_user_import",
]
""",
    )
)


from tutormfe.hooks import PLUGIN_SLOTS

PLUGIN_SLOTS.add_items([
    (
        "learner-dashboard",
        "desktop_user_menu_slot",
        """
        {
          op: PLUGIN_OPERATIONS.Insert,
          widget: {
            id: 'add_user_link_desktop',
            type: DIRECT_PLUGIN,
            RenderWidget: () => {
              const cfg = (globalThis?.getConfig?.() || {});
              const fallbackLms = 'https://edx.mysleepwell.com';
              const base = (cfg.LMS_BASE_URL || fallbackLms).replace(/\\/$/, '');
              const url = `${base}/admin/auth/user/`;

              return (
                <a className="dropdown-item" href={url}>
                  Add User
                </a>
              );
            },
          },
        }
        """
    ),
])




































# import os
# from glob import glob

# import click
# import importlib_resources
# from tutor import hooks

# from .__about__ import __version__

# ########################################
# # CONFIGURATION
# ########################################

# hooks.Filters.CONFIG_DEFAULTS.add_items(
#     [
#         # Add your new settings that have default values here.
#         # Each new setting is a pair: (setting_name, default_value).
#         # Prefix your setting names with 'STAQO_LMS_PLUGIN_'.
#         ("STAQO_LMS_PLUGIN_VERSION", __version__),
#     ]
# )

# hooks.Filters.CONFIG_UNIQUE.add_items(
#     [
#         # Add settings that don't have a reasonable default for all users here.
#         # For instance: passwords, secret keys, etc.
#         # Each new setting is a pair: (setting_name, unique_generated_value).
#         # Prefix your setting names with 'STAQO_LMS_PLUGIN_'.
#         # For example:
#         ### ("STAQO_LMS_PLUGIN_SECRET_KEY", "{{ 24|random_string }}"),
#     ]
# )

# hooks.Filters.CONFIG_OVERRIDES.add_items(
#     [
#         # Danger zone!
#         # Add values to override settings from Tutor core or other plugins here.
#         # Each override is a pair: (setting_name, new_value). For example:
#         ### ("PLATFORM_NAME", "My platform"),
#     ]
# )


# ########################################
# # INITIALIZATION TASKS
# ########################################

# # To add a custom initialization task, create a bash script template under:
# # create_bulk_user/templates/staqo-lms-plugin/tasks/
# # and then add it to the MY_INIT_TASKS list. Each task is in the format:
# # ("<service>", ("<path>", "<to>", "<script>", "<template>"))
# MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
#     # For example, to add LMS initialization steps, you could add the script template at:
#     # create_bulk_user/templates/staqo-lms-plugin/tasks/lms/init.sh
#     # And then add the line:
#     ### ("lms", ("staqo-lms-plugin", "tasks", "lms", "init.sh")),
# ]


# # For each task added to MY_INIT_TASKS, we load the task template
# # and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# # run it as part of the `init` job.
# for service, template_path in MY_INIT_TASKS:
#     full_path: str = str(
#         importlib_resources.files("create_bulk_user")
#         / os.path.join("templates", *template_path)
#     )
#     with open(full_path, encoding="utf-8") as init_task_file:
#         init_task: str = init_task_file.read()
#     hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


# ########################################
# # DOCKER IMAGE MANAGEMENT
# ########################################


# # Images to be built by `tutor images build`.
# # Each item is a quadruple in the form:
# #     ("<tutor_image_name>", ("path", "to", "build", "dir"), "<docker_image_tag>", "<build_args>")
# hooks.Filters.IMAGES_BUILD.add_items(
#     [
#         # To build `myimage` with `tutor images build myimage`,
#         # you would add a Dockerfile to templates/staqo-lms-plugin/build/myimage,
#         # and then write:
#         ### (
#         ###     "myimage",
#         ###     ("plugins", "staqo-lms-plugin", "build", "myimage"),
#         ###     "docker.io/myimage:{{ STAQO_LMS_PLUGIN_VERSION }}",
#         ###     (),
#         ### ),
#     ]
# )


# # Images to be pulled as part of `tutor images pull`.
# # Each item is a pair in the form:
# #     ("<tutor_image_name>", "<docker_image_tag>")
# hooks.Filters.IMAGES_PULL.add_items(
#     [
#         # To pull `myimage` with `tutor images pull myimage`, you would write:
#         ### (
#         ###     "myimage",
#         ###     "docker.io/myimage:{{ STAQO_LMS_PLUGIN_VERSION }}",
#         ### ),
#     ]
# )


# # Images to be pushed as part of `tutor images push`.
# # Each item is a pair in the form:
# #     ("<tutor_image_name>", "<docker_image_tag>")
# hooks.Filters.IMAGES_PUSH.add_items(
#     [
#         # To push `myimage` with `tutor images push myimage`, you would write:
#         ### (
#         ###     "myimage",
#         ###     "docker.io/myimage:{{ STAQO_LMS_PLUGIN_VERSION }}",
#         ### ),
#     ]
# )


# ########################################
# # TEMPLATE RENDERING
# # (It is safe & recommended to leave
# #  this section as-is :)
# ########################################

# hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
#     # Root paths for template files, relative to the project root.
#     [
#         str(importlib_resources.files("create_bulk_user") / "templates"),
#     ]
# )

# hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
#     # For each pair (source_path, destination_path):
#     # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
#     # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
#     # For example, ``create_bulk_user/templates/staqo-lms-plugin/build``
#     # will be rendered to ``$(tutor config printroot)/env/plugins/staqo-lms-plugin/build``.
#     [
#         ("staqo-lms-plugin/build", "plugins"),
#         ("staqo-lms-plugin/apps", "plugins"),
#     ],
# )


# ########################################
# # PATCH LOADING
# # (It is safe & recommended to leave
# #  this section as-is :)
# ########################################

# # For each file in create_bulk_user/patches,
# # apply a patch based on the file's name and contents.
# for path in glob(str(importlib_resources.files("create_bulk_user") / "patches" / "*")):
#     with open(path, encoding="utf-8") as patch_file:
#         hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


# ########################################
# # CUSTOM JOBS (a.k.a. "do-commands")
# ########################################

# # A job is a set of tasks, each of which run inside a certain container.
# # Jobs are invoked using the `do` command, for example: `tutor local do importdemocourse`.
# # A few jobs are built in to Tutor, such as `init` and `createuser`.
# # You can also add your own custom jobs:


# # To add a custom job, define a Click command that returns a list of tasks,
# # where each task is a pair in the form ("<service>", "<shell_command>").
# # For example:
# ### @click.command()
# ### @click.option("-n", "--name", default="plugin developer")
# ### def say_hi(name: str) -> list[tuple[str, str]]:
# ###     """
# ###     An example job that just prints 'hello' from within both LMS and CMS.
# ###     """
# ###     return [
# ###         ("lms", f"echo 'Hello from LMS, {name}!'"),
# ###         ("cms", f"echo 'Hello from CMS, {name}!'"),
# ###     ]


# # Then, add the command function to CLI_DO_COMMANDS:
# ## hooks.Filters.CLI_DO_COMMANDS.add_item(say_hi)

# # Now, you can run your job like this:
# #   $ tutor local do say-hi --name="Abhay Chauhan"


# #######################################
# # CUSTOM CLI COMMANDS
# #######################################

# # Your plugin can also add custom commands directly to the Tutor CLI.
# # These commands are run directly on the user's host computer
# # (unlike jobs, which are run in containers).

# # To define a command group for your plugin, you would define a Click
# # group and then add it to CLI_COMMANDS:


# ### @click.group()
# ### def staqo-lms-plugin() -> None:
# ###     pass


# ### hooks.Filters.CLI_COMMANDS.add_item(staqo-lms-plugin)


# # Then, you would add subcommands directly to the Click group, for example:


# ### @staqo-lms-plugin.command()
# ### def example_command() -> None:
# ###     """
# ###     This is helptext for an example command.
# ###     """
# ###     print("You've run an example command.")


# # This would allow you to run:
# #   $ tutor staqo-lms-plugin example-command
