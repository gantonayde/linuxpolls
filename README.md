# LINUXPOLLS

## Setup

Google Compute Engine f1-micro instance for VM

Cloudflare for CDN

### Good for App Engines
STATIC_FILES - WhiteNoise + CDN (gunicorn will serve static when there is no CDN cache)
### Good for VMs
STATIC_FILES - ngnix + [ optional - CDN (nginx will serve static when there is no CDN cache)]

MEDIA FILES - Google Cloud Storage (any server)
Database - ElephantSQL (20Mb can be hosted on any GCP, AWS, Azure, IBM) or MongoDB (racing condictions do not work in Django with djongo)


### Troubleshooting
For additional troubleshooting, the logs can help narrow down root causes. Check each of them in turn and look for messages indicating problem areas.

The following logs may be helpful:
Check the Nginx process logs by typing: `sudo journalctl -u nginx`
Check the Nginx access logs by typing: `sudo less /var/log/nginx/access.log`
Check the Nginx error logs by typing: `sudo less /var/log/nginx/error.log`
Check the Gunicorn application logs by typing: `sudo journalctl -u gunicorn`

As you update your configuration or application, you will likely need to restart the processes to adjust to your changes.

If you update your Django application, you can restart the Gunicorn process to pick up the changes by typing:
```sudo systemctl restart gunicorn```

If you change gunicorn systemd service file, reload the daemon and restart the process by typing:
```sudo systemctl daemon-reload```
```sudo systemctl restart gunicorn```

If you change the Nginx server block configuration, test the configuration and then Nginx by typing:
```sudo nginx -t && sudo systemctl restart nginx```

These commands are helpful for picking up changes as you adjust your configuration.

### Analysis
https://goaccess.io/