from fabric.api import *
from fabtools import require
import fabtools

host = '165.227.28.54'

@task(default=True)
def deploy():
    #execute(system_dependencies)
    execute(setup_health)
    execute(start_serving)

@task
@hosts(['root@' + host])
def system_dependencies():
    # get some packages
    require.deb.uptodate_index()

    # Require some Debian/Ubuntu packages
    require.deb.packages([
        'python3',
        'nginx-full',
        'python3-dev',
        'python3-pip',
        'git',
        'python3-venv'
    ])

    # let's make a user for our app
    require.user('health')

    # also install cloud monitoring
    run("curl -sSL https://agent.digitalocean.com/install.sh | sh")

    run("mkdir ~health/.ssh")
    run("cp ~/.ssh/authorized_keys ~health/.ssh/authorized_keys")
    run("chown -R health:health ~health/.ssh")

@task
@hosts(['health@' + host])
def setup_health():
    # copy this up there
    require.git.working_copy('https://github.com/fusiongyro/health2', 'health')

    run("python3 -m venv ~/venv")

    # Require a Python package
    with prefix('source ~/venv/bin/activate'):
        with cd('health'):
            run('python setup.py develop')

@task
@hosts(['root@' + host])
def start_serving():
    # Require a PostgreSQL server
    # require.postgres.server()
    # require.postgres.user('myuser', 's3cr3tp4ssw0rd')
    # require.postgres.database('myappsdb', 'myuser')

    # Require a supervisor process for our app
    require.supervisor.process('health',
                               command='/home/health/venv/bin/pserve /home/health/health/production.ini',
                               directory='/home/health/health',
                               user='health')

    # Require an nginx server proxying to our app
    require.nginx.proxied_site('health2.7gf.org',
                               docroot='/home/health/health/static',
                               proxy_url='http://127.0.0.1:6543')

    # Setup a daily cron task
    # fabtools.cron.add_daily('maintenance', 'myuser', 'my_script.py')