# -*- coding: utf-8 -*-
from src.customlogger import get_logger
from src.googlemaps import GoogleMapsScraper
from multiprocessing import Pool
from termcolor import colored
import argparse
import csv
from datetime import datetime
from pathlib import Path
import traceback
import logging

sorting_enumeration = {
    "most_relevant": 0,
    "newest": 1,
    "highest_rating": 2,
    "lowest_rating": 3,
}
HEADER = [
    "id_review",
    "caption",
    "relative_date",
    "retrieval_date",
    "rating",
    "username",
    "n_review_user",
    "n_photo_user",
    "url_user",
]


def call_scraper(row, args, logger):
    print("initializing scraper")

    # Cria pasta se não existir
    path = datetime.now().strftime("data/%Y/%m/%d/")
    Path(path).mkdir(exist_ok=True, parents=True)

    # Configura nome do arquivo
    file_name = row["name"].strip().lower().replace(" ", "-")
    file_name = file_name + "-gm-reviews.csv"

    # Cria csv_writer
    with open(path + file_name, "a", encoding="utf-8", newline="\n") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        print("writer created")

        # Define e escreve header no csv
        header_line = HEADER
        if args.source:
            header_line += ["url_source"]
        writer.writerow(header_line)
        print("header written")

        # Inicializa objeto scraper
        with GoogleMapsScraper(args.debug) as scraper:
            url = row["url"]
            print(f"url: {url}")
            print("scrapping...")

            sort_result = scraper.sort_by(url, sorting_enumeration[args.sort_by])
            print(f"sort_result: {sort_result}")

            n_reviews = int(row["limit"])
            reviews = scraper.get_reviews(writer, n_reviews)
            # n = 0
            # print(f"\t{url} review: {n}")
            # while n < int(row["limit"]):
            #     reviews = scraper.get_reviews(writer)

            #     n += len(reviews)
            #     print(f"\t{url} review: {n}")


def callback(some):
    print("success callback")


def error_callback(error):
    print(f"error callback: {error}\n{traceback.print_exc()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Maps reviews scraper.")
    parser.add_argument("--i", type=str, default="urls.txt", help="target URLs file")
    parser.add_argument(
        "--sort_by",
        type=str,
        default="newest",
        help="most_relevant, newest, highest_rating or lowest_rating",
    )
    parser.add_argument(
        "--place", dest="place", action="store_true", help="Scrape place metadata"
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="Run scraper using browser graphical interface",
    )
    parser.add_argument(
        "--source",
        dest="source",
        action="store_true",
        help="Add source url to CSV file (for multiple urls in a single file)",
    )
    parser.add_argument(
        "--processes",
        type=int,
        dest="processes",
        help="Quantity of processes to launch",
    )
    parser.set_defaults(place=False, debug=False, source=False, processes=4)

    args = parser.parse_args()
    results = []
    logger = get_logger("")
    try:
        with open(args.i, newline="") as csvfile:
            with Pool(processes=args.processes) as pool:
                for row in csv.DictReader(csvfile, delimiter=",", quotechar='"'):
                    result = pool.apply_async(
                        call_scraper,
                        (row, args, logger),
                        callback=callback,
                        error_callback=error_callback,
                    )
                    results.append(result)
                [result.wait() for result in results]
    except Exception as e:
        logger.exception(e)
