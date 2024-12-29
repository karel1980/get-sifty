#!/bin/bash

jq -r '.[] | select(.capital != null) | [.capital[0], .latlng[0], .latlng[1]] | @csv' countries.json 

