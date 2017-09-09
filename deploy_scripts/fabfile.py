from fabric.api import env, run, local
from fabric.contrib.files import exists

REPO_URL = 'git@github.com:alamastor/udacity-catalog.git'


def deploy():
    site_dir = f'~/sites/{env.host}'
    _make_site_dir(site_dir)
    _get_latest_source(site_dir)
    _update_virtualenv(site_dir)


def _make_site_dir(site_dir):
    if not exists(site_dir):
        run(f'mkdir -p {site_dir}')


def _get_latest_source(site_dir):
    if exists(f'{site_dir}/.git'):
        run(f'cd {site_dir} && git fetch')
    else:
        run(f'git clone {REPO_URL} {site_dir}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {site_dir} && git reset --hard {current_commit}')


def _update_virtualenv(site_dir):
    venv_dir = site_dir + '/venv'
    if not exists(venv_dir + '/bin/pip'):
        run(f'python3 -m venv {venv_dir}')
    run(f'{venv_dir}/bin/pip install -r {site_dir}/requirements.txt')
