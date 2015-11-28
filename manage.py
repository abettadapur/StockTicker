import argparse

from stocks import db
from stocks.models.models import *

def create_db():
    db.create_all()
    setting = Setting()
    setting.one_week_threshold = 10.0
    setting.one_month_threshold = 15.0
    setting.three_month_threshold = 25.0
    setting.quarterly_growth_threshold = 25.0
    setting.float_threshold = 300000000
    
    db.session.add(setting)
    db.session.commit()

def drop_db():
    db.drop_all()


def main():
    parser = argparse.ArgumentParser(
        description='Manage this Flask application.')
    parser.add_argument(
        'command', help='the name of the command you want to run')
    parser.add_argument(
        '--seedfile', help='the file with data for seeding the database')
    args = parser.parse_args()

    if args.command == 'create_db':
        create_db()

        print "DB created!"
    elif args.command == 'delete_db':
        drop_db()

        print "DB deleted!"
    else:
        raise Exception('Invalid command')

if __name__ == '__main__':
    main()