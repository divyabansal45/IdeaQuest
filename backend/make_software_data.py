"""
make_software_data.py  --  builds backend/indian_software.csv from the list below.

The list is written by hand: well-known websites, apps and startups from India,
one short description each. To add more, add a line to ROWS and run:
    python3 backend/make_software_data.py
Format of a row:  name | category | what it does | year founded (blank if unsure)
"""
import csv
import os

ROWS = """
Multibhashi|Language learning|Learn Indian and foreign languages online with lessons, audio, pronunciation and live classes for spoken language practice|
Hello English|Language learning|Learn English speaking app for Hindi speakers with lessons, audio, pronunciation, vocabulary meanings and conversation practice|
Shabdkosh|Language learning|English Hindi online dictionary with word meanings, translation and pronunciation|
Rekhta|Language learning|Website for Urdu poetry and literature with word meanings in Hindi, Urdu and English|
Bhashini|Language technology|Government national language translation platform with speech to text, text to speech and translation across Indian languages|
Anuvadini|Language technology|AI translation tool by AICTE to translate text and documents between Indian languages|
Sarvam AI|Language technology|Indian language AI models for speech, text, translation and voice assistants|
Reverie Language Technologies|Language technology|Indian language localisation, translation, keyboard and speech tools for apps and websites|
Gnani.ai|Language technology|Voice AI and speech recognition in Indian languages for customer support calls|
Skit.ai|Language technology|Voice assistants for customer calls that understand Indian languages and accents|
Pratilipi|Content and media|Platform to read and publish stories, novels and poems in Indian languages|
Kuku FM|Content and media|Audiobooks and audio series in Hindi and other Indian languages|
Dailyhunt|Content and media|News and books app with content in many Indian languages|
ShareChat|Social media|Social network for Indian language users to share posts, videos and chat|
Moj|Social media|Short video app in Indian languages with creators and filters|
Josh|Social media|Short video app for Indian creators with music and trends|
Chingari|Social media|Short video sharing app from India|
Roposo|Social media|Short video and social shopping app from India|
Byju's|Education|Online learning app with video lessons for school students and exam preparation|
Unacademy|Education|Online platform with live classes for competitive exam preparation|
PhysicsWallah|Education|Low cost online coaching with video lectures for JEE and NEET preparation|
Vedantu|Education|Live online tutoring and classes for school students|
upGrad|Education|Online degrees and courses for working professionals|
Toppr|Education|Learning app with practice questions and doubt solving for school students|
Doubtnut|Education|App where students take a photo of a question and get a video solution|
Embibe|Education|Exam preparation app with practice tests and learning analytics|
Teachmint|Education|Tools for teachers and schools for online classes, attendance and fee management|
Simplilearn|Education|Online certification courses in technology and digital skills|
Coding Ninjas|Education|Online coding courses and programming practice for students|
GeeksforGeeks|Education|Computer science portal with tutorials, coding problems and interview preparation|
Scaler|Education|Online software engineering course with mentorship and placement support|
Eruditus|Education|Executive education courses from top universities|
Leverage Edu|Education|Platform to help students choose universities and apply abroad|
SwayamPrabha|Education|Government channels with educational video lectures for all subjects|
SWAYAM|Education|Government platform for free online university courses|
DIKSHA|Education|Government platform with digital textbooks and lessons for school students|
PhonePe|Payments|Mobile payment app using UPI to send money, pay bills and recharge|
Paytm|Payments|Wallet and UPI payment app for bills, recharge and shopping|
Google Pay India|Payments|UPI payment app to send money and pay merchants|
BHIM|Payments|Government UPI payment app to send and receive money|
Razorpay|Payments|Payment gateway for websites and businesses to accept online payments|
Cashfree|Payments|Payment gateway and payouts for businesses|
Pine Labs|Payments|Card payment machines and payment solutions for merchants|
MobiKwik|Payments|Digital wallet and UPI payment app|
CRED|Fintech|App to pay credit card bills and earn rewards for on time payment|
Zerodha|Fintech|Stock broker with a trading platform and investing app|
Groww|Fintech|App to invest in stocks and mutual funds|
Upstox|Fintech|Stock trading and investing app|
Policybazaar|Fintech|Website to compare and buy insurance policies online|
Paisabazaar|Fintech|Website to compare loans and credit cards|
Lendingkart|Fintech|Online business loans for small businesses|
Slice|Fintech|Credit card and payments app for young users|
Jar|Fintech|App to save money daily by investing in digital gold|
Zoho Books|Business software|Accounting software for small businesses with invoices and GST|
Tally|Business software|Accounting and GST billing software for businesses|
Zoho CRM|Business software|Customer relationship management software for sales teams|
Freshworks|Business software|Customer support and sales software including helpdesk and chat|
Zoho|Business software|Suite of business apps including email, office tools and CRM|
Khatabook|Business software|App for small shops to record credit and debit ledger entries|
OkCredit|Business software|Digital ledger app for shopkeepers to track credit|
Vyapar|Business software|Billing and inventory app for small businesses|
Chargebee|Business software|Subscription billing and recurring payments software|
Postman|Developer tools|Tool to build and test APIs|
BrowserStack|Developer tools|Cloud platform to test websites and apps on real browsers and devices|
Hasura|Developer tools|GraphQL engine to create instant APIs over databases|
Razorpay X|Fintech|Business banking and payouts automation for companies|
Naukri|Jobs|Job portal to search jobs and post resumes|
Apna|Jobs|Job app for blue collar and entry level jobs with chat with employers|
Internshala|Jobs|Platform for internships and fresher jobs for students|
WorkIndia|Jobs|Job platform for hourly and entry level jobs|
Foundit|Jobs|Job search portal and resume services|
Unstop|Jobs|Platform for students to join competitions, hackathons and apply for jobs|
Instahyre|Jobs|Job platform that matches tech professionals with companies|
Flipkart|E-commerce|Online shopping marketplace for electronics, fashion and home goods|
Myntra|E-commerce|Online fashion and lifestyle shopping|
Meesho|E-commerce|Reselling and shopping app for low cost products through social sharing|
Nykaa|E-commerce|Online beauty and cosmetics store|
Ajio|E-commerce|Online fashion shopping platform|
FirstCry|E-commerce|Online store for baby and kids products|
Lenskart|E-commerce|Online eyeglasses and sunglasses store with home eye test|
boAt|E-commerce|Consumer audio products brand selling earphones and speakers online|
Snapdeal|E-commerce|Online marketplace for value products|
Dukaan|E-commerce|App for shopkeepers to create an online store in minutes|
ONDC|E-commerce|Government backed open network for online buying and selling across apps|
Swiggy|Food delivery|Food delivery and quick grocery delivery app|
Zomato|Food delivery|Restaurant discovery and food delivery app|
Blinkit|Grocery delivery|Quick grocery delivery in minutes|
Zepto|Grocery delivery|Ten minute grocery delivery app|
BigBasket|Grocery delivery|Online grocery shopping and home delivery|
Licious|Food delivery|Online fresh meat and seafood delivery|
EatSure|Food delivery|Food ordering from multiple cloud kitchens|
Ola|Travel and transport|Cab booking and ride hailing app|
Uber India|Travel and transport|Cab and auto ride booking app|
Rapido|Travel and transport|Bike taxi and auto ride booking app|
redBus|Travel and transport|Online bus ticket booking|
MakeMyTrip|Travel and transport|Flight, hotel and holiday booking website|
IRCTC|Travel and transport|Government website and app to book train tickets|
Cleartrip|Travel and transport|Flights and hotels booking website|
Yatra|Travel and transport|Online travel booking for flights, hotels and buses|
Goibibo|Travel and transport|Hotel and flight booking platform|
OYO|Travel and transport|Hotel booking platform for budget hotels and rooms|
Ixigo|Travel and transport|Train, bus and flight booking with live train status|
Zoomcar|Travel and transport|Self drive car rental app|
BlaBlaCar India|Travel and transport|Carpooling app to share rides between cities|
Yulu|Travel and transport|Shared electric bike rental for short city trips|
FASTag|Travel and transport|Electronic toll payment system for vehicles|
Practo|Healthcare|Book doctor appointments, online consultation and lab tests|
1mg|Healthcare|Online pharmacy and lab tests with medicine delivery|
PharmEasy|Healthcare|Online medicine delivery and diagnostic tests|
Apollo 24/7|Healthcare|Online doctor consultation, pharmacy and health records app|
HealthifyMe|Healthcare|Fitness and nutrition app with calorie tracking and diet plans|
Cult.fit|Healthcare|Fitness app with workout classes and gyms|
Mfine|Healthcare|Online doctor consultation app|
Ayushman Bharat Digital Mission|Healthcare|Government digital health ID and health records platform|
eSanjeevani|Healthcare|Government telemedicine service for online doctor consultation|
Cowin|Healthcare|Government portal to register and book vaccination slots|
Wysa|Healthcare|Mental health chat support app with exercises|
YourDOST|Healthcare|Online counselling and emotional wellness platform|
Eka Care|Healthcare|Personal health records app to store reports and prescriptions|
99acres|Real estate|Property listing website to buy, sell and rent property|
MagicBricks|Real estate|Property search website for buying and renting|
Housing.com|Real estate|Property rental and sale search platform|
NoBroker|Real estate|Rent and buy property without a broker|
NestAway|Real estate|Rental home and shared housing platform|
Square Yards|Real estate|Real estate platform for property search and home loans|
Urban Company|Home services|App to book home services like cleaning, salon and repairs|
Housejoy|Home services|Home services booking for repairs and cleaning|
Pepperfry|Home services|Online furniture and home decor store|
Shaadi.com|Matrimony|Matrimonial website to find life partners|
BharatMatrimony|Matrimony|Matrimony website with profiles by community and language|
Jeevansathi|Matrimony|Matrimony website to search profiles|
Hotstar|Entertainment|Streaming app for movies, TV shows and live cricket|
JioCinema|Entertainment|Streaming app for movies, shows and live sports|
Gaana|Entertainment|Music streaming app with Indian songs|
JioSaavn|Entertainment|Music streaming app with Hindi and regional songs and podcasts|
Wynk Music|Entertainment|Music streaming app by Airtel|
ZEE5|Entertainment|Streaming app for Indian TV shows, movies and originals|
SonyLIV|Entertainment|Streaming app for TV shows, movies and sports|
MX Player|Entertainment|Video player and streaming app with free shows|
BookMyShow|Entertainment|Website and app to book movie, event and show tickets|
Dream11|Gaming|Fantasy sports app to create teams for cricket and other sports|
MPL|Gaming|Mobile gaming platform with many casual games|
Ludo King|Gaming|Mobile ludo board game|
Nazara|Gaming|Mobile games and esports company|
Cricbuzz|Sports|Live cricket scores, commentary and news app|
ESPNcricinfo|Sports|Cricket news, scores and stats website|
DigiLocker|Government|Government app to store and share digital documents like certificates|
UMANG|Government|Government app with many public services in one place|
mParivahan|Government|Government app for driving licence and vehicle registration details|
MyGov|Government|Government website to share ideas and join citizen programs|
GeM|Government|Government marketplace for departments to buy goods and services|
Startup India|Government|Government portal for startup registration, schemes and funding|
e-Shram|Government|Government portal for unorganised workers registration|
Jan Aushadhi|Government|Government scheme and app to find low cost generic medicine stores|
Income Tax e-filing|Government|Government portal to file income tax returns online|
ClearTax|Tax and legal|Website to file income tax and GST returns online|
Vakilsearch|Tax and legal|Online legal services for company registration and agreements|
LegalKart|Tax and legal|Online lawyer consultation platform|
Kisan Suvidha|Agriculture|Government app with weather, market prices and farming advice for farmers|
DeHaat|Agriculture|Platform giving farmers seeds, advice and market access|
Ninjacart|Agriculture|Supply chain platform where farmers sell fresh produce directly to retailers and buyers|
AgroStar|Agriculture|App for farmers to buy farm inputs and get crop advice|
eNAM|Agriculture|Government online market where farmers sell crops to buyers and traders|
Digital Green|Agriculture|Videos and training for farmers in local languages|
Mausam|Weather|Government app for weather forecast and alerts|
Sulekha|Local services|Local business listings and service provider search|
Justdial|Local services|Local search to find businesses, shops and services nearby|
Quikr|Local services|Classifieds website to buy and sell used items|
OLX India|Local services|Classifieds platform to buy and sell used products|
CarDekho|Automobile|Website to research, compare and buy new and used cars|
CarTrade|Automobile|Marketplace to buy and sell cars online|
Spinny|Automobile|Used car buying and selling platform with inspection|
Ather Energy|Automobile|Electric scooter maker with a connected app for navigation and ride data|
Park+|Automobile|Parking and car services app including FASTag|
Tata Neu|Super app|Super app for shopping, payments and loyalty rewards|
Jio|Telecom|Mobile network and digital apps for calls, data and entertainment|
Airtel Thanks|Telecom|App for mobile recharge, bill payment and entertainment|
Arattai|Messaging|Indian messaging app for chats, calls and groups|
Yellow.ai|Language technology|Customer service chatbots and voice bots in many languages|
Haptik|Language technology|Conversational AI chatbots for customer support|
Observe.AI|Language technology|Speech analytics to review customer call conversations|
Krutrim|AI assistant|Indian AI assistant and models that chat in Indian languages|
BharatGen|AI assistant|Government funded Indian language AI models|
""".strip().splitlines()

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "indian_software.csv")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["name", "category", "description", "year"])
    seen = set()
    for line in ROWS:
        name, category, description, year = [p.strip() for p in line.split("|")]
        if name.lower() in seen:
            continue
        seen.add(name.lower())
        w.writerow([name, category, description, year])
print("Wrote", len(seen), "rows to", OUT)
