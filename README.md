# check-vmhub.py - retrieve statistics and monitor VirginMedia superhub


## Installation 

Install requirements

	pip install -r requirements.txt

## Usage

	$ check-vmhub.py -j -d 10.20.30.40 -p hub-password
	servername.virginmedia.uploaded 37257 1478171531
	servername.virginmedia.downloaded 288038 1478171531
	servername.virginmedia.session_time 1474313556 1478171531

	$ check-vmhub.py -d 10.20.30.40 -p hub-password
	PING ok - downloaded = 288039, MB, uploaded = 37257 MB | downloaded=288039, uploaded=37257, session_time=1474313555

## Detailed Usage

	`-g` or `--graphite` output in graphite format
	`-d` or `--host` provide alternative superhub IP/name, default of `192.168.0.1`
	`-p` or `--password` provide login password
