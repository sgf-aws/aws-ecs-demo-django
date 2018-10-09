#!/bin/bash

SRC=.env
DST=s3://sgfaws-laravel-demo/django-config/.env

if [ -f $SRC ]; then
    echo aws s3 cp $SRC $DST
    aws s3 cp $SRC $DST --sse aws:kms
else
    echo "File not found [$SRC]"
fi
