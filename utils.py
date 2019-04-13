# -*- coding: utf-8 -*-

import settings
import json
import subscription
import click
import csv
import datetime
import logging


logger = logging.getLogger('satsie.utils')


@click.group()
def cli():
    pass


def load_db(db):
    try:
        with open(db) as input:
            return json.load(input)
    except:
        print ('INVALID DATABASE!')
        raise SystemExit


def dump_db(db, data):
    with open(db, 'w') as output:
        json.dump(data, output)


def sketch_meta(name, db=settings.SUBSCRIPTIONS_FILE):
    data = {}
    data[name] = {}
    dump_db(db, data)


@cli.command(help='sketch a json file for storing data')
def sketch():
    sketch_meta('subscriptions')
    logger.info('sketched a json file for storing data. ')


@cli.command(help='new a subscription')
@click.option('--url', help='the subscription to add')
def new(url):
    s = subscription.Subscription(url)
    s.initialize()


@cli.command(help='check if any updates on a specific subscription')
@click.option('--url', help='the subscription to check')
def arenew(url):
    s = subscription.Subscription(url)
    s.update()


@cli.command(help='check if any updates on all the subscriptions')
def renew(db=settings.SUBSCRIPTIONS_FILE):
    data = load_db(db)
    urls = data['subscriptions'].keys()
    for url in urls:
        s = subscription.Subscription(url)
        s.update()


@cli.command(help='list the subscriptions')
def ls(db=settings.SUBSCRIPTIONS_FILE):
    data = load_db(db)
    urls = data['subscriptions'].keys()
    for url in urls:
        print (url)


@cli.command(help='dump the subscriptions and their info')
@click.option('--options', type=click.Choice(['created_at', 'updated_at']), multiple=True)
def dump(options, db=settings.SUBSCRIPTIONS_FILE):
    data = load_db(db)
    headers = ['url']
    for option in options:
        headers.append(option)
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    with open('subscriptions_%s.csv' % now, 'wb') as output:
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        urls = data['subscriptions'].keys()
        for url in urls:
            fields = {'url': url}
            for option in options:
                fields[option] = data['subscriptions'][url][option]
            writer.writerow(fields)


@cli.command(help='unsubscribe from a url')
@click.option('--url', help='the subscription to remove')
def remove(url):
    s = subscription.Subscription(url)
    s.remove()


@cli.command(help='search')
@click.option('--keyword', help='keyword')
@click.option('--option', type=click.Choice(['url', 'created_at', 'updated_at']))
def search(keyword, option, db=settings.SUBSCRIPTIONS_FILE):
    data = load_db(db)
    urls = data['subscriptions'].keys()
    findings = []
    if option == 'url':
        if keyword in urls:
            print (data['subscriptions'][keyword])
            return
        print (findings)
        return
    for url in urls:
        if str(keyword) in str(data['subscriptions'][url][option]):
            findings.append(data['subscriptions'][url])
    print (findings)


if __name__ == '__main__':
    cli()
