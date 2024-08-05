import requests

def check_url_availability(url):
    try:
        response = requests.get(url)
        # Check for a successful status code (2xx)
        return response.status_code < 400
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
        return False

def check_series(urls_file, name):
    first_series = name[0].upper()
    with open(urls_file, 'r') as file:
        domains = file.readlines()

    for domain in domains:
        domain = domain.strip()
        if domain:  # Check if the line is not empty
            url = f"https://{domain}/{name}"
            is_available = check_url_availability(url)
            if is_available:
                print(f"Subdomain URL: {url} is available")

    for domain in domains:
        domain = domain.strip()
        if domain:  # Check if the line is not empty
            url = f"https://{domain}/{first_series}/{name}"
            is_available = check_url_availability(url)
            if is_available:
                print(f"Subdomain URL: {url} is available")

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

def check_film(urls_file, name, sub, sal):
    with open(urls_file, 'r') as file:
        domains = file.readlines()
    if sub:
        for domain in domains:
            domain = domain.strip()
            if domain:  # Check if the line is not empty
                url = f"https://{domain}/SoftSub/{sal}"
                found = search_movie_in_page(url, name)
                if found:
                    print(f"Movie name found in {url}")
        for domain in domains:
            domain = domain.strip()
            if domain:  # Check if the line is not empty
                url = f"https://{domain}/HardSub/{sal}"
                found = search_movie_in_page(url, name)
                if found:
                    print(f"Movie name found in {url}")
        for domain in domains:
            domain = domain.strip()
            if domain:  # Check if the line is not empty
                url = f"https://{domain}/Collection"
                found = search_movie_in_page(url, name)
                if found:
                    print(f"Movie name found in {url}")

    else:
        for domain in domains:
            domain = domain.strip()
            if domain:  # Check if the line is not empty
                url = f"https://{domain}/DUBLE/{sal}"
                found = search_movie_in_page(url, name)
                if found:
                    print(f"Movie name found in {url}")


# Specify the path to your domain text file

# Specify the subdomain to check
name = input("input name: ").replace(" ", ".").strip()

video_type = input("Enter Video type: Series[0] OR Film[1]: ")
if video_type == "0":
    urls_file = 'series.txt'
    check_series(urls_file, name)
elif video_type == "1":
    urls_file = 'films.txt'
    year = input("Enter The Year: ")
    duble_sub = input("Sub[0] or Dub[1]: ")
    if duble_sub == "0":
        issub = True
    elif duble_sub == "1":
        issub = False
    check_film(urls_file, name, issub, year)



