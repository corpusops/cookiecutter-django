#!/bin/bash
set -e
THISSCRIPT=$0
W="$(dirname $(readlink -f $0))"

SHELL_DEBUG=${SHELL_DEBUG-${SHELLDEBUG}}
if  [[ -n $SHELL_DEBUG ]];then set -x;fi

shopt -s extglob

APP={{cookiecutter.app_type}}
APP_USER=${APP_USER:-${APP}}
APP_CONTAINER=${APP_CONTAINER:-${APP}}
DEBUG=${DEBUG-}
NO_BACKGROUND=${NO_BACKGROUND-}
BUILD_PARALLEL=${BUILD_PARALLEL:-1}
BUILD_CONTAINERS="$APP_CONTAINER{%-if cookiecutter.remove_cron%} cron{%endif%}"
EDITOR=${EDITOR:-vim}
DIST_FILES_FOLDERS=". src/*/settings"
CONTROL_COMPOSE_FILES="${CONTROL_COMPOSE_FILES:-docker-compose.yml docker-compose-dev.yml}"
COMPOSE_COMMAND=${COMPOSE_COMMAND:-docker-compose}

set_dc() {
    local COMPOSE_FILES="${@:-${CONTROL_COMPOSE_FILES}}"
    DC="${COMPOSE_COMMAND}"
    for i in $COMPOSE_FILES;do
        DC="${DC} -f $i"
    done
    DCB="$DC -f docker-compose-build.yml"
}

log(){ echo "$@">&2;}

vv() { log "$@";"$@";}

dvv() { if [[ -n $DEBUG ]];then log "$@";fi;"$@";}

_shell() {
    local container="$1" user="$2"
    shift;shift
    local bargs="$@"
    set -- dvv $DC \
        run --rm --no-deps --service-ports \
        -e TERM=$TERM -e COLUMNS=$COLUMNS -e LINES=$LINES \
        -u $user $container bash
    if [[ -n "$bargs" ]];then
        set -- $@ -c "$bargs"
    fi
    "$@"
}

#  usershell $user [$args]: open shell inside container as \$APP_USER
do_usershell() { _shell $APP_CONTAINER $APP_USER $@;}

#  shell [$args]: open root shell inside \$APP_CONTAINER
do_shell()     { _shell $APP_CONTAINER root      $@;}

#  install_docker: install docker and docker-compose on ubuntu
do_install_docker() {
    vv .ansible/scripts/download_corpusops.sh
    vv .ansible/scripts/setup_corpusops.sh
    vv local/*/bin/cops_apply_role --become \
        local/*/*/corpusops.roles/services_virt_docker/role.yml
}

#  pull [$args]: pull stack container images
do_pull() {
    vv $DC pull $@
}

#  up [$args]: start stack
do_up() {
    local bars=$@
    set -- vv $DC up
    if [[ -z $NO_BACKGROUND ]];then bargs="-d $bargs";fi
    $@ $bargs
}

#  down [$args]: down stack
do_down() {
    local bargs=$@
    set -- vv $DC down
    $@ $bargs
}

#  stop [$args]: stop
do_stop() {
    local bargs=$@
    set -- vv $DC stop
    $@ $bargs
}

#  stop_containers [$args]: stop containers (app_container by default)
stop_containers() {
    for i in ${@:-$APP_CONTAINER};do $DC stop $i;done
}

#  fg: launch app container in foreground (using entrypoint)
do_fg() {
    stop_containers
    vv $DC run --rm --no-deps --service-ports $APP_CONTAINER $@
}

#  build [$args]: rebuild app containers ($BUILD_CONTAINERS)
do_build() {
    local bargs="$@" bp=""
    if [[ -n $BUILD_PARALLEL ]];then
        bp="--parallel"
    fi
    set -- vv $DCB build $bp
    if [[ -z "$bargs" ]];then
        for i in $BUILD_CONTAINERS;do
            $@ $i
        done
    else
        $@ $bargs
    fi
}

#  buildimages: alias for build
do_buildimages() {
    do_build "$@"
}

#  build_images: alias for build
do_build_images() {
    do_build "$@"
}

#  usage: show this help
do_usage() {
    echo "$0:"
    # Show autodoc help
    awk '{ if ($0 ~ /^#[^!]/) { \
                gsub(/^#/, "", $0); print $0 } }' "$THISSCRIPT"
    echo " Defaults:
        \$BUILD_CONTAINERS (default: $BUILD_CONTAINERS)
        \$APP_CONTAINER: (default: $APP_CONTAINER)
        \$APP_USER: (default: $APP_USER)
    "
}

#  init: copy base configuration files from defaults if not existing
do_init() {
    for d in  $( \
        find $DIST_FILES_FOLDERS -mindepth 1 -maxdepth 1 -name "*.dist" -type f )
    do
        i="$(dirname $d)/$(basename $d .dist)"
        if [ ! -e $i ];then
            cp -fv "$d" "$i"
        else
            if ! ( diff -Nu "$d" "$i" );then
                echo "Press enter to continue";read -t 120
            fi
        fi
        $EDITOR $i
    done
}

#  yamldump [$file]: dump yaml file with anchors resolved
do_yamldump() {
    local bargs=$@
    if [ -e local/corpusops.bootstrap/venv/bin/activate ];then
        . local/corpusops.bootstrap/venv/bin/activate
    fi
    set -- .ansible/scripts/yamldump.py
    $@ $bargs
}

# {{cookiecutter.app_type.upper()}} specific
#  python: enter python interpreter
do_python() {
    do_usershell ../venv/bin/python $@
}

#  manage [$args]: run manage.py commands
do_manage() {
    do_python manage.py $@
}

#  runserver [$args]: launch app container in foreground (using {{cookiecutter.app_type}} runserver)
do_runserver() {
    local bargs=${@:-0.0.0.0:8000}
    stop_containers
    do_shell \
    ". ../venv/bin/activate
    && ./manage.py migrate
    && ./manage.py runserver $bargs"
}

do_run_server() { do_runserver $@; }

#  tests [$tests]: run tests
do_test() {
    local bargs=${@:-tests}
    stop_containers
    set -- vv do_shell \
        "chown {{cookiecutter.app_type}} ../.tox
        && gosu {{cookiecutter.app_type}} ../venv/bin/tox -c ../tox.ini -e $bargs"
    "$@"
}

do_tests() { do_test $@; }

#  linting: run linting tests
do_linting() { do_test linting; }

#  coverage: run coverage tests
do_coverage() { do_test coverage; }

do_main() {
    local args=${@:-usage}
    local actions="shell|usage|install_docker|setup_corpusops"
    actions="$actions|yamldump|stop|usershell"
    actions="$actions|init|up|fg|pull|build|buildimages|down"
    actions_{{cookiecutter.app_type}}="runserver|tests|test|coverage|linting|manage|python"
    actions="@($actions|$actions_{{cookiecutter.app_type}})"
    action=${1-}
    if [[ -n $@ ]];then shift;fi
    set_dc
    case $action in
        $actions) do_$action $@;;
        *) do_usage;;
    esac
}
cd "$W"
do_main "$@"
