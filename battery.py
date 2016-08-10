#!/usr/bin/env python3
import logging
import re
import subprocess
import sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream=sys.stderr)
logger = logging.getLogger(__name__)

def main():
    encoding = 'utf-8'
    output = ''

    power_supplies_proc = subprocess.run(['upower', '-e'], stdout=subprocess.PIPE, check=True)
    power_supplies = [line for line in iter(power_supplies_proc.stdout.decode(encoding).splitlines())]

    batteries = []
    for power_supply in power_supplies:
        if 'BAT' in power_supply:
            batteries.append(power_supply)
    logger.debug('Following batteries were found: %s', str(batteries))

    if len(batteries) <= 0:
        logger.error('No battery found')
    elif len(batteries) > 1:
        logger.error('Multiple batteries found')
    else:
        battery = batteries[0]
        logger.info('Using battery: %s', battery)
        battery_info_cli = subprocess.run(['upower', '-i', battery], stdout=subprocess.PIPE, check=True)
        battery_info = battery_info_cli.stdout.decode(encoding)
        logger.debug("Found battery information\n%s  for battery %s", battery_info, battery)

        percentage = get_battery_percentage(battery_info)
        if percentage is None:
            logger.error('Did not find battery percentage')
        else:
            logger.info('Battery percentage is %s', percentage)
            battery_percentage_symbols = ['[      ]', '[I     ]', '[II    ]', '[III   ]', '[IIII  ]', '[IIIII ]', '[IIIIII]']
            percentage_num = int(percentage.replace('%',''))
            symbol_index = round(percentage_num/100 * (len(battery_percentage_symbols) - 1))
            output = battery_percentage_symbols[symbol_index]

    print(output)

def get_battery_percentage(battery_info):
    for line in iter(battery_info.splitlines()):
        if 'percentage' in line:
            percentage_match = re.search('\d+%', line)
            if percentage_match is not None:
                return percentage_match.group(0)
            else:
                return None


if __name__ == '__main__':
    logger.info('Entering main...')
    main()
