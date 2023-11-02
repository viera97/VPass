# VPass

Vpass is a self-hosted password manager and OTP code generator. The main goal of this project is to stop using private company password managers and really start caring about your security. This project can be used offline, no internet required, but you can also host it on cloud like [linode](https://www.linode.com/) or other services. If the project has internet access for a period of time it can sync between devices. It's a `Django` project with nice and clean interface. It has encryption functionalities among others.

> Note: This project is in active development, be aware that various changes may occur.

## Using
For start using the project you need to clone the repository:

```bash
git clone https://github.com/viera97/VPass
```

you should create `python` venv for installing the dependencies. Use the following code for creating a venv in hidden folder .venv

```bash
python -m venv .venv
source .venv/bin/activate
```

## Installing dependencies and making migrations
```bash
pip install -r requirements.text
python manage.py migrate
```
## Run the server
After this you can run the server by doing
```bash
python manage.py runserver
```
And you can acces it on any browser at: [localhost:8000](localhost:8000) or [127.0.0.1:8000](127.0.0.1:8000). You can serve in any ip and in a specific port by doing
```bash
python manage.py runserver 0.0.0.0:8181
```
in this example the used port is `8181`.

For more information you can follow the [documentation](link-a-la-documentacion)