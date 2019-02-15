#!/usr/bin/env python
#
# Análise de Logs - NASA KENNEDY SERVER
#
# Autor: Quenaz da Cruz Eller (quenaz@gmail.com)
#


import re
from datetime import datetime

from pyspark import SparkContext, SparkConf


class LogAnalysis(object):

    def __init__(self):
        self.__conf = SparkConf().setMaster('local[*]')
        self.__files = 'data'

    def date_to_str(self, input_date):
        ''' Convert input date to string'''
        try:
            return datetime.fromordinal(input_date).strftime('%d/%b/%Y')
        except Exception as e:
            return '01/01/1900'

    def get_url(self, url):
        ''' Get url from log data '''
        try:
            re_result = re.compile('(HEAD|GET|POST) (.*)').match(url[2])
            return url[0] + re_result.group(2).split()[0]
        except Exception as e:
            return ''

    def parseLog(self, data):
        ''' Read and parse log data '''
        RE_MASK = '(.*) - - \[(.*):(.*):(.*):(.*)\] "(.*)" ([0-9]*) ([0-9]*|-)'

        try:
            re_result = re.compile(RE_MASK).match(data)
            host = re_result.group(1)
            ord_day = datetime.strptime(re_result.group(2), '%d/%b/%Y').toordinal()
            req = re_result.group(6)
            reply_code = int(re_result.group(7))
            
            try:
                reply_bytes = int(re_result.group(8))
            except ValueError as e:
                reply_bytes = 0
            return host, ord_day, req, reply_code, reply_bytes
        
        except Exception as e:
            return '', -1, '', -1, -1

    def printf(self, msg: str) -> None:
        print('\033[32m' + msg + '\033[0m')


    def run(self) -> int:
        sc = SparkContext().getOrCreate(self.__conf)

        rows = sc.textFile(self.__files)
        rdd = rows.map(self.parseLog).filter(lambda l: l[1] > -1)
        rdd.cache

        num_hosts = rdd.keys().distinct().count()

        get_404_errors = rdd.filter(lambda l: l[3] == 404)
        get_404_errors.cache
        fail_404_errors_count = get_404_errors.count()

        url_data = get_404_errors.map(lambda s: (self.get_url(s), 1)) \
              .reduceByKey(lambda a, b: a + b) \
              .sortBy(keyfunc=lambda l: l[1], ascending=False)
              
        fail_top_5_data = url_data.map(lambda l: l[0]).take(5)
        fail_top_5 = ''.join('\n    %s ' % url for url in fail_top_5_data)

        fail_by_day = get_404_errors.map(lambda s: (s[1], 1))
        fail_by_day_counts = fail_by_day.reduceByKey(lambda a, b: a + b).sortByKey()
        fail_by_day_counts_data = fail_by_day_counts.collect()

        total_fail_by_day = '\n'
        for date_count in fail_by_day_counts_data:
            total_fail_by_day += '%s: %d\n' % (self.date_to_str(date_count[0]), date_count[1])

        total_bytes_data = rdd.map(lambda s: s[4] / 1073741824.0)
        total_bytes = total_bytes_data.sum()

        self.printf('-> 1. Numero de hosts unicos: %d ' % num_hosts)
        self.printf('-> 2. Numero total de erros 404: %d ' % fail_404_errors_count)
        self.printf('-> 3. Os 5 URLs que mais causaram erros 404: %s' % fail_top_5)
        self.printf('-> 4. Quantidade de erros 404 por dia: %s \n' % total_fail_by_day)
        self.printf('-> 5. Total de bytes retornados: %.2f %s' % (total_bytes, 'Gb'))

        return 0

def main() -> int:
    return LogAnalysis().run()

if __name__ == '__main__':
    main()
