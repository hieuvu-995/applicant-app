#!/bin/sh

# Use Black Python to format codebase
black -t py36 . --exclude=management-api-common
