# Geneteka Crawler

Website https://geneteka.genealodzy.pl contains awesome information but no
sensible way to monitor the newly appearing results for all the variations of
the researched names.

This app provides a way to download the basic stats for a given last name
variation.  One can call it for each variant and save the results.  Once you
detect a change in the numbers since the last saved report, you can follow the
URLs and manually check the new results.

Remember to donate to the project if you're using its services, whether via
this app or the web interface.

## Install locally

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -e .[dev]
```
This also installs a script `geneteka-crawler` into the virtual environment.

## Usage

```
$ geneteka-crawler "Surname One"
$ geneteka-crawler "Surname One" -s "Surname Two"
$ geneteka-crawler "Surname One" -s "Surname Two" -f 1795 -t 1840
```
