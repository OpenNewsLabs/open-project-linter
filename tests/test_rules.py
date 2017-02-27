#!/usr/bin/env python3
""" Automated tests for openlinter.rules using pytest. Run from the
openlinter root directory with

$ pytest tests/test_rules.py
"""

import pytest
import git

from openlinter.rules import *

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

def test_detect_version_control_repository_exists():
    result = detect_version_control('tests/fixtures/test-git-repo')
    assert result == 'git'

def test_detect_version_control_folder_does_not_exist():
    assert detect_version_control('zzyzx') is None

def test_detect_version_control_folder_has_no_vc():
    result = detect_version_control('tests/fixtures/pic-folder')
    assert result is None


# Tests for openlinter.rules.check_multiple_branches()

def test_check_multiple_branches_empty_repo():
    assert check_multiple_branches('tests/fixtures/test-git-repo') == False

def test_check_multiple_branches_nonexistent_repo():
    with pytest.raises(git.InvalidGitRepositoryError):
        check_multiple_branches('tests/fixtures/pic-folder')

def test_check_multiple_branches_nonexistent_repo():
    with pytest.raises(git.NoSuchPathError):
        check_multiple_branches('zzyzx')

def test_check_multiple_branches_repo_with_one_branch():
    result = check_multiple_branches('tests/fixtures/git-repo-one-branch')
    assert result == False

def test_check_multiple_branches_repo_with_two_branches():
    result = check_multiple_branches('tests/fixtures/git-repo-dev-branch')
    assert result == True


# Tests for openlinter.rules.check_for_develop_branch()

def test_check_for_develop_branch_nonexistent_repo():
    with pytest.raises(git.NoSuchPathError):
        check_for_develop_branch('zzyzx', 'dev')

def test_check_for_develop_branch_nonexistent_repo():
    with pytest.raises(git.InvalidGitRepositoryError):
        check_for_develop_branch('tests/fixtures/pic-folder', 'dev')

def test_check_for_develop_branch_repo_without_dev_branch():
    result = check_for_develop_branch('tests/fixtures/test-git-repo', 'dev')
    assert result == False

def test_check_for_develop_branch_repo_has_dev_branch():
    result = check_for_develop_branch('tests/fixtures/git-repo-dev-branch',
       'develop')
    assert result == True


# Tests for openlinter.rules.check_for_multiple_commits()

def test_check_for_multiple_commits_nonexistent_repo():
    with pytest.raises(git.NoSuchPathError):
        check_for_multiple_commits('zzyzx')

def test_check_for_multiple_commits_nonexistent_repo():
    with pytest.raises(git.InvalidGitRepositoryError):
        check_for_multiple_commits('tests/fixtures/pic-folder')

def test_check_for_multiple_commits_no_commits():
    result = check_for_multiple_commits('tests/fixtures/test-git-repo')
    assert result is False

def test_check_for_multiple_commits_one_commit():
    result = check_for_multiple_commits('tests/fixtures/git-repo-one-branch')
    assert result == False

def test_check_for_multiple_commits_two_commits():
    result = check_for_multiple_commits('tests/fixtures/git-repo-dev-branch')
    assert result == True
