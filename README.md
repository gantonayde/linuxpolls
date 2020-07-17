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

### Commands

```sudo journalctl -u gunicorn```

shows gunicorn console log, similar to when using 'runserver'



