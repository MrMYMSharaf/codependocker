docker build -t streamlit-bocapp . 
docker run --name streamlit-container -p 8501:8501 -d -v ${pwd}:/code streamlit-Bocapp

docker run --env-file .env -p 8501:8501 streamlitboc-app


deepseek:
# Headline: Unlock Exclusive Rewards with Your BOC Premium Card, Tailored Just for You!
# Body: Dear {customer_name}, we’re excited to offer you, as a valued {job_category} professional, an exclusive {discount}% discount at {hotel_name}, 
#       available for full board, half board, and bed & breakfast options. 
#       This limited-time offer is exclusively for BOC Credit & Debit Cardholders in {geolocation} and is valid 
#       from {start_date} to {end_date}. Whether you're planning a weekend escape or a longer retreat, this is your chance to enjoy a luxurious getaway at a special rate, designed with {gender} travelers in mind.
# Call to Action: Apply for your BOC Premium Card now and start enjoying amazing benefits tailored to your lifestyle! 
#                 Visit {link} to apply today and unlock a world of exclusive rewards.

cloudai:
# Headline: Unlock Exclusive Rewards with Your BOC Premium Card!

# Body:
Dear {title} {customer_name},

As a valued {job_category} professional in {city}, {country}, we're excited to offer you an exclusive {discount}% discount at {hotel_name}, available for full board, half board, and bed & breakfast options.

Based on your preferences as a {gender} traveler and your professional background in {industry}, we've curated this special getaway package just for you.

This limited-time offer is exclusively for BOC Credit & Debit Cardholders and is valid from {start_date} to {end_date}. Don't miss this chance to enjoy a luxurious getaway at a special rate that's perfectly suited for {city}-based professionals like yourself.

# Call to Action:
Apply for your BOC Premium Card now and start enjoying amazing benefits tailored to {gender} professionals in {job_category}!

Visit {link} to apply today.

# Dynamic Variables:
- {title}: Mr./Mrs./Ms./Dr.
- {customer_name}: Full name
- {gender}: male/female
- {job_category}: Executive/Medical/Legal/Technology/Finance/etc.
- {industry}: Specific industry sector
- {city}: Customer's city
- {country}: Customer's country
- {discount}: Discount percentage
- {hotel_name}: Partner hotel name
- {start_date}: Offer start date
- {end_date}: Offer end date
- {link}: Application URL

gpt:
# Headline: Unlock Exclusive Rewards with Your BOC Premium Card!

# Body: Dear {gender} {customer_name}, we’re excited to offer you an exclusive {discount}% discount at {hotel_name}, available for full board, half board, and bed & breakfast options. This limited-time offer is exclusively for BOC Credit & Debit Cardholders, and is valid from {start_date} to {end_date}. 

# Additional Information: As a {job_category} in {geolocation}, you deserve a luxurious escape! Don’t miss this chance to enjoy a getaway at a special rate.

# Call to Action: Apply for your BOC Premium Card now and start enjoying amazing benefits! Visit {link} to apply today.


google:

Headline: Unlock Exclusive Rewards with Your BOC Premium Card, [Customer Name]!

Body:

Dear [Customer Name]

We're excited to offer you an exclusive [discount]% discount at [hotel_name] in [city, country], available for full board, half board, and bed & breakfast options. This limited-time offer is exclusively for BOC Credit & Debit Cardholders and is valid from [start_date] to [end_date]. Don't miss this chance to enjoy a luxurious getaway at a special rate, tailored just for you.

[Optional: Include a personalized touch based on gender, geolocation, and job category]

Gender: If you're a [his/her] [job category] in [city, country], this is the perfect opportunity to unwind and recharge.
Geolocation: Enjoy a staycation at the beautiful [hotel_name] in [city, country], just a short trip away from your home in [customer's city, country].
Job Category: As a busy [job category] in [city, country], you deserve a break. Treat yourself to a relaxing stay at [hotel_name].
Call to Action: Apply for your BOC Premium Card now and start enjoying amazing benefits! Visit [link] to apply today.
