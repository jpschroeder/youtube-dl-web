
# youtube-dl-web

This is a web wrapper around the [youtube-dl](http://rg3.github.io/youtube-dl/) project.  It downloads the files to the server and then provides the user with a with a link to download it locally.  Files older than 2 days will be removed.

## installation

First copy `app/env.sample` to `app/.env` and add your own secret key.

While you can run the project manually using python, it is recommended to use docker and the attached Dockerfile.  The docker commands to build, run, and cleanup the project have been included in the attached Makefile.

`make` will build the image and run a container.  It will listen on port 8081.

`make clean` will stop the the container, remove the container, and remove the image.

You can also push the repository to a [dokku](http://dokku.viewdocs.io/dokku/) instance to deploy it to a server.

## usage

Paste a youtube link into the main input box.  Once the processing completes, click on the generated link.

## todo

- download collections
- pull the download url from the route url
- build a chrome extension

## credits

- [youtube-dl](https://github.com/rg3/youtube-dl/)
- [Flask](https://github.com/pallets/flask)
- [Flask-SocketIO](https://github.com/miguelgrinberg/Flask-SocketIO)
- Jeremy Thomas: [Web Design in 4 minutes](http://jgthms.com/web-design-in-4-minutes/)

