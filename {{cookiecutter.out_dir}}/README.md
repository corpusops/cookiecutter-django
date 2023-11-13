{%- set envs = ['dev', 'qa', 'staging', 'prod', 'preprod'] %}
{%- set aenvs = [] %}{%- for i in envs %}{% if cookiecutter.get(i+'_host', '')%}{% set _ = aenvs.append(i) %}{%endif%}{%endfor%}
{%- set refenv = aenvs|length > 1 and aenvs[-2] or aenvs[-1] %}
# Initialise your development environment
- Only now launch pycharm and configure a project on this working directory

All following commands must be run only once at project installation.


## First clone

```sh
git clone --recursive {{cookiecutter.git_project_url}}
{%if cookiecutter.use_submodule_for_deploy_code-%}git submodule init # only the fist time
git submodule update --recursive{%endif%}
```

## Before using any ansible command: a note on sudo
If your user is ``sudoer`` but is asking for you to input a password before elavating privileges,
You will need to add ``--ask-become-pass`` (or in earlier ansible versions: ``--ask-sudo-pass``) and maybe ``--become`` to any of the following ``ansible alike`` commands.


## Install corpusops
If you want to use ansible, or ansible vault (see passwords) or install docker via automated script
```sh
.ansible/scripts/download_corpusops.sh
.ansible/scripts/setup_corpusops.sh
```

## Install docker and docker compose
if you are under debian/ubuntu/mint/centos you can do the following:
```sh
local/*/bin/cops_apply_role --become \
    local/*/*/corpusops.roles/services_virt_docker/role.yml
```

... or follow official procedures for
  [docker](https://docs.docker.com/install/#releases) and
  [docker-compose](https://docs.docker.com/compose/install/).


## Update corpusops
You may have to update corpusops time to time with

```sh
./control.sh up_corpusops
```

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
git pull{% if cookiecutter.use_submodule_for_deploy_code
%}
git submodule init # only the fist time
git submodule update --recursive{%endif%}
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

## Launch app in foreground

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

## Run plain docker-compose commands

- Please remember that the ``CONTROL_COMPOSE_FILES`` env var controls which docker-compose configs are use (list of space separated files), by default it uses the dev set.

    ```sh
    ./control.sh dcompose <ARGS>
    ```

## Rebuild/Refresh local docker image in dev

```sh
./control.sh buildimages
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

## File permissions
If you get annoying file permissions problems on your host in development, you can use the following routine to (re)allow your host
user to use files in your working directory


```sh
./control.sh open_perms_valve
```

## Refresh Pipenv.lock

- Use

    ```
    ./control.sh usershell sh -ec "cd requirements && pipenv lock"
    ```

## Docker volumes

Your application extensivly use docker volumes. From times to times you may
need to erase them (eg: burn the db to start from fresh)

```sh
docker volume ls  # hint: |grep \$app
docker volume rm $id
```

## Reusing a precached image in dev to accelerate rebuilds
Once you have build once your image, you have two options to reuse your image as a base to future builds, mainly to accelerate buildout successive runs.

- Solution1: Use the current image as an incremental build: Put in your .env

    ```sh
    {{cookiecutter.app_type.upper()}}_BASE_IMAGE={{ cookiecutter.docker_image }}:latest-dev
    ```

- Solution2: Use a specific tag: Put in your .env

    ```sh
    {{cookiecutter.app_type.upper()}}_BASE_IMAGE=a tag
    # this <a_tag> will be done after issuing: docker tag registry.makina-corpus.net/mirabell/chanel:latest-dev a_tag
    ```

## Integrating an IDE
- <strong>DO NOT START YET YOUR IDE</strong>
- Start the stack, but specially stop the app container as you will
  have to separatly launch it wired to your ide

    ```sh
    ./control.sh up
    ./control.sh down {{cookiecutter.app_type}}
    ```

### Using pycharm

- Tips and tricks to know:
    - the python interpreter (or wrapper in our case) the pycharm glue needs should be named `python.*`
    - Paths mappings are needed, unless pycharm will execute in its own folder under `/opt` totally messing the setup
    - you should have the latest (2021-01-19) code of the common glue (`local/django-deploy-common`) for this to work
- Goto settings (CTRL-ALT-S)
    - Create a `docker-compose` python interpreter:
        - compose files: `docker-compose.yml`, `docker-compose-dev.yml`
        - python interpreter: `/code/sys/python-pycharm`
        - service: `django`
        - On project python interpreter settings page, set:
            - Path Mapping: Add with browsing your local:`src` , remote: `/code/src` <br/>
              (you should then see `<Project root>/src→/code/src`)
    - on language/frameworks → django
        - enable django support
        - set project root to `src` folder
        - set manage script to `manage.py`
        - browse to your `dev.py` settings file
    - Add a debug configuration
        - host: `0.0.0.0`

### fixes
- If there are errors when running debug sessions eg:

    ```
    django_1          | ModuleNotFoundError: No module named '_pydevd_bundle_ext'
    ```

    - stop your stack
    - stop pycharm
    - docker rmi all pycharm images (`docker images -a |grep -i pycharm`)
    - docker volume rm all pycharm volumes (`docker volume ls |grep -i pycharm`)
    - restart your stack (`./control.sh up`)
    - restart pycharm
    - edit your debug session and add/modify this envvar: `PYDEVD_USE_CYTHON=NO`
    - start a debug session
    - `docker exec -it <THEPYCHARCONTAINERID> bash` (`docker ps`)

        ```bash
        . /code/venv/bin/activate
        apt update && apt install $(cat /code/apt.txt)
        cd /opt/.pycharm_helpers/pydev
        rm -rf build
        python setup_cython.py build_ext --inplace
        ```
    - terminate the debug session in pycharm
    - edit your debug session and add/modify this envvar: `PYDEVD_USE_CYTHON=YES`
    - Congrats, your debug session env should be repaired


### Using VSCode

#### Get the completion and the code resolving for bundled dependencies wich are inside the container
- Whenever you rebuild the image, you need to refresh the files for your IDE to complete bundle dependencies

    ```sh
    ./control.sh get_container_code
    ```
#### IDE settings

- Add to your .env and re-run ``./control.sh build {{cookiecutter.app_type}}``

```sh
WITH VISUALCODE=1
```

```python
import pydevd_pycharm;pydevd_pycharm.settrace('host.docker.internal', port=12345, stdoutToServer=True, stderrToServer=True)
```
- if ``host.docker.internal`` does not work for you, you can replace it by the local IP of your machine.
- Remember this rules to insert your breakpoint:  If the file reside on your host, you can directly insert it, but on the other side, you will need to run a usershell session and debug from there.<br/>
  Eg: if  you want to put a pdb in ``../venv/*/*/*/foo/__init__.py``
    - <strong>DO NOT DO IT in ``local/code/venv/*/*/*/foo/__init__.py`` </strong>
    - do:

- You must launch VSCode using ``./control.sh vscode`` as vscode needs to have the ``PYTHONPATH`` variable preset to make linters work

    ```sh
    ./control.sh vscode
    ```
    - In other words, this add ``local/**/site-packages`` to vscode sys.path.


Additionnaly, adding this to ``.vscode/settings.json`` would help to give you a smooth editing experience

  ```json
  {
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/.git/subtree-cache/**": true,
        "**/node_modules/*/**": true,
        "**/local/*/**": true,
        "**/local/code/venv/lib/**/site-packages/**": false

      }
  }
  ```

#### Debugging with VSCode
- [vendor documentation link](https://code.visualstudio.com/docs/python/debugging#_remote-debugging)
- The VSCode process will connect to your running docker container, using a network tcp connection, eg on port ``5678``.
- ``5678`` can be changed but of course adapt the commands, this port must be reachable from within the container and in the ``docker-compose-dev.yml`` file.
- Ensure you added ``WITH_VSCODE`` in your ``.env`` and that ``VSCODE_VERSION`` is tied to your VSCODE installation and start from a fresh build if it was not (pip will mess to update it correctly, sorry).
- Wherever you have the need to break, insert in your code the following snippet after imports (and certainly before wherever you want your import):

    ```python
    import ptvsd;ptvsd.enable_attach(address=('0.0.0.0', 5678), redirect_output=True);ptvsd.wait_for_attach()
    ```
- Remember this rules to insert your breakpoint:  If the file reside on your host, you can directly insert it, but on the other side, you will need to run a usershell session and debug from there.<br/>
  Eg: if  you want to put a pdb in ``venv/*/*/*/foo/__init__.py``
    - <strong>DO NOT DO IT in ``local/code/venv/*/*/*/foo/__init__.py`` </strong>
    - do:

        ```sh
        ./control.sh down {{cookiecutter.app_type}}
        services_ports=1 ./control.sh usershell
        apt install -y vim
        vim ../venv/*/*/*/foo/__init__.py
        # insert: import ptvsd;ptvsd.enable_attach(address=('0.0.0.0', 5678), redirect_output=True);ptvsd.wait_for_attach()
        ./manage.py runserver 0.0.0.0:8000
        ```
- toggle a breakpoint on the left side of your text editor on VSCode.
- Switch to Debug View in VS Code, select the Python: Attach configuration, and select the settings (gear) icon to open launch.json to that configuration.<br/>
  Duplicate the remote attach part and edit it as the following

  ```json
  {
    "name": "Python Docker Attach",
    "type": "python",
    "request": "attach",
    "pathMappings": [
      {
        "localRoot": "${workspaceFolder}",
        "remoteRoot": "/code"
      }
    ],
    "port": 5678,
    "host": "localhost"
  }
  ```
- With VSCode and your configured debugging session, attach to the session and it should work



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
docker volume rm {{cookiecutter.lname}}-postgresql # check with docker volume ls
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


## Pipelines workflows tied to deploy environments and built docker images
### TL;DR
- We use deploy branches where some git **branches** are dedicated to deploy related **gitlab**, **configuration managment tool's environments**, and **docker images tags**.<br/>
- You can use them to deliver to a specific environment either by:
    1. Not using promotion workflow and only pushing to this branch and waiting for the whole pipeline to complete the image build, and then deploy on the targeted env.
    2. Using tags promotion: "Docker Image Promotion is the process of promoting Docker Images between registries to ensure that only approved and verified images are used in the right environments, such as production."<br/>
        - You **run or has run a successful pipeline with the code you want to deploy**, (surely ``{{cookiecutter.main_branch}}``).
        - You can then **``promote`` its tag** to either **one or all** env(s) with the ``promote_*`` jobs and reuse the previously produced tag.<br/>
        - After the succesful promotion, you can then manually **deploy on the targeted env(s)**.

### Using promotion in practice
- As an example, we are taking <br/>
  &nbsp;&nbsp;&nbsp;&nbsp;the ``{{refenv}}`` branch which is tied to <br/>
  &nbsp;&nbsp;&nbsp;&nbsp;the {{refenv}} **inventory ansible group**<br/>
  &nbsp;&nbsp;&nbsp;&nbsp;and deliver the {{refenv}} **docker image**<br/>
  &nbsp;&nbsp;&nbsp;&nbsp;and associated resources on the **{{refenv}} environment**.
- First, run an entire pipeline on the branch (eg:``{{cookiecutter.main_branch}}``)  and the commit you want to deploy.<br/>
  Please note that it can also be another branch like `stable` if `stable` branch was configured to produce the `stable` docker tags via the `TAGGUABLE_IMAGE_BRANCH` [`.gitlab-ci.yml`](./.gitlab-ci.yml) setting.
- Push your commit to the desired related env branche(s) (remove the ones you won't deploy now) to track the commit you are deploying onto

    ```sh
    # on local main branch
    git fetch --all
    git reset --hard origin/{{cookiecutter.main_branch}}
    git push --force origin{% for i in aenvs %} HEAD:{{i}}{%endfor %}
    ```
    1. Go to your gitab project ``pipelines`` section and immediately kill/cancel all launched pipelines.
    2. Find the killed pipeline on the environment (branch) you want to deploy onto (and if you don't have it, launch one via the ``Run pipeline`` button and **immediatly kill** it),<br/>
       Click on the ``canceled/running`` button link which links the pipeline details), <br/>
       It will lead to a jobs dashboard which is really appropriated to complete next steps.<br/>
       Either run:
        - ``promote_all_envs``: promote all deploy branches with the selected ``FROM_PROMOTE`` tag (see just below).
        - ``promote_single_env``: promote only this env with the selected ``FROM_PROMOTE`` tag (see just below).
        - Indeed, **in both jobs**, you can override the default promoted tag which is ``latest`` with the help of that ``FROM_PROMOTE`` pipeline/environment variable.<br/>
          This can help in those following cases:
            - If you want `production` to be deployed with the `dev` image, you can then set `FROM_PROMOTE=dev`.
            - If you want `dev` to be deployed with the `stable` image produced by the `stable` branch, you can then set `FROM_PROMOTE=stable`.
    3. Upon successful promotion, run the ``manual_deploy_$env`` job. (eg: ``manual_deploy_dev``)

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


# Teleport (load one env from one another)
init your vault (see [`docs/README.md`](./docs/README.md#docs#generate-vault-password-file))

```sh
CORPUSOPS_VAULT_PASSWORD="xxx" .ansible/scripts/setup_vaults.sh
.ansible/scripts/call_ansible.sh .ansible/playbooks/deploy_key_setup.yml
```


## Load a production database from old prod (standard modes)
```sh
.ansible/scripts/call_ansible.sh -vvvv .ansible/playbooks/teleport.yml \
    -e "{teleport_mode: standard, teleport_destination: controller, teleport_origin: {{cookiecutter.teleport_branch}}}"
```

## Load a production database from old prod (makinastates modes)
```sh
.ansible/scripts/call_ansible.sh -vvvv .ansible/playbooks/teleport.yml \
    -e "{teleport_mode: makinastates, teleport_destination: controller, teleport_origin: oldprod}"
```
