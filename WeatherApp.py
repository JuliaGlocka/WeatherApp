import requests
from tabulate import tabulate
from datetime import datetime, timedelta
import psycopg2  # connect with PostgreSQL

def connect_db():
    """Function for connecting to the database."""
    return psycopg2.connect(
        dbname="weather_forecast",
        user="postgres",
        password="discoelysium",
        host="localhost",
        port="5432"
    )

# Dictionary of timezones proposed in Open-Meteo.com with geographical places as KEYS and UTC offsets as VALUES
TIME_ZONES = {
    "America/Anchorage": "-9",
    "America/Los_Angeles": "-8",
    "America/Denver": "-7",
    "America/Chicago": "-6",
    "America/New_York": "-5",
    "America/Sao_Paulo": "-3",
    "Europe/London": "0",
    "Europe/Berlin": "+1",
    "Africa/Cairo": "+2",
    "Europe/Moscow": "+3",
    "Asia/Bangkok": "+7",
    "Asia/Singapore": "+8",
    "Asia/Tokyo": "+9",
    "Australia/Sydney": "+11",
    "Pacific/Auckland": "+13"
}

BASE_URL = "https://api.open-meteo.com/v1/forecast"
HOURLY_PARAMETERS = "temperature_2m,apparent_temperature,rain,snowfall"

def get_weather_data(latitude, longitude, timezone, date):
    """Generates GET URL for API based on given parameters."""
    return f"{BASE_URL}?latitude={latitude}&longitude={longitude}&hourly={HOURLY_PARAMETERS}&timezone={timezone}&start_date={date}&end_date={date}"

def fetch_weather_data(url):
    """Fetches forecast data from Open-Meteo API."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Błąd podczas próby wykonania zapytania GET:", e)
        return None

def format_response(response_data, selected_hour):
    """Formats and prints forecast data as a table."""
    hourly_data = response_data.get("hourly", {})
    times = hourly_data.get("time", [])
    table = [
        [time,
         hourly_data["temperature_2m"][i],
         hourly_data["apparent_temperature"][i],
         hourly_data["rain"][i],
         hourly_data["snowfall"][i]]
        for i, time in enumerate(times)
        if selected_hour in time
    ]
    headers = ["Czas", "Temperatura (°C)", "Odczuwalna Temp. (°C)", "Opady deszczu (mm)", "Opady śniegu (cm)"]
    print(tabulate(table, headers=headers, tablefmt="grid"))

def get_timezone_by_offset(offset):
    """Returns timezone based on UTC offset."""
    return next((tz for tz, utc in TIME_ZONES.items() if utc == offset), None)

def get_user_input(prompt, valid_type=float):
    """Gets and validates user input."""
    while True:
        user_input = input(prompt)
        try:
            return valid_type(user_input)
        except ValueError:
            print("Niepoprawny format. Spróbuj ponownie.")

def get_coordinates_from_city(city_name):
    """Fetches city coordinates based on the city name from the PostgreSQL database."""
    conn = connect_db()
    with conn.cursor() as cur:
        # Search for the city regardless of whether a local or English name is used
        cur.execute(
            """
            SELECT latitude, longitude
            FROM cities
            WHERE %s ILIKE ANY(string_to_array(city, ' '))
            """,
            (city_name,)
        )
        result = cur.fetchone()
    conn.close()
    if result:
        return result[0], result[1]
    else:
        print("Miasto nie znalezione w bazie.")
        return None, None

def main():
    """Main function handling user interaction."""
    while True:
        user_input = input("Wpisz 1, aby zobaczyć dane na temat pogody, lub 0, aby zakończyć program: ")

        if user_input == '1':
            search_method = input("Wpisz 1, aby podać nazwę miasta lub 2, aby podać współrzędne geograficzne: ")

            if search_method == '1':
                city_name = input("Wpisz nazwę miasta (lokalna lub angielska): ")
                latitude, longitude = get_coordinates_from_city(city_name)
                if latitude is None or longitude is None:
                    continue  # Skip if city not found
            elif search_method == '2':
                latitude = get_user_input("Wpisz szerokość geograficzną (latitude): ")
                longitude = get_user_input("Wpisz długość geograficzną (longitude): ")
            else:
                print("Nieprawidłowy wybór. Wpisz 1 lub 2.")
                continue

            print("Dostępne strefy czasowe (czas standardowy):")
            print(tabulate(TIME_ZONES.items(), headers=["Strefa Czasowa", "Przesunięcie UTC"], tablefmt="grid"))

            while True:
                offset = input("Wpisz przesunięcie UTC dostępne w tabeli (np. -3, 0, +3): ")
                if offset in TIME_ZONES.values():
                    timezone = get_timezone_by_offset(offset)
                    break
                print("Niepoprawne przesunięcie UTC. Spróbuj ponownie.")

            today = datetime.now().date()
            days_ahead = today + timedelta(days=15)
            date_input = get_user_input(f"Wpisz datę (RRRR-MM-DD) w zakresie od {today} do {days_ahead}: ", str)
            selected_date = datetime.strptime(date_input, "%Y-%m-%d").date()

            while True:
                hour_input = get_user_input("Wpisz godzinę prognozy (00-23): ", str)
                if hour_input.isdigit() and 0 <= int(hour_input) <= 23:
                    selected_hour = f"T{hour_input.zfill(2)}:00"
                    break
                print("Godzina musi być liczbą od 0 do 23.")

            url = get_weather_data(latitude, longitude, timezone, selected_date)
            print("Skonstruowany URL:", url)

            weather_data = fetch_weather_data(url)
            if weather_data:
                if city_name:
                    print(f"Wprowadzono miasto: {city_name}")
                else:
                    print(f"Wprowadzono współrzędne: szerokość = {latitude}, długość = {longitude}")
                print(f"Wprowadzona strefa czasowa: {timezone}")
                print("Pogoda dla wybranej daty i godziny:")
                format_response(weather_data, selected_hour)

        elif user_input == '0':
            print("Zamykanie aplikacji.")
            break
        else:
            print("Nieprawidłowy wybór. Wpisz 1 lub 0.")

if __name__ == "__main__":
    main()
