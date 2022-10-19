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

ind = {"most_relevant": 0, "newest": 1, "highest_rating": 2, "lowest_rating": 3}
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
HEADER_W_SOURCE = [
    "id_review",
    "caption",
    "relative_date",
    "retrieval_date",
    "rating",
    "username",
    "n_review_user",
    "n_photo_user",
    "url_user",
    "url_source",
]


def csv_writer(source_field, ind_sort_by, path="data/2022/09/19/"):
    outfile = ind_sort_by + "-gm-reviews.csv"
    targetfile = open(path + outfile, mode="a", encoding="utf-8", newline="\n")
    writer = csv.writer(targetfile, quoting=csv.QUOTE_MINIMAL)

    if source_field:
        h = HEADER_W_SOURCE
    else:
        h = HEADER
    writer.writerow(h)

    return writer


def do_the_job(row, args, logger):
    logger.info("doing the job")
    now = datetime.now().strftime("data/%Y/%m/%d/")
    Path(now).mkdir(exist_ok=True, parents=True)
    writer = csv_writer(
        args.source, row["name"].strip().lower().replace(" ", "-"), path=now
    )
    logger.info("writer created")
    with GoogleMapsScraper(args.debug) as scraper:
        url = row["url"]
        print(url)
        logger.info("scrapping...")
        error = scraper.sort_by(url, ind[args.sort_by])
        if True:
            n = 0
            logger.info(url)
            logger.info("\t" + url + " review " + str(n))
            while n < int(row["limit"]):

                print(n)

                reviews = scraper.get_reviews(writer)

                n += len(reviews)
                logger.info("\t" + url + " review " + str(n))


def callback(some):
    print(colored("deu bom"))


def error_callback(error):
    print(f"error: {error}")
    print(colored("deu ruim"))


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
    logger = get_logger("main")
    try:
        with open(args.i, newline="") as csvfile:
            with Pool(processes=args.processes) as pool:
                for row in csv.DictReader(csvfile, delimiter=",", quotechar="|"):
                    result = pool.apply_async(
                        do_the_job,
                        (row, args, logger),
                        callback=callback,
                        error_callback=error_callback,
                    )
                    results.append(result)
                [result.wait() for result in results]
    except Exception as e:
        logger.exception(e)
