from fabric.api import *
from fabtools import require
import fabtools

@task
def setup():

    # Require some Debian/Ubuntu packages
    # require.deb.packages([
    #     'imagemagick',
    #     'libxml2-dev',
    # ])

    # Require a Python package
    with fabtools.python.virtualenv('venv'):
        require.python.package('pyramid')

    # Require a PostgreSQL server
    # require.postgres.server()
    # require.postgres.user('myuser', 's3cr3tp4ssw0rd')
    # require.postgres.database('myappsdb', 'myuser')

    # Require a supervisor process for our app
    require.supervisor.process('hello',
                               command='hello',
                               directory='health')

    # Require an nginx server proxying to our app
    # require.nginx.proxied_site('example.com',
    #                            docroot='/home/myuser/env/myapp/myapp/public',
    #                            proxy_url='http://127.0.0.1:8888'
    #                            )

    # Setup a daily cron task
    # fabtools.cron.add_daily('maintenance', 'myuser', 'my_script.py')