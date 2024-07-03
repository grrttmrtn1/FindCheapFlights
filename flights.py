import requests
import datetime

airports = [
    {
        "city": "",
        "id": "",
        "code": ""
    },
    {
        "city": "",
        "id": "",
        "code": ""
    },
    {
        "city": "",
        "id": "=",
        "code": ""
    }]

def get_upcoming_friday():
    today = datetime.date.today()
    # Calculate the number of days until the next Friday (5)
    days_until_friday = (4 - today.weekday() + 7) % 7
    if days_until_friday == 0:  # If today is Friday, get the next Friday
        days_until_friday = 7
    upcoming_friday = today + datetime.timedelta(days=days_until_friday)
    return upcoming_friday.strftime("%Y-%m-%d")

def get_upcoming_saturday():
    today = datetime.date.today()
    # Calculate the number of days until the next Friday (5)
    days_until_saturday = (5 - today.weekday() + 7) % 7
    if days_until_saturday == 0:  # If today is Friday, get the next Friday
        days_until_saturday = 7
    upcoming_saturday = today + datetime.timedelta(days=days_until_saturday)
    return upcoming_saturday.strftime("%Y-%m-%d")

def get_upcoming_sunday():
    today = datetime.date.today()
    # Calculate the number of days until the next Friday (5)
    days_until_sunday = (6 - today.weekday() + 7) % 7
    if days_until_sunday == 0:  # If today is Friday, get the next Friday
        days_until_sunday = 7
    upcoming_sunday = today + datetime.timedelta(days=days_until_sunday)
    return upcoming_sunday.strftime("%Y-%m-%d")


try:
    flights = [] 
    cheapFlights = []
    for airport in airports:
        airport['code']
        headers = {
            'x-rapidapi-host': 'sky-scrapper.p.rapidapi.com',
            'x-rapidapi-key': ''
        }
        uri = 'https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchFlightEverywhereDetails?originSkyId=' + airport['code'] + '&travelDate=' + get_upcoming_friday() + '&returnDate=' + get_upcoming_sunday() + '&CountryId=us&oneWay=false&currency=USD'
        r = requests.get(uri,headers=headers)
        flights += r.json()['data']

    for flight in flights:
        if flight['Quote']['Price'] < 300:
            headers = {
                'x-rapidapi-host': 'airports15.p.rapidapi.com',
                'x-rapidapi-key': ''
            }
            uri = 'https://airports15.p.rapidapi.com/airports/iata/' + flight['Quote']['DestinationPlaceId'][:len(flight['Quote']['DestinationPlaceId'])-1]
            r = requests.get(uri,headers=headers)
            flight['Quote']['DestinationCity'] = r.json()['city']
            cheapFlights.append(flight['Quote'])

    if len(cheapFlights) >= 1:
        html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Flight Information</title>
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                    }
                    th, td {
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h2>Flight Information</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Origin Place</th>
                            <th>Destination Place</th>
                            <th>Destination City</th>
                            <th>Outbound Departure Date</th>
                            <th>Inbound Departure Date</th>
                            <th>Direct</th>
                            <th>Currency</th>
                            <th>Price</th>
                            <th>Origin Place Type</th>
                        </tr>
                    </thead>
                    <tbody>
            """
        for flight in cheapFlights:
            html += f"""
                    <tr>
                        <td>{flight['OriginPlaceId']}</td>
                        <td>{flight['DestinationPlaceId']}</td>
                        <td>{flight['DestinationCity']}</td>
                        <td>{flight['OutboundDepartureDate']}</td>
                        <td>{flight['InboundDepartureDate']}</td>
                        <td>{'Yes' if flight['Direct'] else 'No'}</td>
                        <td>{flight['CurrencyId']}</td>
                        <td>{flight['Price']}</td>
                        <td>{flight['OriginPlaceType']}</td>
                    </tr>
            """
        # Close the HTML string
        html += """
                </tbody>
            </table>
        </body>
        </html>
        """
except requests.exceptions.RequestException as e:
    raise SystemExit(e) 
