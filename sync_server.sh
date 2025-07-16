# the syncignore sends the .env
rsync -avz --exclude-from=.syncignore . tsunami@raid:/home/user/


# install package: python3 -m pip install . --break-system-packages