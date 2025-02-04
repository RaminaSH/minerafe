import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def url_exists(url, timeout=5):
    """
    بررسی می‌کند که آیا URL داده شده (با استفاده از HEAD) معتبر و در دسترس است.
    """
    try:
        r = requests.head(url, allow_redirects=True, timeout=timeout)
        return r.status_code == 200
    except requests.RequestException:
        return False


def build_filename(parts, sep):
    filtered = [p for p in parts if p]
    return sep.join(filtered)


def generate_candidates(film_name, year, sep):
    folder_candidate = sep.join(film_name.split()) + sep + str(year)

    qualities = ["1080", "720"]
    quality_types = [None, "WEBRip", "BluRay", "BrRip", "WEB-DL"]
    codecs = [None, "x264"]
    releases = [None,"GalaxyRG", "YIFY", "Pahe","PaHe", "Ganool" ]

    candidates = []
    for quality in qualities:
        for qtype in quality_types:
            for codec in codecs:
                for tag in releases:
                    parts = [folder_candidate, f"{quality}p"]
                    if qtype:
                        parts.append(qtype)
                    if codec:
                        parts.append(codec)
                    if tag:
                        parts.append(tag)
                    parts.append("ZarFilm.mp4")
                    filename = build_filename(parts, sep)
                    candidates.append(filename)
    return folder_candidate, candidates


def main():
    film_name = input("نام فیلم را وارد کنید: ").strip()
    year = input("سال ساخت را وارد کنید: ").strip()

    base_url = "https://dl2-2.upenlod.pw/stream_movies"
    seps = ['.', '_']
    urls_to_check = []  # لیست تمام URLهایی که باید بررسی شوند

    # تولید لیست URL ها
    for stream in range(1, 10):
        for sep in seps:
            folder_candidate, file_candidates = generate_candidates(film_name, year, sep)
            folder_url = f"{base_url}/stream{stream}/{year}/{folder_candidate}/"
            for filename in file_candidates:
                full_url = folder_url + "/" + filename
                urls_to_check.append(full_url)

    # استفاده از ThreadPoolExecutor برای بررسی همزمان URL ها
    found_url = None
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_url = {executor.submit(url_exists, url): url for url in urls_to_check}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                if future.result():
                    found_url = url
                    print("\nفایل پیدا شد!")
                    print("آدرس فایل:", found_url)
                    # در صورت پیدا شدن، می‌توانید فوراً کار را متوقف کنید:
                    executor.shutdown(wait=False)
                    return
            except Exception as exc:
                print(f"خطا در بررسی {url}: {exc}")

    if not found_url:
        print("\nمتاسفانه فایل مورد نظر پیدا نشد.")


if __name__ == "__main__":
    main()
