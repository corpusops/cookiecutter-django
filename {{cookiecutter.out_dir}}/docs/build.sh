#!/usr/bin/env bash
set -e
set -o pipefail

if [ "x${SDEBUG-}" != "x" ];then set -x;fi
readlinkf() {
    if ( uname | egrep -iq "darwin|bsd" );then
        if ( which greadlink 2>&1 >/dev/null );then
            greadlink -f "$@"
        elif ( which perl 2>&1 >/dev/null );then
            perl -MCwd -le 'print Cwd::abs_path shift' "$@"
        elif ( which python 2>&1 >/dev/null );then
            python -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' "$@"
        fi
    else
        readlink -f "$@"
    fi
}
cd $(dirname $(readlinkf $0))/..
{% if cookiecutter.with_sphinx %}
SPHINX_IMAGE="${SPHINX_IMAGE:-sphinxdoc/sphinx}"
SPHINX_PYTHON="${SPHINX_PYTHON:-python}"
SPHINX_MP="${SPHINX_MP:-/docs}"
SPHINX_WD="${SPHINX_WD:-$SPHINX_MP/docs}"
t=$(docker build -q -f docs/Dockerfile \
    --build-arg SPHINX_PYTHON=$SPHINX_PYTHON \
    --build-arg SPHINX_IMAGE=$SPHINX_IMAGE \
    .)
cmd="${@-make html}"
printf "${cmd}\n" \
    | docker run --rm -i -u $(id -u) \
    -v "$(pwd):$SPHINX_MP" \
    -w "$SPHINX_WD" \
    --entrypoint bash $t -ex
{% endif%}
# vim:set et sts=4 ts=4 tw=80:
