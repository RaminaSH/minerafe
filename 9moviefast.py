import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_url_availability(url, timeout=10):
    """
    بررسی می‌کند که آیا URL داده شده (با استفاده از GET) معتبر و در دسترس است.
    """
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code < 400  # موفقیت‌آمیز: کدهای 200-399
    except requests.RequestException as e:
        print(f"Error checking {url}")
        return False


def get_first_available(urls, max_workers=50):
    """
    به کمک ThreadPoolExecutor همه‌ی URLهای داده شده را به صورت موازی بررسی می‌کند
    و اولین URL معتبر را برمی‌گرداند.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(check_url_availability, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                if future.result():
                    return url  # اولین URL معتبر پیدا شد
            except Exception as exc:
                print(f"Error checking {url}: {exc}")
    return None


def check_movie_in_urls(urls_file, movie_name, movie_year=None):
    # خواندن لیست دامین‌ها از فایل
    with open(urls_file, 'r') as file:
        domains = [line.strip() for line in file if line.strip()]

    # تولید سه الگوی URL مختلف:
    # الگو 1: {domain}/{first_letter_lower}/{movie_name_with_dot}.{movie_year}
    # (این الگو در صورتی که سال ساخت وارد شده باشد بررسی می‌شود)
    urls1 = []
    first_serieslow = movie_name[0].lower()
    if movie_year:
        for domain in domains:
            url = f"{domain}/{first_serieslow}/{movie_name.replace(' ', '.')}.{movie_year}"
            urls1.append(url)

    # الگو 2: {domain}/{movie_name_with_dot}.{movie_year}
    urls2 = []
    if movie_year:
        for domain in domains:
            url = f"{domain}/{movie_name.replace(' ', '.')}.{movie_year}"
            urls2.append(url)

    # الگو 3: {domain}/{movie_name_with_dot}
    urls3 = []
    for domain in domains:
        url = f"{domain}/{movie_name.replace(' ', '.')}"
        urls3.append(url)

    result = None

    # بررسی همزمان الگو 1 (در صورت وجود سال)
    if urls1:
        result = get_first_available(urls1)
        if result:
            print(f"Pattern 1 available: {result}")

    # در صورتی که در الگو 1 نتیجه‌ای پیدا نشد، الگو 2 را بررسی می‌کنیم
    if not result and urls2:
        result = get_first_available(urls2)
        if result:
            print(f"Pattern 2 available: {result}")

    # در صورتی که همچنان نتیجه‌ای پیدا نشد، الگو 3 را بررسی می‌کنیم
    if not result and urls3:
        result = get_first_available(urls3)
        if result:
            print(f"Pattern 3 available: {result}")

    if not result:
        print("No available URL found.")


if __name__ == "__main__":
    urls_file = '9movieLinks.txt'  # فایل حاوی لیست دامین‌ها
    movie_name = input("Input Name: ").strip()
    movie_year = input("Year: ").strip() or None
    check_movie_in_urls(urls_file, movie_name, movie_year)
