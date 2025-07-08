import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import boto3
import os
from dotenv import load_dotenv

# Load AWS credentials
load_dotenv()
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")
bucket_name = "booking-hotel-rates"

cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
    "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
    "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington",
    "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City",
    "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

today = datetime.today()


def extract_data():
    all_data = []
    for city in cities:
        for i in range(1, 8):  # next 7 days
            checkin = (today + timedelta(days=i)).strftime("%Y-%m-%d")
            checkout = (today + timedelta(days=i + 1)).strftime("%Y-%m-%d")

            url = (
                f"https://www.booking.com/searchresults.html?"
                f"ss={city}&checkin={checkin}&checkout={checkout}&group_adults=1&no_rooms=1&group_children=0"
            )
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.find_all("div", attrs={"data-testid": "property-card"})

            for card in cards[:5]:  # Top 5 only
                name_tag = card.find("div", attrs={"data-testid": "title"})
                price_tag = card.find("span", attrs={"data-testid": "price-and-discounted-price"}) or \
                        card.find("span", attrs={"data-testid": "price"})
                hotel_name = name_tag.get_text(strip=True) if name_tag else None

                if price_tag:
                    raw_price = price_tag.get_text(strip=True)
                    # Remove currency symbols like "US$", "$", and any commas
                    raw_price = raw_price.replace("US$", "").replace("$", "").replace(",", "")
                    try:
                        price = float(raw_price)
                    except ValueError:
                        price = None
                else:
                    price = None


                all_data.append({
                    "city": city,
                    "hotel_name": hotel_name,
                    "date_of_stay": checkin,
                    "price": price,
                    "scraped_date": today.strftime("%Y-%m-%d")
                })

            time.sleep(1)
    return pd.DataFrame(all_data)


def transform_data(df):

    df['date_of_stay'] = pd.to_datetime(df['date_of_stay'])
    df['scraped_date'] = pd.to_datetime(df['scraped_date'])

    daily_avg = (
        df.groupby(['city', 'date_of_stay', 'scraped_date'])['price']
        .mean().reset_index()
    )
    daily_avg.rename(columns={'price': 'average_price'}, inplace=True)
    return daily_avg


def upload_to_s3(local_file, bucket, s3_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )
    s3.upload_file(local_file, bucket, s3_key)
    print(f"✅ Uploaded {local_file} to s3://{bucket}/{s3_key}")


def main():
    df_raw = extract_data()
    # print("Columns in df_raw:", df_raw.columns.tolist())
    output_raw_file = f"{today.strftime('%Y-%m-%d')}.csv"
    df_raw.to_csv(output_raw_file, index = False)
    
    df_transformed = transform_data(df_raw)
    output_processed_file = f"daily_avg_rates_{today.strftime('%Y-%m-%d')}.csv"
    df_transformed.to_csv(output_processed_file, index=False)

    upload_to_s3(output_raw_file, bucket_name, f"raw/{output_raw_file}")
    upload_to_s3(output_processed_file, bucket_name, f"processed/{output_processed_file}")


if __name__ == "__main__":
    main()
