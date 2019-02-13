#!/usr/bin/env bash

git add .
git commit -m "$1"
git push github master

cd ../alice2-y
git add .
git commit -m "$1"
git push github master

cd ../professor-y
git add .
git commit -m "$1"
git push github master

cd ../rosie-y
git add .
git commit -m "$1"
git push github master

cd ../servusai-y
git add .
git commit -m "$1"
git push github master

cd ../talk-y
git add .
git commit -m "$1"
git push github master

cd ../template-y
git add .
git commit -m "$1"
git push github master

cd ../traintimes-y
git add .
git commit -m "$1"
git push github master

cd ../y-bot
git add .
git commit -m "$1"
git push github master

cd ../wiki-y
git add .
git commit -m "$1"
git push github master
