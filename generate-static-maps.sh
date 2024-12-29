#!/bin/bash

generate_static_map() {
    mbtiles="$1"
    name=$(basename "$mbtiles")

    if [ ! -e "$mbtiles" ]; then
        echo "$mbtiles does not exist"
        return
    fi

    # update config.json with tile file
    jq '.data.openmaptiles.mbtiles = "/data/'$name'"' tiles/config.json.template > tiles/config.json

    # run tile server
    ./tileserver.sh
    sleep 2

    echo "Generating static map in static-maps"
    python generate-static-maps.py $(basename "$mbtiles" .mbtiles)
}

generate_static_map tiles/amsterdam.mbtiles
generate_static_map tiles/london.mbtiles
