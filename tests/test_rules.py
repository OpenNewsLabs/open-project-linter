#!/usr/bin/env python3
""" Automated tests for openlinter.rules using pytest. Run from the
openlinter root directory with

$ pytest tests/test_rules.py
"""

import pytest
import git

from openlinter.rules import *


# Test fixtures

@pytest.fixture()
def setup_empty_repo(tmpdir):
    # tmpdir is a LocalPath, git chokes unless you cast to str
    git.Repo.init(str(tmpdir))

@pytest.fixture()
def setup_repo_one_br_one_commit(tmpdir):
    repo = git.Repo.init(str(tmpdir))
    # Make temporary file for the temporary repo
    with open(str(tmpdir.join('test_file.txt')), 'w') as f:
        f.write('This is a file with text.\n')
    repo.index.add([str(tmpdir.join('test_file.txt'))])
    repo.index.commit('initial commit')

@pytest.fixture()
def setup_repo_two_br_two_commits(tmpdir):
    repo = git.Repo.init(str(tmpdir))
    # Make first temporary file and commit it
    with open(str(tmpdir.join('test_file.txt')), 'w') as f:
        f.write('This is a file with text.\n')
    repo.index.add([str(tmpdir.join('test_file.txt'))])
    repo.index.commit('initial commit')

    # Make second temporary file and commit it
    with open(str(tmpdir.join('test_file2.txt')), 'w') as f:
        f.write('This is a second file with text.\n')
    repo.index.add([str(tmpdir.join('test_file2.txt'))])
    repo.index.commit('second commit')

    # Make the dev branch
    new_branch = repo.create_head('develop')


# Tests for openlinter.rules.check_file_presence()

def test_check_file_presence_nonexistent_file():
    assert check_file_presence('zzyzx', 'tests/fixtures') == False

def test_check_file_presence_empty_file():
    result = check_file_presence('empty_file.txt', 'tests/fixtures')
    assert result == None

def test_check_file_presence_existing_file():
    result = check_file_presence('file_with_text.txt', 'tests/fixtures')
    assert result == True


# Tests for openlinter.rules.check_for_file_content()

def test_check_for_file_content_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        check_for_file_content('zzyzx')

def test_check_for_file_content_file_has_content():
    assert check_for_file_content('tests/fixtures/file_with_text.txt') is True

def test_check_for_file_content_empty_file():
    assert check_for_file_content('tests/fixtures/empty_file.txt') is False


# Tests for openlinter.rules.check_for_code()
# Cases not tested: code exists, structured text that is not "code" exists

def test_check_for_code_empty_dir():
    assert check_for_code('tests/fixtures/emptydir') == False

def test_check_for_code_nonexistent_dir():
    assert check_for_code('zzyzyx') == False

def test_check_for_code_only_non_text_files_exist():
    assert check_for_code('tests/fixtures/pic-folder/kitten_pic.jpg') == False


# Tests for openlinter.rules.get_file_text()

def test_get_file_text_undecodable():
    result = get_file_text('tests/fixtures/pic-folder/kitten_pic.jpg')
    assert result is None

def test_get_file_text_file_does_not_exist():
    with pytest.raises(FileNotFoundError):
        get_file_text('zzyzx')

def test_get_file_text_file_exists_has_text():
    result = get_file_text('tests/fixtures/file_with_text.txt')
    assert result == 'This is a file with content.\n'


# Tests for openlinter.rules.detect_version_control()

def test_detect_version_control_repository_exists(setup_empty_repo, tmpdir):
    result = detect_version_control(str(tmpdir))
    assert result == 'git'

def test_detect_version_control_folder_does_not_exist():
    assert detect_version_control('zzyzx') is None

def test_detect_version_control_folder_has_no_vc():
    result = detect_version_control('tests/fixtures/pic-folder')
    assert result is None


# Tests for openlinter.rules.check_multiple_branches()

def test_check_multiple_branches_empty_repo(setup_empty_repo, tmpdir):
    assert check_multiple_branches(str(tmpdir)) == False

def test_check_multiple_branches_nonexistent_repo():
    with pytest.raises(git.InvalidGitRepositoryError):
        check_multiple_branches('tests/fixtures/pic-folder')

def test_check_multiple_branches_nonexistent_folder():
    with pytest.raises(git.NoSuchPathError):
        check_multiple_branches('zzyzx')

def test_check_multiple_branches_repo_one_branch(setup_repo_one_br_one_commit, tmpdir):
    result = check_multiple_branches(str(tmpdir))
    assert result == False

def test_check_multiple_branches_repo_with_two_branches(setup_repo_two_br_two_commits, tmpdir):
    result = check_multiple_branches(str(tmpdir))
    assert result == True


# Tests for openlinter.rules.check_for_develop_branch()

def test_check_for_develop_branch_nonexistent_folder():
    with pytest.raises(git.NoSuchPathError):
        check_for_develop_branch('zzyzx', 'dev')

def test_check_for_develop_branch_nonexistent_repo():
    with pytest.raises(git.InvalidGitRepositoryError):
        check_for_develop_branch('tests/fixtures/pic-folder', 'dev')

def test_check_for_develop_branch_repo_without_dev_branch(setup_empty_repo, tmpdir):
    result = check_for_develop_branch(str(tmpdir), 'develop')
    assert result == False

def test_check_for_develop_branch_repo_has_dev_branch(setup_repo_two_br_two_commits, tmpdir):
    result = check_for_develop_branch(str(tmpdir),
       'develop')
    assert result == True


# Tests for openlinter.rules.check_for_multiple_commits()

def test_check_for_multiple_commits_nonexistent_folder():
    with pytest.raises(git.NoSuchPathError):
        check_for_multiple_commits('zzyzx')

def test_check_for_multiple_commits_nonexistent_repo():
    with pytest.raises(git.InvalidGitRepositoryError):
        check_for_multiple_commits('tests/fixtures/pic-folder')

def test_check_for_multiple_commits_no_commits(setup_empty_repo, tmpdir):
    result = check_for_multiple_commits(str(tmpdir))
    assert result is False

def test_check_for_multiple_commits_one_commit(setup_repo_one_br_one_commit, tmpdir):
    result = check_for_multiple_commits(str(tmpdir))
    assert result == False

def test_check_for_multiple_commits_two_commits(setup_repo_two_br_two_commits, tmpdir):
    result = check_for_multiple_commits(str(tmpdir))
    assert result == True
