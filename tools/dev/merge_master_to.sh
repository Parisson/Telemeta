#!/bin/sh

git checkout $1
git merge master
git checkout master

