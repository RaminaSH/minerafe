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
    """
    از لیستی از قسمت‌ها، تنها قسمت‌های غیرخالی را انتخاب و با جداکننده‌ی sep به هم می‌پیوندد.
    """
    filtered = [p for p in parts if p]  # حذف موارد None یا رشته‌های خالی
    return sep.join(filtered)


def generate_candidates(film_name, year, sep):
    """
    تولید نام پوشه و لیست نام فایل‌های احتمالی بر اساس جداکننده‌ی داده‌شده (sep).

    الگوی پوشه:
      [نام فیلم با جداکننده] + sep + [سال]

    الگوی فایل (بدون پسوند):
      [پوشه] + sep + [کیفیت]+'p' + (اختیاری: نوع کیفیت) + (اختیاری: codec) + (اختیاری: tag)

    سپس دو نوع پسوند به‌صورت جداگانه اضافه می‌شود:
      - پسوند اول: ".ZarFilm.mp4"
      - پسوند دوم: ".mp4"
    """
    # تولید نام پوشه؛ به عنوان مثال "Confessions.2010" یا "Oki_s_Movie_2010"
    folder_candidate = sep.join(film_name.split()) + sep + str(year)

    qualities = ["1080", "720"]
    # برای نوع کیفیت، None یعنی حذف آن قسمت (مثلاً همانند لینکی که فقط کیفیت وجود دارد)
    quality_types = [None, "BluRay", "BrRip", "WEB-DL", "WEBRip"]
    codecs = [None, "x264"]
    releases = [None, "YIFY", "Pahe","PaHe", "Ganool","GalaxyRG" ]

    candidates = []
    # تولید ترکیبات مختلف برای قسمت‌های اختیاری
    for quality in qualities:
        for qtype in quality_types:
            for codec in codecs:
                for tag in releases:
                    # ساخت لیست قسمت‌های اصلی (بدون پسوند)
                    parts = [folder_candidate, f"{quality}p"]
                    if qtype:
                        parts.append(qtype)
                    if codec:
                        parts.append(codec)
                    if tag:
                        parts.append(tag)

                    base_candidate = build_filename(parts, sep)
                    # تولید دو نسخه فایل: یکی با ZarFilm و دیگری بدون آن
                    candidate_with = base_candidate + ".ZarFilm.mp4"
                    candidate_without = base_candidate + ".mp4"
                    candidates.append(candidate_with)
                    candidates.append(candidate_without)
    return folder_candidate, candidates


def main():
    film_name = input("نام فیلم را وارد کنید: ").strip()
    year = input("سال ساخت را وارد کنید: ").strip()

    base_url = "https://dl2-2.upenlod.pw/stream_movies"
    seps = ['.', '_']
    urls_to_check = []  # لیست تمام URLهایی که باید بررسی شوند

    # تولید لیست URLها
    for stream in range(1, 10):
        for sep in seps:
            folder_candidate, file_candidates = generate_candidates(film_name, year, sep)
            # مسیر پوشه به شکل:
            # https://dl2-2.upenlod.pw/stream_movies/stream{n}/{year}/{folder_candidate}/
            folder_url = f"{base_url}/stream{stream}/{year}/{folder_candidate}"
            for filename in file_candidates:
                full_url = folder_url + "/" + filename  # افزودن "/" بین پوشه و نام فایل
                urls_to_check.append(full_url)

    # استفاده از ThreadPoolExecutor برای بررسی همزمان URL ها
    found_url = None
    max_workers = 50  # می‌توانید تعداد تردها را برحسب نیاز تنظیم کنید
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(url_exists, url): url for url in urls_to_check}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                if future.result():
                    found_url = url
                    print("\nفایل پیدا شد!")
                    print("آدرس فایل:", found_url)
                    # در صورت پیدا شدن، به پایان برنامه می‌رسیم
                    executor.shutdown(wait=False)
                    return
            except Exception as exc:
                print(f"خطا در بررسی {url}: {exc}")

    if not found_url:
        print("\nمتاسفانه فایل مورد نظر پیدا نشد.")


if __name__ == "__main__":
    main()
