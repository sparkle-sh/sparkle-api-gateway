#!/bin/bash

docker run --name sparkle-db --rm -e POSTGRES_PASSWORD='foo' -v "$PWD/misc/schema.sql:/docker-entrypoint-initdb.d/schema.sql" -it -p 5432:5432 postgres:12
