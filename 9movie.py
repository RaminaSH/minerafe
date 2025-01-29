import requests

def check_movie_in_urls(urls_file, movie_name, movie_year=None):
    # with open(urls_file, 'r') as file:
    #     domains = file.readlines()
    def check_url_availability(url):
        try:
            response = requests.get(url, timeout=10)
            return response.status_code < 400  # کدهای موفقیت‌آمیز (200-299)
        except requests.RequestException as e:
            print(f"Error checking {url}: {e}")
            return False

    # def generate_movie_urls(domain, movie_name, movie_year):
    #     """
    #     لینک‌های ممکن برای جستجوی فیلم را ایجاد می‌کند.
    #     """
    #     urls = []
    #     years = ["1400", "1401", "1402", "1403"]
    #     months = [f"{i:02d}" for i in range(1, 21)]  # از 01 تا 20
    #
    #     # فرمت اول: بدون سال ساخت
    #     if movie_year:
    #         for url1 in domains:
    #                 urls.append(f"{domain}/{movie_name.replace(' ', '.')}.{movie_year}")
    #
    #
    #
    #     for url1 in domains:
    #             urls.append(f"{domain}/{movie_name.replace(' ', '.')}")
    #
    #     # فرمت دوم: با سال ساخت (اگر سال داده شده باشد)
    #     return urls

    with open(urls_file, 'r') as file:
        domains = file.readlines()

    for domain in domains:
        domain = domain.strip()
        if domain:  # Check if the line is not empty
            url = f"{domain}/{movie_name.replace(' ', '.')}.{movie_year}"
            is_available = check_url_availability(url)
            if is_available:
                print(f"Subdomain URL: {url} is available")





    for domain in domains:
        domain = domain.strip()
        if domain:  # Check if the line is not empty
            url = f"{domain}/{movie_name.replace(' ', '.')}"
            is_available = check_url_availability(url)
            if is_available:
                print(f"Subdomain URL: {url} is available")



if __name__ == "__main__":
    urls_file = '9movieLinks.txt'  # فایل حاوی لینک‌ها
    movie_name = input("نام فیلم را وارد کنید: ").strip()
    movie_year = input("سال ساخت فیلم را وارد کنید (اختیاری): ").strip() or None
    check_movie_in_urls(urls_file, movie_name, movie_year)