#connect to internet
import wolframalpha
def vis():
    client = wolframalpha.Client('6ERJK5-T7YX6JGYK7')

    while True:
        query = str(input('Query: '))
        res = client.query(query)
        output = next(res.results).text
        print(output)
