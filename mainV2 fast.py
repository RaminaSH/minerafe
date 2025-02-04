import requests
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_url_availability(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        # در نظر گرفتن کدهای موفقیت‌آمیز (< 400)
        return response.status_code < 400
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
        return False


def search_movie_in_page(url, movie_name, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code < 400:
            if movie_name.lower() in response.text.lower():
                return True
        return False
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
        return False


def check_series(urls_file, name, sal):
    # تعریف چند الگو برای ساخت URL
    first_series = name[0].upper()
    first_serieslow = name[0].lower()
    with open(urls_file, 'r') as file:
        domains = [line.strip() for line in file if line.strip()]

    # تولید لیست URLها برای همه الگوها
    url_list = []
    for domain in domains:
        url_list.append(f"https://{domain}/{name}")
        url_list.append(f"https://{domain}/{sal}/{name}")
        url_list.append(f"https://{domain}/{first_series}/{name}")
        url_list.append(f"https://{domain}/{first_serieslow}/{name}")

    # بررسی همزمان URLها
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {executor.submit(check_url_availability, url): url for url in url_list}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                if future.result():
                    print(f"Subdomain URL: {url} is available")
            except Exception as exc:
                print(f"Error checking {url}: {exc}")


def check_film(urls_file, name, sub, sal):
    with open(urls_file, 'r') as file:
        domains = [line.strip() for line in file if line.strip()]
    first_film = name[0].upper()
    datenow = datetime.datetime.now()
    tasks = []  # لیست کارهایی که شامل (url, function) هستند

    if sub:
        # الگوی اول: فقط برای دامنه‌ی مشخص
        for domain in domains:
            if domain == "cdn.bolbolk.fun/Film":
                url = f"https://{domain}/SOFT.SUB/{first_film}"
                tasks.append((url, lambda url, nm=name: search_movie_in_page(url, nm)))

        # الگوی دوم: دامنه vip10 با تاریخ‌های ماه و روز
        for domain in domains:
            if domain == "vip10.meserverpro.lol/dl32/Film":
                for i in range(1, datenow.month + 1):
                    for j in range(1, 32):
                        url = f"https://{domain}/SoftSub/2025/{i:02d}/{j:02d}"
                        tasks.append((url, lambda url, nm=name: search_movie_in_page(url, nm)))

        # الگوی سوم: دامنه به همراه SoftSub/{سال}
        for domain in domains:
            url = f"https://{domain}/SoftSub/{sal}"
            tasks.append((url, lambda url, nm=name: search_movie_in_page(url, nm)))

        # الگوی چهارم: دامنه به همراه {سال}
        for domain in domains:
            url = f"https://{domain}/{sal}"
            tasks.append((url, lambda url, nm=name: search_movie_in_page(url, nm)))

        # الگوی پنجم: دامنه به همراه HardSub/{سال}
        for domain in domains:
            url = f"https://{domain}/HardSub/{sal}"
            tasks.append((url, lambda url, nm=name: search_movie_in_page(url, nm)))

        # الگوی ششم: دامنه به همراه Collection
        for domain in domains:
            url = f"https://{domain}/Collection"
            tasks.append((url, lambda url, nm=name: search_movie_in_page(url, nm)))
    else:
        # حالت Duble: فقط الگوی DUBLE/{سال}
        for domain in domains:
            url = f"https://{domain}/DUBLE/{sal}"
            tasks.append((url, lambda url, nm=name: search_movie_in_page(url, nm)))

    # اجرای همزمان کارها
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {executor.submit(func, url): url for url, func in tasks}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                if future.result():
                    print(f"Movie name found in {url}")
            except Exception as exc:
                print(f"Error checking {url}: {exc}")


if __name__ == "__main__":
    name = input("input name: ").replace(" ", ".").strip()
    video_type = input("Enter Video type: Series[0] OR Film[1]: ").strip()
    if video_type == "0":
        urls_file = 'series.txt'
        sal = input("Input the year: ").strip()
        check_series(urls_file, name, sal)
    elif video_type == "1":
        urls_file = 'films.txt'
        year = input("Enter The Year: ").strip()
        duble_sub = input("Sub[0] or Dub[1]: ").strip()
        issub = True if duble_sub == "0" else False
        check_film(urls_file, name, issub, year)
