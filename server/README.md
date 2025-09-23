# Server README  
Main folder for server deployment

## Quick Start  
Make sure you have the necessary python dependencies download, check out main/README.md. Next we need to set up our docker environment. If you are unfamiliar with docker check out https://docs.sevenbridges.com/docs/install-docker-on-linux .
```bash
docker compose up --build
```

Superuser of django admin: 
```bash
python manage.py runserver 
```

To **shut down** the docker server simply *Ctr + C*