#!/bin/bash

set -x

if nox -s build; then
  set -e

  # Test our local changes before creating a tag
  nox -s format test

  # Deal with detached head state that Travis puts us in
  git checkout master

  # Change our Git username and email to not be Travis user
  git config --global user.name "Seth Michael Larson"
  git config --global user.email "sethmichaellarson@gmail.com"

  # Create a commit and tag with the date attached
  datetime=`date "+%Y-%-m-%-d"`
  version=`date "+%Y.%-m.%-d"`
  git add psl/
  git commit -m "Automated updates to the Public Suffix list on $datetime"
  git tag -a "$version" -m "$version"

  # Use our GitHub token to make the commit
  git remote rm origin
  git remote add origin https://sethmlarson:${GITHUB_TOKEN}@github.com/sethmlarson/psl > /dev/null 2>&1
  git push origin master --quiet --tags

  # Deploy our changes to PyPI
  nox -s deploy
fi
