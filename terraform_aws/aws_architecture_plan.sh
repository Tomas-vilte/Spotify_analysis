#!/usr/bin/env bash

# Run this script pointing to all libraries required to package them for the Lambda.

terraform init
cp -r /home/tomi/Spotify_analysis/venv/lib/python3.10/site-packages/typing_extensions.py ../lambda_payloads/
cp -r /home/tomi/Spotify_analysis/venv/lib/python3.10/site-packages/dotenv ../lambda_payloads/
cp -r /home/tomi/Spotify_analysis/venv/lib/python3.10/site-packages/certifi ../lambda_payloads/
cp -r /home/tomi/Spotify_analysis/venv/lib/python3.10/site-packages/idna ../lambda_payloads/
cp -r /home/tomi/Spotify_analysis/venv/lib/python3.10/site-packages/charset_normalizer ../lambda_payloads/
cp -r /home/tomi/Spotify_analysis/venv/lib/python3.10/site-packages/packaging ../lambda_payloads/
cp -r /home/tomi/Spotify_analysis/venv/lib/python3.10/site-packages/redis ../lambda_payloads/
cp -r /home/tomi/Spotify_analysis/venv/lib/python3.10/site-packages/spotipy ../lambda_payloads/
cp -r /home/tomi/Spotify_analysis/venv/lib/python3.10/site-packages/requests ../lambda_payloads/

cp -r /home/tomi/Spotify_analysis/src/avg_album_playlist.py  ../lambda_payloads/
cp -r /home/tomi/Spotify_analysis/config ../lambda_payloads/config
cp -r /home/tomi/Spotify_analysis/tools ../lambda_payloads/tools


cd ../lambda_payloads/




zip -r ../payload.zip *

cd ../terraform_aws/

terraform plan
