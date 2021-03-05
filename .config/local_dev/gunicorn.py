daemon = False
chdir = '/srv/iamport/app'
bind = 'unix:/run/iamport.sock'
accesslog = '/var/log/gunicorn/iamport-access.log'
errorlog = '/var/log/gunicorn/iamport-error.log'
capture_output = True
