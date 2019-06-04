"""A setuptools based setup module for omnisci renderers"""
# To use a consistent encoding
from codecs import open
from os import path
import sys
from subprocess import check_call
from setuptools import find_packages, setup, Command
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.bdist_egg import bdist_egg
from distutils import log

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Create setuptools commands for installing extensions


def run(cmd, *args, **kwargs):
    """Echo a command before running it. Defaults to repo as cwd"""
    from shlex import quote
    log.info('> ' + ' '.join(map(quote, cmd)))
    kwargs.setdefault('cwd', here)
    kwargs.setdefault('shell', sys.platform == 'win32')
    if not isinstance(cmd, list):
        cmd = cmd.split()
    return check_call(cmd, *args, **kwargs)


class BaseCommand(Command):
    """Empty command for custom commands to subclass"""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def get_inputs(self):
        return []

    def get_outputs(self):
        return []


class InstallJupyterWidgets(BaseCommand):
    description = 'Install jupyter-widgets extension for JupyterLab'

    def run(self):
        run(['jupyter', 'labextension', 'install',
             '@jupyter-widgets/jupyterlab-manager', '--no-build'])


class InstallJupyterOmnisci(BaseCommand):
    description = 'Install jupyterlab-omnisci extension for JupyterLab'

    def run(self):
        run(['jupyter', 'labextension', 'install',
             'jupyterlab-omnisci', '--no-build'])


class bdist_egg_disabled(bdist_egg):
    """Disabled version of bdist_egg
    Prevents setup.py install performing setuptools' default easy_install,
    which it should never ever do.
    """

    def run(self):
        sys.exit(
            "Aborting implicit building of eggs. Use `pip install .` to install from source.")


def install_labextension(command):
    class DecoratedCommand(command):
        def run(self):
            command.run(self)
            self.distribution.run_command(
                'install_jupyter_widgets_labextension')
            self.distribution.run_command('install_labextension')
    return DecoratedCommand


setup(
    name="jupyterlab-omnisci",  # Required
    version="0.9.0",  # Required
    description="Omnisci integration with JupyterLab",  # Required
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/Quansight/jupyterlab-omnisci",  # Optional
    packages=find_packages(),
    install_requires=[
        "pymapd",
        "jupyterlab==1.0.0a3",
        "pyyaml",
        "ibis-framework==1.0.0",
        "altair==3.0.1",
        "vega_datasets",
        "ipywidgets",
        "vdom"
    ],
    cmdclass={
        'install_jupyter_widgets_labextension': InstallJupyterWidgets,
        'install_labextension': InstallJupyterOmnisci,
        'build_py': install_labextension(build_py),
        'egg_info': install_labextension(egg_info),
        'sdist': install_labextension(sdist),
        'develop': install_labextension(develop),
        'bdist_egg': bdist_egg if 'bdist_egg' in sys.argv else bdist_egg_disabled
    }
)
