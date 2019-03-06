# Initialise your development environment

All following commands must be run only once at project installation.


## First clone

```sh
git clone --recursive {{cookiecutter.git_project_url}}
{%-if cookiecutter.use_submodule_for_deploy_code%}git submodule init --recursive  # only the fist time
git submodule upate{%endif%}
```

## Install docker and docker compose

if you are under debian/ubuntu/mint/centos you can do the following:

```sh
.ansible/scripts/download_corpusops.sh
.ansible/scripts/setup_corpusops.sh
local/*/bin/cops_apply_role --become \
    local/*/*/corpusops.roles/services_virt_docker/role.yml
```

... or follow official procedures for
  [docker](https://docs.docker.com/install/#releases) and
  [docker-compose](https://docs.docker.com/compose/install/).


## Update corpusops
You may have to update corpusops time to time with
￼
```
./control.sh up_corpusops
```
￼
## Configuration

Use the wrapper to init configuration files from their ``.dist`` counterpart
and adapt them to your needs.

```bash
./control.sh init
```

**Hint**: You may have to add `0.0.0.0` to `ALLOWED_HOSTS` in `local.py`.

## Login to the app docker registry

You need to login to our docker registry to be able to use it:


```bash
docker login {{cookiecutter.docker_registry}}  # use your gitlab user
```

{%- if cookiecutter.registry_is_gitlab_registry %}
**⚠️ See also ⚠️** the
    [project docker registry]({{cookiecutter.git_project_url.replace('ssh://', 'https://').replace('git@', '')}}/container_registry)
{%- else %}
**⚠️ See also ⚠️** the makinacorpus doc in the docs/tools/dockerregistry section.
{%- endif%}

# Use your development environment

## Update submodules

Never forget to grab and update regulary the project submodules:

```sh
git pull
{%-if cookiecutter.use_submodule_for_deploy_code%}git submodule init --recursive  # only the fist time
git submodule upate{%endif%}
```

## Control.sh helper

You may use the stack entry point helper which has some neat helpers but feel
free to use docker command if you know what your are doing.

```bash
./control.sh usage # Show all available commands
```

## Start the stack

After a last verification of the files, to run with docker, just type:

```bash
# First time you download the app, or sometime to refresh the image
./control.sh pull # Call the docker compose pull command
./control.sh up # Should be launched once each time you want to start the stack
```

## Launch app as foreground

```bash
./control.sh fg
```

**⚠️ Remember ⚠️** to use `./control.sh up` to start the stack before.

## Start a shell inside the {{cookiecutter.app_type}} container

- for user shell

    ```sh
    ./control.sh usershell
    ```
- for root shell

    ```sh
    ./control.sh shell
    ```

**⚠️ Remember ⚠️** to use `./control.sh up` to start the stack before.

## Rebuild/Refresh local docker image in dev

```sh
control.sh buildimages
```

## Running heavy session
Like for installing and testing packages without burning them right now in requirements.<br/>
You will need to add the network alias and maybe stop the django worker

```sh
./control.sh stop {{cookiecutter.app_type}}
services_ports=1 ./control.sh usershell
./manage.py runserserver 0.0.0.0:8000
```

## Calling Django manage commands

```sh
./control.sh manage [options]
# For instance:
# ./control.sh manage migrate
# ./control.sh manage shell
# ./control.sh manage createsuperuser
# ...
```

**⚠️ Remember ⚠️** to use `./control.sh up` to start the stack before.

## Run tests

```sh
./control.sh tests
# also consider: linting|coverage
```

**⚠️ Remember ⚠️** to use `./control.sh up` to start the stack before.

## Docker volumes

Your application extensivly use docker volumes. From times to times you may
need to erase them (eg: burn the db to start from fresh)

```sh
docker volume ls  # hint: |grep \$app
docker volume rm $id
```

## Doc for deployment on environments
- [See here](./docs/README.md)

## FAQ

If you get troubles with the nginx docker env restarting all the time, try recreating it :

```bash
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d --no-deps --force-recreate nginx backup
```

If you get the same problem with the django docker env :

```bash
docker-compose -f docker-compose.yml -f docker-compose-dev.yml stop django db
docker volume rm oppm-postgresql # check with docker volume ls
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d db
# wait fot postgis to be installed
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up django
```

## Django settings managment
- We embrace many concepts to manage django settings
    - 12Factors: we try to make system environment the primary sources of settings
    - For hosted environments, we use ByEnv pythonic settings that extends prod and
      leverage complexity of combining settings by allowing to write logic to factorize the needed glue
- The layout and variable precedence is as-follow:
    - ``settings.base``
    - ``environ (DJANGO__* variables)``: every environment var that has that prefix will be exposed
      as a django setting (without the prefix).<br/>
      For example ``DJANGO__SECRET_KEY`` ➡️ ``SECRET_KEY``
    - ``settings.base.{dev,test,prod}``
    - ``settings.base.instances{dev,qa,staging,prod,...}``
- So where do you need to put your settings ?
    - **Generic env values**:
        - The default form needs to be, even with a null value (``[]``, ``0``, ``None``, ``{}``) in ``settings/base.py``.
        - If you need a specific value for ``dev envs (localhost)`` or ``test (ci)``, you can put in in ``settings/{dev/test}.py``.
        - If the production value is the same for every one, you can make it vary in ``settings/prod.py``.
    - **Hosted env values**: If the value has to vary on a specific, hosted env. <br/>Say that you need ``'prod.foo.com'`` in prod but the default value
      everywhere else, you need to put your settings in  ``settings/instances/prod.py``.
    - If the value is exposed on the environment, whenever you add/edit it, you need to add it
        - to ``docker.env`` & ``docker.env.dist`` in dev
        - To **ansible setup**, [Read this section of the ansible readme](./docs/README.md#django-settings-setup).

{% if cookiecutter.with_celery %}
## Celery

Celery can be used in foreground for easy developement<br/>
Open two shell windows.<br/>

In one of them, launch the beat
```sh
./control.sh celery_beat_fg
```

In the other, launch one worker
```sh
./control.sh celery_worker_fg
```


{% endif %}
