from datetime import datetime, timedelta
import json
import requests
import time

BASE_URL = 'https://api.coingecko.com/api/v3'
CONSULTAS_POR_BLOQUE = 5
TIEMPO_DE_ESPERA = 5  # Segundos

def fetch_bitcoin_price_coingecko(date_str, session):
    """
    Consulta el precio de Bitcoin para un día específico utilizando la API de CoinGecko.

    Args:
        date_str (str): Fecha para la cual se desea obtener el precio (YYYY-MM-DD).
        session (requests.Session): Sesión de requests para mantener la conexión.

    Returns:
        float or None: El precio de cierre de Bitcoin en USD para la fecha especificada,
                       o None si ocurre un error.
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d-%m-%Y')
    url = f'{BASE_URL}/coins/bitcoin/history'
    params = {
        'date': formatted_date
    }
    try:
        response = session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'market_data' in data and 'current_price' in data['market_data'] and 'usd' in data['market_data']['current_price']:
            return data['market_data']['current_price']['usd']
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el precio para {date_str}: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error al decodificar la respuesta JSON para {date_str}")
        return None

def get_bitcoin_prices_by_range_coingecko(start_date_str, end_date_str):
    """
    Obtiene los precios de Bitcoin para un rango de fechas de hasta 5 días utilizando la API de CoinGecko,
    realizando bloques de 5 consultas seguidas, seguidos de una pausa de 5 segundos.

    Args:
        start_date_str (str): Fecha de inicio del rango (YYYY-MM-DD).
        end_date_str (str): Fecha de fin del rango (YYYY-MM-DD).

    Returns:
        dict or None: Un diccionario donde las claves son las fechas (YYYY-MM-DD)
                     y los valores son los precios de Bitcoin en USD para ese día.
                     Retorna None si el rango de fechas excede los 5 días o si hay un
                     error en el formato de las fechas.
    """
    prices = {}
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        delta = end_date - start_date
        if delta.days > 4:
            print("Error: El rango de fechas no puede exceder los 5 días.")
            return None

        current_date = start_date
        consulta_contador = 0

        with requests.Session() as session:
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                price = fetch_bitcoin_price_coingecko(date_str, session)
                if price is not None:
                    prices[date_str] = price

                consulta_contador += 1
                current_date += timedelta(days=1)

                if consulta_contador % CONSULTAS_POR_BLOQUE == 0 and current_date <= end_date:
                    print(f"Realizadas {CONSULTAS_POR_BLOQUE} consultas. Durmiendo {TIEMPO_DE_ESPERA} segundos...")
                    time.sleep(TIEMPO_DE_ESPERA)

    except ValueError:
        print("Error en el formato de las fechas. Use YYYY-MM-DD.")
        return None
    return prices

if __name__ == "__main__":
    print("Bienvenido al programa de consulta de precios de Bitcoin.")
    print("El Rango maximo de consulta es de 5 dias.")
    start_date = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    end_date = input("Ingrese la fecha de fin (YYYY-MM-DD): ")

    bitcoin_prices_range = get_bitcoin_prices_by_range_coingecko(start_date, end_date)

    if bitcoin_prices_range:
        print("\n--- Precios de Bitcoin por día (CoinGecko) ---")
        print(json.dumps(bitcoin_prices_range, indent=2))
    else:
        print("No se pudieron obtener los precios de Bitcoin para el rango de fechas especificado usando CoinGecko.")