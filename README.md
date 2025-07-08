# hotel-rates-pipelineHotel Rates Data Pipeline
A Python-based data pipeline that scrapes hotel rate data from major US cities to serve as an additional regressor for restaurant demand prediction at ClearCOGS.

Overview
This pipeline collects daily hotel pricing data from Booking.com across 30 major US cities, processes it into aggregated metrics, and stores the results in AWS S3. The data serves as an external economic indicator to enhance restaurant demand forecasting models by capturing tourism and business travel patterns that correlate with dining activity.

Features
Automated Data Collection: Scrapes hotel rates for the next 7 days across 30 major US cities
Data Processing: Aggregates individual hotel prices into daily city-level averages
AWS Integration: Automatically uploads both raw and processed data to S3
Robust Scraping: Handles various price formats and missing data gracefully
Rate Limiting: Implements delays to respect website terms of service
Cities Covered
The pipeline monitors hotel rates in these 30 major US cities:

New York, Los Angeles, Chicago, Houston, Phoenix
Philadelphia, San Antonio, San Diego, Dallas, San Jose
Austin, Jacksonville, Fort Worth, Columbus, Charlotte
San Francisco, Indianapolis, Seattle, Denver, Washington
Boston, El Paso, Nashville, Detroit, Oklahoma City
Portland, Las Vegas, Memphis, Louisville, Baltimore
Data Schema
Raw Data (raw/YYYY-MM-DD.csv)
city: City name
hotel_name: Name of the hotel
date_of_stay: Check-in date
price: Hotel rate per night (USD)
scraped_date: Date when data was collected
Processed Data (processed/daily_avg_rates_YYYY-MM-DD.csv)
city: City name
date_of_stay: Check-in date
scraped_date: Date when data was collected
average_price: Average hotel rate for the city on that date
Setup
Prerequisites
Python 3.7+
AWS account with S3 access
Required Python packages (see requirements below)
Installation
Clone the repository:
bash
git clone https://github.com/yourusername/hotel-rates-pipeline.git
cd hotel-rates-pipeline
Install required packages:
bash
pip install requests beautifulsoup4 pandas boto3 python-dotenv
Set up environment variables: Create a .env file in the root directory:
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
Create S3 bucket: Ensure you have an S3 bucket named booking-hotel-rates (or modify the bucket name in the script)
Usage
Run the pipeline:

bash
python hotel-rates-pipeline.py
The script will:

Scrape hotel data for the next 7 days across all cities
Process the data into daily averages
Save both raw and processed data locally
Upload files to S3 in respective folders
S3 Structure
booking-hotel-rates/
├── raw/
│   └── YYYY-MM-DD.csv
└── processed/
    └── daily_avg_rates_YYYY-MM-DD.csv
Integration with Restaurant Demand Prediction
This data serves as an external regressor in ClearCOGS' restaurant demand forecasting models by:

Capturing tourism patterns that affect dining demand
Providing economic indicators for business travel
Offering city-level activity metrics for location-based predictions
Ethical Considerations
Implements rate limiting to respect website resources
Follows robots.txt guidelines
Uses appropriate User-Agent headers
Collects only publicly available pricing information
Future Enhancements
Add support for additional cities
Implement data quality checks and validation
Add scheduling capabilities (cron jobs, AWS Lambda)
Include additional hotel metadata (ratings, amenities)
Add error handling and retry logic
Implement data freshness monitoring
Contributing
Fork the repository
Create a feature branch
Make your changes
Add tests if applicable
Submit a pull request
License
This project is licensed under the MIT License - see the LICENSE file for details.

Disclaimer
This tool is for educational and research purposes. Please ensure compliance with website terms of service and applicable laws when using this scraper.

