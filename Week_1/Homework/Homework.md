## Question 1. Knowing docker tags

--rm : Automatically remove the container when it exits

## Question 2: Understanding docker first run
docker run command for python:3.9 in interactive mode and bash entrypoint

docker run -it --entrypoint=bash python:3.9
pip list

Gives the output:
Package    Version
---------- -------
pip        23.0.1
setuptools 58.1.0
wheel      0.42.0

Version of package wheel=0.42.0

## Preparing Postgres