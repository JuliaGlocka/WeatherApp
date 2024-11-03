import requests
from tabulate import tabulate
from datetime import datetime, timedelta

# Zdefiniowane strefy czasowe i ich przesunięcia UTC
TIME_ZONES = {
    "America/Anchorage": "-9",         # UTC-09:00, w czasie letnim UTC-08:00
    "America/Los_Angeles": "-8",       # UTC-08:00, w czasie letnim UTC-07:00
    "America/Denver": "-7",             # UTC-07:00, w czasie letnim UTC-06:00
    "America/Chicago": "-6",            # UTC-06:00, w czasie letnim UTC-05:00
    "America/New_York": "-5",           # UTC-05:00, w czasie letnim UTC-04:00
    "America/Sao_Paulo": "-3",          # UTC-03:00, czas standardowy
    "Europe/London": "0",                # UTC+00:00, w czasie letnim UTC+01:00
    "Europe/Berlin": "+1",              # UTC+01:00, w czasie letnim UTC+02:00
    "Europe/Moscow": "+3",              # UTC+03:00, czas standardowy
    "Africa/Cairo": "+2",               # UTC+02:00, czas standardowy
    "Asia/Bangkok": "+7",               # UTC+07:00, czas standardowy
    "Asia/Singapore": "+8",              # UTC+08:00, czas standardowy
    "Asia/Tokyo": "+9",                 # UTC+09:00, czas standardowy
    "Australia/Sydney": "+11",           # UTC+11:00, w czasie letnim UTC+10:00
    "Pacific/Auckland": "+13"            # UTC+13:00, w czasie letnim UTC+12:00
}

# URL i nagłówki
BASE_URL = "https://api.open-meteo.com/v1/forecast"
HOURLY_PARAMETERS = "temperature_2m,apparent_temperature,rain,snowfall"

def get_weather_data(latitude, longitude, timezone, date):
    # Konstrukcja URL z parametrami
    url = f"{BASE_URL}?latitude={latitude}&longitude={longitude}&hourly={HOURLY_PARAMETERS}&timezone={timezone}&start_date={date}&end_date={date}"
    return url

def fetch_weather_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print("Błąd podczas próby wykonania zapytania GET:", e)
        return None

def format_response(response_data, selected_hour):
    # Wybierz interesujące dane z odpowiedzi
    hourly_data = response_data.get("hourly", {})
    times = hourly_data.get("time", [])
    temperatures = hourly_data.get("temperature_2m", [])
    apparent_temps = hourly_data.get("apparent_temperature", [])
    rain = hourly_data.get("rain", [])
    snowfall = hourly_data.get("snowfall", [])

    # Przygotuj dane do tabeli tylko dla wybranej godziny
    table = []
    for i in range(len(times)):
        # Sprawdź, czy godzina odpowiada wybranej przez użytkownika
        if selected_hour in times[i]:
            row = [times[i], temperatures[i], apparent_temps[i], rain[i], snowfall[i]]
            table.append(row)

    # Drukowanie tabeli za pomocą `tabulate`
    headers = ["Czas", "Temperatura (°C)", "Odczuwalna Temp. (°C)", "Opady deszczu (mm)", "Opady śniegu (cm)"]
    print(tabulate(table, headers=headers, tablefmt="grid"))

def main():
    while True:
        user_input = input("Wpisz 1, aby zobaczyć dane na temat pogody, lub 0, aby zakończyć program: ")

        if user_input == '1':
            # Pobranie szerokości geograficznej
            while True:
                try:
                    latitude = float(input("Wpisz szerokość geograficzną (latitude): "))
                    break
                except ValueError:
                    print("Niepoprawny format. Wprowadź liczbę.")

            # Pobranie długości geograficznej
            while True:
                try:
                    longitude = float(input("Wpisz długość geograficzną (longitude): "))
                    break
                except ValueError:
                    print("Niepoprawny format. Wprowadź liczbę.")

            # Pobranie strefy czasowej
            print("Dostępne strefy czasowe (czas standardowy):")
            print(tabulate(TIME_ZONES.items(), headers=["Time Zone", "UTC Offset"], tablefmt="grid"))

            while True:
                offset = input("Wpisz przesunięcie UTC dostępne w tabeli (np. -3, 0, +3): ")
                if offset in TIME_ZONES.values():
                    timezone = get_timezone_by_offset(offset)
                    break
                else:
                    print("Niepoprawne przesunięcie UTC. Spróbuj ponownie.")

            # Pobranie daty w zakresie tygodnia
            today = datetime.now().date()
            week_later = today + timedelta(days=7)
            while True:
                date_input = input(f"Wpisz datę (RRRR-MM-DD) w zakresie od {today} do {week_later}: ")
                try:
                    selected_date = datetime.strptime(date_input, "%Y-%m-%d").date()
                    if today <= selected_date <= week_later:
                        break
                    else:
                        print(f"Data musi być w zakresie od {today} do {week_later}.")
                except ValueError:
                    print("Niepoprawny format daty. Wprowadź datę w formacie RRRR-MM-DD.")

            # Pobranie godziny
            while True:
                hour_input = input("Wpisz godzinę prognozy (00-23): ")
                if hour_input.isdigit() and 0 <= int(hour_input) <= 23:
                    selected_hour = f"T{hour_input.zfill(2)}:00"
                    break
                else:
                    print("Godzina musi być liczbą od 0 do 23.")

            # Wywołanie funkcji do wygenerowania URL
            url = get_weather_data(latitude, longitude, timezone, selected_date)
            print("Skonstruowany URL:", url)

            # Pobranie danych pogodowych
            weather_data = fetch_weather_data(url)
            if weather_data:
                print(f"Wprowadzono współrzędne: szerokość = {latitude}, długość = {longitude}")
                print(f"Wprowadzona strefa czasowa: {timezone}")

                print("Pogoda dla wybranej daty i godziny:")
                format_response(weather_data, selected_hour)

        elif user_input == '0':
            print("Zamykanie aplikacji.")
            break
        else:
            print("Nieprawidłowy wybór. Wpisz 1 lub 0.")

def get_timezone_by_offset(offset):
    """Zwraca strefę czasową na podstawie przesunięcia UTC."""
    for timezone, utc in TIME_ZONES.items():
        if utc == offset:
            return timezone
    return None

if __name__ == "__main__":
    main()
