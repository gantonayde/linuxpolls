# LINUXPOLLS

LinuxPolls.com is a toy model website made with Django. The website can serve as a news outlet and data generator based on users input. Frontend uses Bootstrap and Javascript. PosgreSQL is used for the database. Data is visualised using Plotly. The project can be hosted on GCP AppEngine or deployed on a Linux server using the script `server_setup.sh`.

## Features

- CMS for posts, questions and figures. 
- Categories for posts.
- Hitcounter for posts.
- IP2Location integration.
- HyvorTalk comments integration.
- Summernote can be used for formatting articles content.

## Setup

Example with Google Compute Engine f1-micro instance.

1. Create `.env` file in `linuxpolls`, check `linuxpolls/.env.example` to see what needs to be included.
2. Create `credentials.json` file in `linuxpolls` directory. More information on how to generate this file can be found here https://cloud.google.com/docs/authentication/getting-started
3. Edit `WEBSITE_NAME` and `DOMAIN` in `server_setup.sh` accordingly.
4. Run `chmod +x server_setup.sh`.
5. Execute `server_setup.sh`. This should configure the server, i.e. migrate the database, collect static files, install all requirements, configure nginx and gunicorn and instal SSL certificate.  

STATIC_FILES are served with ngnix + [ optional - CDN, i.e. Cloudflare (nginx will serve static when there is no CDN cache)]

MEDIA FILES are served from Google Cloud Storage.

Database uses PostgreSQL. A decent choice is ElephantSQL (20Mb can be hosted on any GCP, AWS, Azure, IBM). MongoDB is not recommended because racing condictions cannot be avoided in Django with the djongo module.

*Optional: If you want to add a swapfile to your server instance you can use `deploy/make_swap.sh` in order to create a 1GB swap file.

### App Engine configuration

You need to create the `.env` and `credentials.json` files before uploading the project to the App Engine.

It might be a good idea to change `WHITENOISE=True` in `linuxpolls/settings.py` when using App Engine. STATIC_FILES can be served with WhiteNoise + CDN, i.e. Cloudflare (gunicorn will serve static when there is no CDN cache)

### Troubleshooting
For additional troubleshooting, the logs can help narrow down root causes. Check each of them in turn and look for messages indicating problem areas.

The following logs may be helpful:
Check the Nginx process logs by typing: `sudo journalctl -u nginx`
Check the Nginx access logs by typing: `sudo less /var/log/nginx/access.log`
Check the Nginx error logs by typing: `sudo less /var/log/nginx/error.log`
Check the Gunicorn application logs by typing: `sudo journalctl -u gunicorn`

*As you update your configuration or application, you will likely need to restart the processes to adjust to your changes.*

If you update your Django application, you can restart the Gunicorn process to pick up the changes by typing:
```sudo systemctl restart gunicorn```

If you change gunicorn systemd service file, reload the daemon and restart the process with:
```sudo systemctl daemon-reload```
```sudo systemctl restart gunicorn```

If you change the Nginx server block configuration, it is recommended to check the setup with:
```sudo nginx -t && sudo systemctl restart nginx```

These commands are helpful for picking up changes as you adjust your configuration.

### Requests Analysis
A user-friendly way of analysing the `access.log` file is provided by goaccess.io. On Debian/Ubuntu the program can be installed by running:

`sudo apt install goaccess`

After the installation is done, run `goaccess /var/log/nginx/access.log -c` to inspect the `access.log` file.

You can also genarate an html file showing the same data by running:
`goaccess /var/log/nginx/access.log -o /var/www/html/report.html --log-format=COMBINED --real-time-html`