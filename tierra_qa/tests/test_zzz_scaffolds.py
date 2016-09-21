# -*- coding: utf-8 -*-

""" This module contains the tests for the tierra_qa clone feature.

A clean virtualenv is created, a package created from tierra_qa and
the tests of that package are run.

Because the is potentially really time consuming the scaffolding tests
are marked with ``slow`` and are not run unless ``py.test`` is invoked with the
``--runslow`` option.

The module name starts with ``test_zzz`` to make the contained tests always the
last in a complete test run.

Thanks to:
*  https://github.com/Kotti/Kotti/blob/master/kotti/tests/test_zzz_scaffolds.py
"""

import os
import shutil
import subprocess
import sys
from copy import copy
from tempfile import mkdtemp

from pytest import fixture
from pytest import mark

slow = mark.slow


@fixture
def virtualenv(request, travis):
    """ Create a virtualenv and ``chdir`` into it.  Remove it and ``chdir``
    into the previous working directory again when the test has been run.
    """

    with travis.folding_output():
        import virtualenv
        from virtualenv import Logger

        # create a temp directory
        cwd = os.getcwd()
        virtualenv_directory = mkdtemp()

        # install a virtualenv
        logger = Logger([(Logger.level_for_integer(2), sys.stdout)])
        virtualenv.logger = logger
        virtualenv.create_environment(
            virtualenv_directory,
            site_packages=False,
            clear=True,
            unzip_setuptools=True)

        # chdir into the virtualenv directory
        os.chdir(virtualenv_directory)

        # update setuptools in the virtualenv
        subprocess.check_call([
            os.path.join('bin', 'pip'),
            'install', '-U', 'pip', 'wheel', 'setuptools', ])

        # create a local copy of the environment, where we can override
        # VIRTUAL_ENV to make pip-accel work
        env = copy(os.environ)
        env.update({'VIRTUAL_ENV': virtualenv_directory, })

        # install requirements.txt into the virtualenv
        subprocess.check_call([
            os.path.join('bin', 'pip'),
            'install', '-r',
            os.path.join(cwd, 'requirements.txt')],
            env=env)

        # setuptools-git is required to be able to call setup.py install
        # sucessfully.  also install psycopg2 and oursql.
        subprocess.check_call([
            os.path.join('bin', 'pip'),
            'install', 'setuptools-git'],
            env=env)

        shutil.copytree(cwd, os.path.join(virtualenv_directory, 'tierra_qa'))

        # install tierra_qa into the virtualenv
        os.chdir('tierra_qa')
        subprocess.check_call([
            os.path.join('..', 'bin', 'python'), 'setup.py', 'develop'])
        os.chdir('..')

    def delete_virtualenv():
        shutil.rmtree(virtualenv_directory)
        os.chdir(cwd)

    request.addfinalizer(delete_virtualenv)


@slow
def test_scaffold_tierra_qa(virtualenv, travis, splinter_webdriver):

    with travis.folding_output():

        # clone a project from the scaffold
        subprocess.check_call([
            os.path.join('bin', 'tierra_qa_clone'),
            'dummy_qa'])

        # develop the package
        os.chdir('dummy_qa')
        subprocess.check_call([
            os.path.join('..', 'bin', 'python'),
            'setup.py', 'develop'])

        # run the tests
        subprocess.check_call([
            os.path.join('..', 'bin', 'py.test'),
            '--splinter-webdriver', splinter_webdriver,
            '--variables', 'credentials_template.yml'])


@slow
def test_scaffold_tierra_qa_clone_translate():
    """ Assert if internal _translate has been called with right input """
    import mock
    with mock.patch('tierra_qa.scripts._translate') as mock_translate:
        with mock.patch('tierra_qa.scripts._optparse_args') as mock_optparse:
            from tierra_qa.scripts import tierra_qa_clone
            mock_optparse.return_value = [{}, ['new_name']]
            tierra_qa_clone()
            mock_translate.assert_called_once_with('new_name')


@slow
def test_scaffold_tierra_qa_clone_translate_noinput():
    """ Assert if internal _translate has not been called without required
        parameters
    """
    import mock
    with mock.patch('tierra_qa.scripts._translate') as mock_translate:
        with mock.patch('tierra_qa.scripts._optparse_args') as mock_optparse:
            from tierra_qa.scripts import tierra_qa_clone
            mock_optparse.return_value = [{}, []]
            tierra_qa_clone()
            assert not mock_translate.called


@slow
def test_scaffold_tierra_qa_clone_translate_nomock(tmpdir):
    """ _translate call should replicate tierra_qa structure """
    import os
    import mock
    previous_path = os.getcwd()
    os.chdir(tmpdir.strpath)
    try:
        with mock.patch('tierra_qa.scripts._optparse_args') as mock_optparse:
            from tierra_qa.scripts import tierra_qa_clone
            mock_optparse.return_value = [{}, ['new_name1']]
            tierra_qa_clone()
    finally:
        os.chdir(previous_path)
