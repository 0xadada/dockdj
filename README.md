# dockdj

:ship: A recipe for building 12-factor Python / Django web apps with
multi-container Docker and deploying to Amazon AWS using Elastic Beanstalk.

The aim of Dockdj is to provide an example of how to quickly create a
Django web application following the [Twelve Factor](https://12factor.net/)
App principals.

The Twelve Factors

1. Codebase
  One codebase tracked in revision control, many deploys
  :white_check_mark: Yup, GitHub
1. Dependencies
  Explicitly declare and isolate dependencies
  :white_check_mark: Yup, uses requirements.txt
1. Config
  Store config in the environment
  :white_check_mark: Yup, uses .env files
1. Backing Services
  Treat backing services as attached resources
  :white_check_mark: BYOBacking service
1. Build, release, run
  Strictly separate build and run stages
  :white_check_mark: gulp, bin/image, bin/stevedore, bin/deploy
1. Processes
  Execute the app as one or more stateless processes
  :white_check_mark: Thanks Docker!
1. Port binding
  Export services via port binding
  :white_check_mark: 80 & 8010
1. Concurrency
  Scale out via the process model
  :white_check_mark: Keep your sessions in Redis or DB
1. Disposability
  Maximize robustness with fast startup and graceful shutdown
  :white_check_mark: Thank Docker!
1. Dev/Prod parity
  Keep development, staging, and production as similar as possible
  :white_check_mark: Yup
1. Logs
  Treat logs as event streams
  :construction: ToDo
1. Admin Processes
  Run admin/management tasks as one-off processes
  :no_entry_sign: Does not Apply



## Contents

This repo contains a simple Python Django 1.8 web app as well as the
configuration for both Django and NGINX Docker images. There are
also some Bash scripts to help automate the build, release and
deploy process.

**Stack**
* Python 3.4
* Django 1.8
* Gunicorn app server
* Nginx web server
* MySQL
* Sass css preprocessor
* Bootstrap 4-alpha CSS framework
* Gulp build system


## Get Started

This document assumes you are running OS X. These are the requirements
needed by the `bin/install` script;

* Bash
* XCode & command line utilities
* [Homebrew](http://brew.sh) 0.9+

Additionally these requirements are installed:

* [boot2docker](https://github.com/boot2docker/boot2docker-cli)
* Docker & [Docker-compose](https://docs.docker.com/compose/)
* Amazon Web Services
  [Elastic Beanstalk CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html)

These steps will get you running locally:

1. `./bin/install` Provisions your local development machine for
the first time. It will
  * Installs all requirements (if they don't exist)
  * Initializes and starts a Docker virtual machine
1. Rename `environments/dev/.env.example` to `environments/dev/.env` and
   edit the values. Please make sure to change the following keys:
  * `ENV_SECRET_KEY` create your own
  [Django secret key](https://docs.djangoproject.com/en/dev/ref/settings/#secret-key)
  * `ENV_CDN` to your Docker host IP
  * `ENV_AWS_EB_ENVIRONMENT_NAME` to your Amazon AWS Elastic Beanstalk
    environment name
  * `ENV_DOCKER_HUB_REPO_PATH` to your Docker repo (Create one if you
    plan to publish images to Docker Hub.)
1. `./bin/image dev build` Creates "dev" Docker images with all
dependencies installed.
1. `./bin/stevedore dev start` Runs the "dev" Docker containers, open
the browser, and tail the logs. At this point you machine is running code.
  * `ctrl+c` stops the logs `./bin/stevedore dev stop` Stops the Docker
containers.
  * `./bin/stevedore dev logs` Resumes log tailing.

You can typically connect to your web application at:
http://192.168.59.103/xyzzy.


## Deployment

Read more about deploying with Amazon AWS Elastic Beanstalk, version
numbering, running deployments, hotfix / patch deployments, Docker Hub,
and more on the [Deployments](../../wiki/Deployments) wiki page.


## Testing & Code Quality Tooling

Read more about the set of [tools](../../wiki/Tooling) for managing,
testing and deploying.


## Authors

* [Ron. A](https://github.com/0xadada) -
  [@0xadada](http://twitter.com/0xadada)


## License

MIT
