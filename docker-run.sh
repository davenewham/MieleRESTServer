#!/bin/bash
docker run --net=host -v /etc/MieleRESTServer.config:/etc/MieleRESTServer.config mielerestserver
