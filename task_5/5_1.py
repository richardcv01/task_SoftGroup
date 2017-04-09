import argparse
import requests

parser = argparse.ArgumentParser(prog = 'richardcv',
            description = '''The program shows the current air temperature of the indicated city''',
            epilog = '''(c) 2017. end  .''')
parser.add_argument('-l', '-L', '--city', help='City',nargs='+', default='Chernivtsi', type=str)
parser.add_argument('-i','-I', '--city_id', help='City_id', default=0, type = str)

arg = parser.parse_args()
city = arg.city
city_id = arg.city_id
if (city_id and city):
    city = ''

def print_temp(city, city_id):
    appid = 'ad3e81d779b543d67e3faf5a6da3bf96'
    url = 'http://api.openweathermap.org/data/2.5/find'
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                 params={'q': city, 'id': city_id, 'units': 'metric', 'lang': 'ua', 'APPID': appid})
    data = res.json()
    temp = str(data['main']['temp'])
    symvol = '\u00B0C'
    print('{0} {1}{2}'.format('Current temp:',temp,symvol ))

print_temp(city, city_id)
