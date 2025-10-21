# WeatherApp - Weather Forecast CLI Application

## 📌 Project Overview

A Python-based command-line weather forecast application that integrates Open-Meteo API with PostgreSQL for location-based weather queries. The application supports both city name searches and direct geographic coordinate inputs, with comprehensive timezone support across 15 global regions.

**A production-ready weather forecast CLI tool built with Python 3 and PostgreSQL, demonstrating API integration, database operations, and interactive user experience design. The application leverages the Open-Meteo public weather API for 16-day forecast data, combining it with a PostgreSQL city database for intelligent location resolution that supports both local and English city names through case-insensitive pattern matching.**

**The architecture implements clean separation between data retrieval (API layer), data persistence (PostgreSQL integration), and presentation (tabulate-formatted console output). Timezone handling spans 15 global regions with UTC offset mapping, enabling accurate weather queries across Americas, Europe, Africa, Asia, and Pacific zones. The city lookup system uses PostgreSQL's `ILIKE` and `string_to_array` functions for flexible multi-language search, allowing users to input cities in their native language or English equivalent.**

**Core functionality includes hourly weather parameter retrieval (temperature, apparent temperature, rainfall, snowfall) with date range validation (today + 15 days ahead) and hour-specific forecast filtering. The request builder constructs RESTful API URLs with proper query parameter encoding, while comprehensive error handling manages network failures, invalid coordinates, and database connection issues. User input validation ensures type safety for floats (coordinates), strings (dates in YYYY-MM-DD format), and integers (hour selection 00-23).**

**The application features an intuitive menu-driven interface with dual search modes (city name vs. coordinates), tabular timezone selection with UTC offset display, and formatted weather output using the tabulate library for enhanced readability. PostgreSQL integration via psycopg2 enables persistent city data storage, supporting scalable location databases without API rate limits. The modular design with single-responsibility functions (fetch, format, validate) promotes maintainability and testability, following Python best practices for CLI application development.**

---

## 🎯 Key Features

### Weather Data Retrieval
- **Multi-Parameter Forecasts**: Temperature, apparent temperature, rainfall, and snowfall
- **Hourly Precision**: Select specific hours (00-23) for targeted forecasts
- **16-Day Range**: Query weather from today up to 15 days ahead
- **Open-Meteo Integration**: Reliable public API with no authentication required

### Location Intelligence
- **Dual Search Modes**: 
  - City name lookup (supports local and English names)
  - Direct latitude/longitude coordinates
- **PostgreSQL City Database**: Fast local lookups without API calls
- **Multi-Language Support**: Case-insensitive matching for international cities

### Timezone Management
- **15 Global Timezones**: From UTC-9 (Alaska) to UTC+13 (Auckland)
- **Automatic UTC Conversion**: Timezone-aware API requests
- **Visual Timezone Table**: Easy selection with formatted display

### User Experience
- **Interactive CLI**: Menu-driven navigation
- **Input Validation**: Type checking and range validation
- **Formatted Output**: Grid-style tables using tabulate library
- **Error Handling**: Graceful handling of network and database errors

---

## 🛠️ Technologies

- **Python 3.x**
- **requests** - HTTP client for API communication
- **tabulate** - Table formatting for console output
- **psycopg2** - PostgreSQL database adapter
- **PostgreSQL** - City coordinates database
- **Open-Meteo API** - Weather data provider

---

## 📂 Project Structure

```
WeatherApp/
├── WeatherApp.py          # Main application file
├── README.md              # Project documentation
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies (to be created)
└── database/             # Database setup scripts (to be created)
    └── cities.sql        # City data initialization
```

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.7+**
2. **PostgreSQL 12+**
3. **pip** (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/JuliaGlocka/WeatherApp
cd WeatherApp
```

2. **Install Python dependencies**
```bash
pip install requests tabulate psycopg2-binary
```

Or create `requirements.txt`:
```txt
requests>=2.31.0
tabulate>=0.9.0
psycopg2-binary>=2.9.0
```

Then install:
```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL Database**

Create database:
```sql
CREATE DATABASE weather_forecast;
```

Create cities table:
```sql
\c weather_forecast

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL
);

-- Example data (add more cities as needed)
INSERT INTO cities (city, latitude, longitude) VALUES
('Warsaw Warszawa', 52.2297700, 21.0117800),
('London', 51.5074, -0.1278),
('New York', 40.7128, -74.0060),
('Tokyo 東京', 35.6762, 139.6503),
('Paris', 48.8566, 2.3522);
```

4. **Configure Database Connection**

Update database credentials in `WeatherApp.py`:
```python
def connect_db():
    return psycopg2.connect(
        dbname="weather_forecast",
        user="your_username",      # Change this
        password="your_password",  # Change this
        host="localhost",
        port="5432"
    )
```

### Running the Application

```bash
python WeatherApp.py
```

---

## 📖 Usage Guide

### Starting the Application

```
Wpisz 1, aby zobaczyć dane na temat pogody, lub 0, aby zakończyć program: 1
```

### Option 1: Search by City Name

```
Wpisz 1, aby podać nazwę miasta lub 2, aby podać współrzędne geograficzne: 1
Wpisz nazwę miasta (lokalna lub angielska): Warsaw
```

**Supports:**
- English names: `London`, `New York`, `Tokyo`
- Local names: `Warszawa`, `東京`, `Paris`
- Partial matches: `War` matches `Warsaw`

### Option 2: Search by Coordinates

```
Wpisz 1, aby podać nazwę miasta lub 2, aby podać współrzędne geograficzne: 2
Wpisz szerokość geograficzną (latitude): 52.2297
Wpisz długość geograficzną (longitude): 21.0118
```

### Select Timezone

The app displays available timezones:
```
╒════════════════════════╤═══════════════════╕
│ Strefa Czasowa         │ Przesunięcie UTC  │
╞════════════════════════╪═══════════════════╡
│ America/Anchorage      │ -9                │
│ America/Los_Angeles    │ -8                │
│ Europe/Berlin          │ +1                │
│ Asia/Tokyo             │ +9                │
╘════════════════════════╧═══════════════════╛

Wpisz przesunięcie UTC dostępne w tabeli (np. -3, 0, +3): +1
```

### Select Date and Hour

```
Wpisz datę (RRRR-MM-DD) w zakresie od 2025-10-21 do 2025-11-05: 2025-10-22
Wpisz godzinę prognozy (00-23): 14
```

### View Results

```
╒════════════════════╤═══════════════════╤═══════════════════════════╤════════════════════════╤═══════════════════════╕
│ Czas               │ Temperatura (°C)  │ Odczuwalna Temp. (°C)     │ Opady deszczu (mm)     │ Opady śniegu (cm)     │
╞════════════════════╪═══════════════════╪═══════════════════════════╪════════════════════════╪═══════════════════════╡
│ 2025-10-22T14:00   │ 15.2              │ 13.8                      │ 0.0                    │ 0.0                   │
╘════════════════════╧═══════════════════╧═══════════════════════════╧════════════════════════╧═══════════════════════╛
```

---

## 🔧 Code Architecture

### Main Components

```python
# Database Connection
connect_db()                           # PostgreSQL connection management

# API Integration
get_weather_data()                     # URL builder for Open-Meteo API
fetch_weather_data()                   # HTTP GET request handler

# Data Processing
format_response()                      # Tabulate formatter
get_timezone_by_offset()              # Timezone resolver

# User Input
get_user_input()                       # Validated input handler
get_coordinates_from_city()           # Database city lookup

# Main Flow
main()                                 # Interactive menu loop
```

### Key Functions

#### Database City Lookup
```python
def get_coordinates_from_city(city_name):
    """Flexible city search supporting multiple languages."""
    cur.execute(
        """
        SELECT latitude, longitude
        FROM cities
        WHERE %s ILIKE ANY(string_to_array(city, ' '))
        """,
        (city_name,)
    )
```

#### API URL Construction
```python
def get_weather_data(latitude, longitude, timezone, date):
    """Generates GET URL with proper parameter encoding."""
    return f"{BASE_URL}?latitude={latitude}&longitude={longitude}" \
           f"&hourly={HOURLY_PARAMETERS}&timezone={timezone}" \
           f"&start_date={date}&end_date={date}"
```

#### Input Validation
```python
def get_user_input(prompt, valid_type=float):
    """Type-safe input with retry logic."""
    while True:
        try:
            return valid_type(user_input)
        except ValueError:
            print("Niepoprawny format. Spróbuj ponownie.")
```

---

## 🌍 Supported Timezones

| Region | Timezone | UTC Offset |
|--------|----------|------------|
| Alaska | America/Anchorage | -9 |
| Los Angeles | America/Los_Angeles | -8 |
| Denver | America/Denver | -7 |
| Chicago | America/Chicago | -6 |
| New York | America/New_York | -5 |
| São Paulo | America/Sao_Paulo | -3 |
| London | Europe/London | 0 |
| Berlin | Europe/Berlin | +1 |
| Cairo | Africa/Cairo | +2 |
| Moscow | Europe/Moscow | +3 |
| Bangkok | Asia/Bangkok | +7 |
| Singapore | Asia/Singapore | +8 |
| Tokyo | Asia/Tokyo | +9 |
| Sydney | Australia/Sydney | +11 |
| Auckland | Pacific/Auckland | +13 |

---

## 📊 Weather Parameters

| Parameter | Unit | Description |
|-----------|------|-------------|
| Temperature | °C | Air temperature at 2 meters above ground |
| Apparent Temperature | °C | Feels-like temperature (wind chill/heat index) |
| Rainfall | mm | Precipitation as rain |
| Snowfall | cm | Precipitation as snow |

---

## 🚧 Current Limitations & Future Enhancements

### Known Limitations
- **Hardcoded Database Credentials**: Needs environment variable configuration
- **Limited City Database**: Requires manual population
- **Polish-Only UI**: Interface text hardcoded in Polish
- **No Configuration File**: Settings embedded in code
- **Single-User Design**: No concurrent user support

### Planned Enhancements

**Short-term:**
- [ ] Move database credentials to `.env` file
- [ ] Add `requirements.txt` with pinned versions
- [ ] Create database initialization script (`cities.sql`)
- [ ] Add error logging to file
- [ ] Implement multi-language UI (English, Polish)

**Medium-term:**
- [ ] Add weather condition descriptions (sunny, cloudy, etc.)
- [ ] Support multiple date queries in one session
- [ ] Add data export to CSV/JSON
- [ ] Implement caching for repeated API calls
- [ ] Add city autocomplete suggestions

**Long-term:**
- [ ] Build GUI with Tkinter or PyQt
- [ ] Add weather alerts and notifications
- [ ] Implement historical weather data queries
- [ ] Create REST API wrapper
- [ ] Add weather visualization (charts/graphs)
- [ ] Support weather comparison between cities

---

## 🔐 Security Considerations

**Current Issues:**
- ⚠️ Database password in plaintext
- ⚠️ No input sanitization for SQL (uses parameterized queries, but limited validation)
- ⚠️ No API rate limiting

**Recommendations:**
```python
# Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost")
    )
```

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] Valid city name lookup (English)
- [ ] Valid city name lookup (local language)
- [ ] Invalid city name handling
- [ ] Valid coordinate input
- [ ] Invalid coordinate input (letters, out of range)
- [ ] All 15 timezones
- [ ] Date validation (past dates, future dates beyond 15 days)
- [ ] Hour validation (negative, >23, letters)
- [ ] Network error simulation (disconnect internet)
- [ ] Database connection error (wrong credentials)

### Future: Automated Tests

```python
# Example unit test structure
import unittest

class TestWeatherApp(unittest.TestCase):
    def test_timezone_lookup(self):
        result = get_timezone_by_offset("+1")
        self.assertEqual(result, "Europe/Berlin")
    
    def test_invalid_offset(self):
        result = get_timezone_by_offset("+99")
        self.assertIsNone(result)
```

---

## 📝 Configuration

### Creating `.env` File (Recommended)

```bash
# Database Configuration
DB_NAME=weather_forecast
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# API Configuration (future use)
OPENMETEO_API_URL=https://api.open-meteo.com/v1/forecast
```

---

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Add tests for new functionality
4. Ensure code follows PEP 8 style guide
5. Commit changes (`git commit -m 'Add AmazingFeature'`)
6. Push to branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 📞 Contact

**Julia Głocka**
- Email: glockajulia@gmail.com
- GitHub: [@JuliaGlocka](https://github.com/JuliaGlocka)
- LinkedIn: [Connect with me](https://linkedin.com/in/julia-glocka)

---

## 🙏 Acknowledgments

- [Open-Meteo](https://open-meteo.com/) - Free weather API
- [tabulate](https://github.com/astanin/python-tabulate) - Python table formatting
- [psycopg2](https://www.psycopg.org/) - PostgreSQL adapter for Python

---

## 📚 Additional Resources

- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python Requests Library](https://requests.readthedocs.io/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
