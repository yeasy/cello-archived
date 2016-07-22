#!/usr/bin/env bash

nuitka --module $1 --recurse-directory=$1
