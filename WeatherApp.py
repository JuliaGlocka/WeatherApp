import requests
from tabulate import tabulate

# URL i nagłówki
BASE_URL = "https://api.open-meteo.com/v1/forecast"
HOURLY_PARAMETERS = "temperature_2m,apparent_temperature,rain,snowfall,visibility"


def get_weather_data(latitude, longitude, timezone, forecast_days):
    # Konstrukcja URL z parametrami
    url = f"{BASE_URL}?latitude={latitude}&longitude={longitude}&hourly={HOURLY_PARAMETERS}&timezone={timezone}&forecast_days={forecast_days}"
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


def format_response(response_data):
    # Wybierz interesujące dane z odpowiedzi
    hourly_data = response_data.get("hourly", {})
    times = hourly_data.get("time", [])
    temperatures = hourly_data.get("temperature_2m", [])
    apparent_temps = hourly_data.get("apparent_temperature", [])
    visibilities = hourly_data.get("visibility", [])
    rain = hourly_data.get("rain", [])
    snowfall = hourly_data.get("snowfall", [])

    # Przygotuj dane do tabeli
    table = []
    for i in range(len(times)):
        row = [times[i], temperatures[i], apparent_temps[i], visibilities[i], rain[i], snowfall[i]]
        table.append(row)

    # Drukowanie tabeli za pomocą `tabulate`
    headers = ["Czas", "Temperatura (°C)", "Odczuwalna Temp. (°C)", "Widoczność (m)", "Opady deszczu (mm)",
               "Opady śniegu (cm)"]
    print(tabulate(table, headers=headers, tablefmt="grid"))


def main():
    while True:
        user_input = input("Wpisz 1, aby zobaczyć dane na temat dzisiejszej pogody, lub 0, aby zakończyć program: ")

        if user_input == '1':
            # Pobranie szerokości geograficznej
            while True:
                try:
                    latitude = float(input("Wpisz szerokość geograficzną (latitude): "))
                    break  # Wyjdź z pętli, jeśli wartość jest poprawna
                except ValueError:
                    print("Niepoprawny format. Wprowadź liczbę.")

            # Pobranie długości geograficznej
            while True:
                try:
                    longitude = float(input("Wpisz długość geograficzną (longitude): "))
                    break  # Wyjdź z pętli, jeśli wartość jest poprawna
                except ValueError:
                    print("Niepoprawny format. Wprowadź liczbę.")

            # Pobranie strefy czasowej
            valid_timezones = [
                "America/Anchorage", "America/Los_Angeles", "America/Denver",
                "America/Chicago", "America/New_York", "America/Sao_Paulo",
                "Europe/London", "Europe/Berlin", "Europe/Moscow",
                "Africa/Cairo", "Asia/Bangkok", "Asia/Singapore",
                "Asia/Tokyo", "Australia/Sydney", "Pacific/Auckland"
            ]
            while True:
                timezone = input("Wpisz jedną ze stref czasowych:\n" + "\n".join(valid_timezones) + "\n")
                if timezone in valid_timezones:
                    break
                else:
                    print("Niepoprawna strefa czasowa. Spróbuj ponownie.")

            # Pobranie liczby dni prognozy
            while True:
                try:
                    forecast_days = int(input("Wpisz liczbę dni prognozy (forecast days) maksymalna liczba dni to 16: "))
                    if forecast_days > 0:
                        break  # Wyjdź z pętli, jeśli wartość jest poprawna
                    else:
                        print("Liczba dni prognozy musi być większa od 0.")
                except ValueError:
                    print("Niepoprawny format. Wprowadź liczbę całkowitą.")

            # Wywołanie funkcji do wygenerowania URL
            url = get_weather_data(latitude, longitude, timezone, forecast_days)
            print("Skonstruowany URL:", url)

            # Pobranie danych pogodowych
            weather_data = fetch_weather_data(url)
            if weather_data:
                # Informacje o wprowadzonych danych
                print(f"Wprowadzono współrzędne: szerokość = {latitude}, długość = {longitude}")
                print(f"Wprowadzona strefa czasowa: {timezone}")

                print("Pogoda na wybrany okres:")
                format_response(weather_data)

        elif user_input == '0':
            print("Zamykanie aplikacji.")
            break
        else:
            print("Nieprawidłowy wybór. Wpisz 1 lub 0.")


if __name__ == "__main__":
    main()
