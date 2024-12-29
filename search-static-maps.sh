#!/bin/bash

search_static_map() {
    for map in $@; do
        for query in query/*png; do
            python sift.py $map "${query}"
        done
    done
}

search_static_map static-maps/london*-static.png
