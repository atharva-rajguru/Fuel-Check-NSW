import requests
import pandas as pd
import datetime
import time
import os
import json
import warnings
import sys
warnings.filterwarnings("ignore", category=DeprecationWarning, module="paho")

def activate():
    # To get the current date and time
    def timer():
        now = datetime.datetime.now()
        formatted = now.strftime("%d/%m/%Y %I:%M:%S %p")
        return formatted

    # Creates folder if does not exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Function to get the access token and other details
    def outh():
        now = datetime.datetime.now()
        formatted = now.strftime("%d/%m/%Y %I:%M:%S %p")
        # Establish connection
        grant_type = 'client_credentials'
        authorization = 'Basic SzE4dkduU3ZEU2EwR3I3c21QYmxzUUxNMWcwSFZIYWo6azQ3d0pnempzSnZYN05BNA=='
        url = f"https://api.onegov.nsw.gov.au/oauth/client_credential/accesstoken"

        params = {
            "grant_type": f"{grant_type}"
        }

        headers = {
                    "Accept":"application/json",
                    "Authorization": f"{authorization}"
                }

        resp = requests.get(url, params=params, headers=headers)

        resp.raise_for_status()
        output = resp.json()

        access_token = 'Bearer ' + (output.get('access_token',''))
        api_key = (output.get('client_id',''))
        content_type = 'application/json; charset=utf-8'
        transactionid = 'transact_id_activity-10_group-10'
        requesttimestamp = f'{formatted}'
        requesttimestamp_modified = f'{formatted}'

        return access_token, api_key, content_type, transactionid, requesttimestamp, requesttimestamp_modified

    
    # Call function for outh
    access_token, api_key, content_type, transactionid, requesttimestamp, requesttimestamp_modified = outh()


    # get time for logging
    formatted = timer()


    ## Fetch data for prices
    url_prices = 'https://api.onegov.nsw.gov.au/FuelPriceCheck/v1/fuel/prices'
    headers={
            'accept': 'application/json',
            'Authorization': f'{access_token}',
            'Content-Type': f'{content_type}',
            'apikey': f'{api_key}',
            'transactionid': f'{transactionid}',
            'requesttimestamp': f'{requesttimestamp}',
    }


    response2 = requests.get(url_prices, headers=headers)
    response2.raise_for_status()
    data = response2.json()

    # DataFrame for Prices details
    prices = data.get('prices',{})
    station_code = []
    fuel_type = []
    price = []
    last_updated = []
    for i in prices:
        station_code.append(i.get('stationcode',''))
        fuel_type.append(i.get('fueltype',''))
        price.append(i.get('price',))
        last_updated.append(i.get('lastupdated',''))

    prices = pd.DataFrame({
        'station_code': station_code,
        'fuel_type': fuel_type,
        'price': price,
        'last_updated': last_updated
    })

    # DataFrame for station details
    stations = data.get('stations',{})
    brandid = []
    stationid = []
    brand = []
    code = []
    name = []
    address = []
    isAdBlueAvailable = []
    latitude = []
    longitude = []
    stations = data.get('stations',{})
    for i in stations:
        brandid.append(i.get('brandid',''))
        stationid.append(i.get('stationid',''))
        brand.append(i.get('brand',''))
        code.append(i.get('code',''))
        name.append(i.get('name',''))
        address.append(i.get('address',''))
        lat_long = i.get('location',{})
        latitude.append(lat_long.get('latitude',''))
        longitude.append(lat_long.get('longitude',''))
        isAdBlueAvailable.append(i.get('isAdBlueAvailable',))


    # Creating DataFrame
    station_details = pd.DataFrame({
        'brandid': brandid,
        'stationid': stationid,
        'brand': brand,
        'code': code,
        'name': name,
        'address': address,
        'latitude': latitude,
        'longitude': longitude,
        'isAdBlueAvailable': isAdBlueAvailable})
        

    # merging dataframes
    df_outer_old = pd.merge(
        prices,
        station_details,
        right_on="code",
        left_on="station_code",
        how="outer")
    # Data cleaning for prices dataframe
    df_outer_old['last_updated'] = pd.to_datetime(df_outer_old['last_updated'], dayfirst=True, errors='coerce')
    df_outer_old['last_updated'] = df_outer_old['last_updated'].dt.strftime('%d/%m/%Y %I:%M:%S %p')
    df_outer_old.drop('code',axis=1,inplace=True)

    # Saving DataFreame to CSV
    old_file = df_outer_old
    old_file.to_csv('data/all_data.csv', index=False)
    old_file.to_csv('data/overall.csv', index=False)
    
    start_time = time.time()
    time_limit = 15 * 60

    # import requests
    print('Loop initiated.\n')
    while True:
        # get time for logging
        formatted = timer()

        # Call function for outh
        access_token, api_key, content_type, transactionid, requesttimestamp, requesttimestamp_modified = outh()

        # fetch data
        url_station_prices = "https://api.onegov.nsw.gov.au/FuelPriceCheck/v1/fuel/prices/new"
        headers = {
                    "Accept":"application/json",
                    "Authorization":f'{access_token}',
                    "Content-Type":f'{content_type}',
                    "apikey":f'{api_key}',
                    "transactionid":f'{transactionid}',
                    "requesttimestamp":f'{requesttimestamp}'
                }
        response2 = requests.get(url_station_prices, headers=headers)
        data = response2.json()

        # DataFrame for Stations details

        stations = data.get('stations', [])
        if data.get('stations', []) == [] and data.get('prices', []) == []:
            print(f'No data is updated yet! Logged at:{formatted}\n')
        else:
            brandid = []
            stationid = []
            brand = []
            code = []
            name = []
            address = []
            isAdBlueAvailable = []
            latitude = []
            longitude = []

            for i in stations:
                brandid.append(i.get('brandid',''))
                stationid.append(i.get('stationid',''))
                brand.append(i.get('brand',''))
                code.append(i.get('code',''))
                name.append(i.get('name',''))
                address.append(i.get('address',''))
                lat_long = i.get('location',{})
                latitude.append(lat_long.get('latitude',''))
                longitude.append(lat_long.get('longitude',''))
                isAdBlueAvailable.append(i.get('isAdBlueAvailable',))
            
            df_station = pd.DataFrame({
                'brandid': brandid,
                'stationid': stationid,
                'brand': brand,
                'code': code,
                'name': name,
                'address': address,
                'latitude': latitude,
                'longitude': longitude,
                'isAdBlueAvailable': isAdBlueAvailable
            })

            # DataFrame for Prices details
            prices = data.get('prices', [])
            station_code = []
            fuel_type = []
            price = []
            last_updated = []
            for k in prices:
                station_code.append(k.get('stationcode',''))
                fuel_type.append(k.get('fueltype',''))
                price.append(k.get('price',))
                last_updated.append(k.get('lastupdated',''))

            df_price = pd.DataFrame({
                'station_code': station_code,
                'fuel_type': fuel_type,
                'price': price,
                'last_updated': last_updated
            })
            # merging dataframes
            df_outer_new = pd.merge(
            df_price,
            df_station,
            right_on="code",
            left_on="station_code",
            how="outer")
            
            
            

            # Data cleaning for prices dataframe
            df_outer_new['last_updated'] = pd.to_datetime(df_outer_new['last_updated'], dayfirst=True, errors='coerce')
            df_outer_new['last_updated'] = df_outer_new['last_updated'].dt.strftime('%d/%m/%Y %I:%M:%S %p')
            df_outer_new['station_code']=df_outer_new['code']
            df_outer_new.drop ('code',axis=1,inplace=True)

            # Fetching the brandid and station id
            bid = ''
            sid = ''
            check = []
            tracer = df_outer_new['station_code']
            for i in tracer:
                if i not in check:
                    check.append(i)

            for z in check:
                k = 0
                while k < len(df_outer_old):
                    if df_outer_old['station_code'][k] == z:
                        bid = df_outer_old['brandid'][k]
                        sid = df_outer_old['stationid'][k]
                        h = 0
                        while h < len(df_outer_new):
                            if df_outer_new['station_code'][h] == z:
                                df_outer_new.loc[h, 'brandid']   = bid
                                df_outer_new.loc[h, 'stationid'] = sid
                            h+=1
                        break
                    k+=1
            
            print(df_outer_new)

            # Saving DataFreame to CSV
            df_outer_new.to_csv('data/all_data.csv',mode = 'a', header = False, index=False)
            # This will replace old prices with new ones
            all_data = pd.read_csv('data/overall.csv')
            unq = df_outer_new['stationid'].unique()
            filtered = all_data[~all_data['stationid'].isin(unq)]
            final = pd.concat([filtered, df_outer_new])
            final.to_csv('data/overall.csv', index=False)
            break

            

        break

if __name__ == "__main__":
    activate()
