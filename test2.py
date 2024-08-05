import requests
import concurrent.futures

def check_url_availability(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code < 400
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
        return False

def search_movie_in_page(url, movie_name):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code < 400:
            if movie_name.lower() in response.text.lower():
                return True
        return False
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
        return False

def check_series(urls_file, name):
    first_series = name[0].upper()
    with open(urls_file, 'r') as file:
        domains = file.readlines()

    urls_to_check = []
    for domain in domains:
        domain = domain.strip()
        if domain:  # Check if the line is not empty
            urls_to_check.append(f"https://{domain}/{name}")
            urls_to_check.append(f"https://{domain}/{first_series}/{name}")

    def check_url(url):
        is_available = check_url_availability(url)
        if is_available:
            print(f"Subdomain URL: {url} is available")

    # Use ThreadPoolExecutor to run check_url function concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_url, urls_to_check)

def check_film(urls_file, name, sub, sal):
    with open(urls_file, 'r') as file:
        domains = file.readlines()

    urls_to_check = []
    if sub:
        for domain in domains:
            domain = domain.strip()
            if domain:  # Check if the line is not empty
                urls_to_check.append(f"https://{domain}/SoftSub/{sal}")
                urls_to_check.append(f"https://{domain}/HardSub/{sal}")
                urls_to_check.append(f"https://{domain}/Collection")
    else:
        for domain in domains:
            domain = domain.strip()
            if domain:  # Check if the line is not empty
                urls_to_check.append(f"https://{domain}/DUBLE/{sal}")

    def check_url(url):
        found = search_movie_in_page(url, name)
        if found:
            print(f"Movie name found in {url}")

    # Use ThreadPoolExecutor to run check_url function concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_url, urls_to_check)

# Main script execution
if __name__ == "__main__":
    # User inputs
    name = input("Input name: ").replace(" ", ".").strip()
    video_type = input("Enter Video type: Series[0] OR Film[1]: ").strip()

    if video_type == "0":
        urls_file = 'series.txt'
        check_series(urls_file, name)
    elif video_type == "1":
        urls_file = 'films.txt'
        year = input("Enter The Year: ").strip()
        duble_sub = input("Sub[0] or Dub[1]: ").strip()
        issub = duble_sub == "0"
        check_film(urls_file, name, issub, year)
    else:
        print("Invalid video type. Please enter 0 for Series or 1 for Film.")
