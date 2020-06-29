import argparse
import os
from datetime import datetime
from glob import glob
from typing import List

import matplotlib.pyplot as plt
import pandas_gbq

MOUNT_LOCATION = '/share'
choices = {'confirmed_cases',
           'deaths',
           'new_deaths'
           }
maps = {'new_deaths': 'deaths - LAG(deaths) OVER (PARTITION BY state_name ORDER BY date)'}
labels = {'deaths': 'Total Deaths by State',
          'confirmed_cases': 'Confirmed Cases by State',
          'new_deaths': 'Daily Deaths by State'
          }


def clean():
    files = glob(f'{MOUNT_LOCATION}/*.png')
    for file_path in files:
        try:
            os.remove(file_path)
        except:
            print("Error while deleting file : ", file_path)


def main(metric: str, states: List[str]):
    extra_colums = ','.join(col for col in choices if col not in maps)
    aliased_columns = ','.join([f'{expression} as {alias}' for alias, expression in maps.items()])

    query = f"""
            SELECT state_name, date, {extra_colums}, {aliased_columns}
            FROM `bigquery-public-data.covid19_nyt.us_states`
            WHERE state_name IN ({','.join([f"'{x}'" for x in states])})
            order by date
            LIMIT 1000 
        """
    data_frame = pandas_gbq.read_gbq(query)

    fig, ax = plt.subplots(figsize=(10, 5))

    for key, grp in data_frame.groupby(['state_name']):
        ax = grp.plot(ax=ax, label=key, kind='line', x='date', y=metric)

    plt.legend(loc='best')
    plt.title(labels.get(metric))
    filename = f'{datetime.now().isoformat()}.png'
    plt.savefig(f'/{MOUNT_LOCATION}/{filename}')
    print('\n')
    print(f'output: {filename}')


parser = argparse.ArgumentParser(description='COVID 19 Stats by day by state.')
parser.add_argument("--metric", "-m",
                    default='deaths',
                    choices=choices,
                    help='Metric to count. Defaults to deaths.')
parser.add_argument('--clean', "-c",
                    help='Clean up files created by this application.',
                    action='store_const',
                    const=clean,
                    default=lambda: None)
parser.add_argument('states', nargs="+", help='Name of state to show.')


if __name__ == '__main__':
    args = parser.parse_args()
    args.clean()
    main(args.metric, args.states)
