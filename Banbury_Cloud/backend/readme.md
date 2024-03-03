# Backend

There are two parts to the backend.

1. api
2. relay server


## API

This is what you would expect, making api calls to a server that will perform various functions. It will also return information. You can run the server by navigating to the api directory and:

```
python3 manage.py runserver 0.0.0.0:8080 --noreload
```

## Relay Server

In my setup, I currently have this running in a Google Cloud VM Instance.
This is really the backbone of the whole project. Without this, we wouldn't have the ability to
seamlessly interact with devices that are outside of the current network. 

## What's the conservatory directory?

I essentially created a conservatory folder, which is comprised of past versions of the relay server. 
Whenever there is a significant amount of work done or a big feature has been added, I will add 
that particular version to the conservatory. This is just a way of being able to easily go back to working
versions and fetch things I may need. I know I can refer back to past versions in github, but there is
a lot of noise in terms of commits, and it seems much easier to just go ahead follow this method. 
