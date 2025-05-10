from datetime import datetime
import json
import requests

BASE_URL = 'https://api.coingecko.com/api/v3'

def fetch_bitcoin_price_on_date(date_str):
    """
    Consulta el precio de Bitcoin para una fecha específica utilizando la API de CoinGecko.

    Args:
        date_str (str): Fecha para la cual se desea obtener el precio (YYYY-MM-DD).

    Returns:
        float or None: El precio de cierre de Bitcoin en USD para la fecha especificada,
                       o None si ocurre un error.
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d-%m-%Y')
        url = f'{BASE_URL}/coins/bitcoin/history'
        params = {
            'date': formatted_date
        }
        with requests.Session() as session:
            response = session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if 'market_data' in data and 'current_price' in data['market_data'] and 'usd' in data['market_data']['current_price']:
                return data['market_data']['current_price']['usd']
            return None
    except ValueError:
        print(f"Error: Formato de fecha incorrecto: {date_str}. Use YYYY-MM-DD.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el precio para {date_str}: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error al decodificar la respuesta JSON para {date_str}")
        return None

if __name__ == "__main__":
    # Ejemplo de cómo usar la función directamente desde este archivo
    fecha_a_consultar = input("Ingrese la fecha para consultar el precio de Bitcoin (YYYY-MM-DD): ")
    precio = fetch_bitcoin_price_on_date(fecha_a_consultar)
    if precio is not None:
        print(f"El precio de Bitcoin el {fecha_a_consultar} fue: ${precio:.2f} USD")
    else:
        print(f"No se pudo obtener el precio de Bitcoin para el {fecha_a_consultar}.")