#!/bin/bash

[ $(docker container ls -aq | wc -l) -eq $(docker container ls -f "status=running" -q | wc -l) ]