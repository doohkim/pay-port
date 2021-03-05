#!/usr/bin/env python

import os
import subprocess
from pathlib import Path

DOCKER_ID = 'johnkdo2021'
DOCKER_IMAGE_NAME = 'pay-port'
DOCKER_IMAGE_TAG = f'{DOCKER_ID}/{DOCKER_IMAGE_NAME}'
DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-d', ''),
    ('-p', '80:80'),
    # ('-p', '443:443'),
    ('--name', 'pay-port'),
    # ('-v', '/etc/letsencrypt:/etc/letsencrypt'),
]

USER = 'ubuntu'
HOST = '13.125.1.183'
TARGET = f'{USER}@{HOST}'
HOME = str(Path.home())
IDENTITY_FILE = os.path.join(HOME, '.ssh', 'iamport.pem')
SOURCE = os.path.join(HOME, 'workspace', 'lumen', 'iamport')
SECRETS_FILE = os.path.join(SOURCE, 'secrets.json')


def run(cmd, ignore_error=False):
    process = subprocess.run(cmd, shell=True)
    if not ignore_error:
        process.check_returncode()


def ssh_run(cmd, ignore_error=False):
    run(f'ssh -o StrictHostKeyChecking=no -i {IDENTITY_FILE} {TARGET} -C {cmd}', ignore_error=ignore_error)


def local_build_push():
    run(f'poetry export -f requirements.txt > requirements.txt')
    run(f'sudo docker build -t {DOCKER_IMAGE_TAG} .')
    run(f'sudo docker login')
    run(f'sudo docker push {DOCKER_IMAGE_TAG}')


def server_init():
    ssh_run(f'sudo apt update')
    ssh_run(f'sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y')
    ssh_run(f'sudo apt -y install docker.io')


def server_pull_run():
    ssh_run(f'sudo docker stop pay-port', ignore_error=True)
    ssh_run(f'sudo docker pull {DOCKER_IMAGE_TAG}')
    ssh_run('sudo docker run {options} {tag} /bin/bash'.format(
        options=' '.join([
            f'{key} {value}' for key, value in DOCKER_OPTIONS
        ]),
        tag=DOCKER_IMAGE_TAG,
    ))


# 3. Host에서 EC2로 secrets.json을 전송, EC2에서 Container로 다시 전송
def copy_secrets():
    run(f'scp -i {IDENTITY_FILE} {SECRETS_FILE} {TARGET}:/tmp', ignore_error=True)
    ssh_run(f'sudo docker cp /tmp/secrets.json {DOCKER_IMAGE_NAME}:/srv/iamport')
    print('coppy secrets!!!!!!!!')


def server_cmd():
    ssh_run(f'sudo docker exec pay-port /usr/sbin/nginx -s stop', ignore_error=True)
    ssh_run(f'sudo docker exec pay-port python manage.py collectstatic --noinput')
    print('거의 옴')
    ssh_run(f'sudo docker exec -it -d pay-port '
            f'supervisord -c /srv/iamport/.config/local_dev/supervisord.conf -n')
    print('거의 옴')


if __name__ == '__main__':
    try:
        local_build_push()
        server_init()
        server_pull_run()
        copy_secrets()
        server_cmd()
    except subprocess.CalledProcessError as e:
        print('deploy Error')
        print(' cmd:', e.cmd)
        print(' return code:', e.returncode)
        print(' output:', e.output)
        print(' stdout:', e.stdout)
        print(' stderr:', e.stderr)
