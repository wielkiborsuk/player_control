#!/bin/bash

DIR="$(dirname "$(readlink -f "$0")")"

. "$DIR"/venv/bin/activate

cd "$DIR"

python __main__.py "$@"

