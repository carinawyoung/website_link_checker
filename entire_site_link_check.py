import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests.exceptions import Timeout, ConnectionError, ReadTimeout
from tabulate import tabulate
from urllib.parse import urlparse, urljoin


def interior_pages_list(domain):
    # Define the target URL
    target_url = domain

    # Send an HTTP GET request to the target URL
    response = requests.get(target_url, timeout=10)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all anchor tags (links) from the HTML
        anchor_tags = soup.find_all("a")

        # Initialize a set to store unique URLs
        internal_urls = set()

        # Get the base URL (to resolve relative URLs)
        base_url = urlparse(target_url).scheme + "://" + urlparse(target_url).netloc

        # Iterate through the anchor tags and extract href attributes
        for tag in anchor_tags:
            href = tag.get("href")
            if href:
                # Join the URL with the base URL to handle relative links
                full_url = urljoin(base_url, href)
                # Get rid of copies of a website that only differ by a / at the end
                if full_url[-1] == "/":
                    full_url = full_url[0:-1]
                # Check if the URL is part of the same domain
                if urlparse(full_url).netloc == urlparse(target_url).netloc:
                    internal_urls.add(full_url)

        return sorted(internal_urls)

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


def get_footer_navbar_tags(url):
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Specify the CSS selector for the footer <a> tags
        footer_selector = "footer a"
        navbar_selector = ".navbar a"

        # Find all <a> tags in footer and navbar and format as "http://....""
        footer_a_tags = soup.select(footer_selector)
        navbar_a_tags = soup.select(navbar_selector)

        footer_and_navbar_hrefs = set()

        for anchor in footer_a_tags:
            href_link = anchor.get("href")
            if href_link != "#" and href_link is not None:
                if href_link[0] == "/":
                    href_link = domain + href_link

                footer_and_navbar_hrefs.add(href_link)

        for anchor in navbar_a_tags:
            href_link = anchor.get("href")
            if href_link != "#" and href_link is not None:
                if href_link[0] == "/":
                    href_link = domain + href_link

                footer_and_navbar_hrefs.add(href_link)

        return sorted(footer_and_navbar_hrefs)


### START OF MAIN CODE ###

domain = "https://www.rc.virginia.edu"

footer_and_navbar_links = get_footer_navbar_tags(domain)

interior_page_list = interior_pages_list(domain)

for page in interior_page_list:
    # Check for connectivity
    try:
        response = requests.get(page, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except (Timeout, ConnectionError, requests.exceptions.HTTPError) as error:
        print(f"Error: {error}")
        print("Could not connect to the website.")
    else:
        if response.status_code == 200:
            print(f"\n\nThe website {page} is up and running")

        # Find all the links on the website page
        soup = BeautifulSoup(response.content, "html.parser")

        anchors = set(soup.find_all("a"))

        link_list = []  # list for info I want to print at the end

        for anchor in anchors:
            try:
                href_link = anchor.get("href")
                if (
                    href_link is None  # exclude tags that have no link
                    or href_link == ""  # exclude empty links
                    or href_link[:6] == "mailto"  # exclude email links
                    or href_link[0] == "#"  # exclude within page links
                ):
                    continue
                if href_link[0] == "/":
                    href_link = "https://www.rc.virginia.edu" + href_link

                if href_link[-1] == "/":
                    href_link = href_link[0:-1]

                if interior_page_list.index(page) == 0:
                    link_page = requests.get(href_link, timeout=10)
                    link_list.append([link_page.status_code, anchor.text, href_link])
                else:
                    if href_link not in footer_and_navbar_links:
                        link_page = requests.get(href_link, timeout=10)
                        link_list.append(
                            [link_page.status_code, anchor.text, href_link]
                        )

            except (
                requests.exceptions.InvalidSchema,
                ConnectionError,
                TimeoutError,
                requests.exceptions.HTTPError,
                requests.exceptions.ReadTimeout,
            ) as error:
                link_list.append(["Error", anchor.text, href_link, error])

        # lists to hold info
        code_200 = [["Linking Text on Website", "Link"]]
        code_404 = [["Linking Text on Website", "Link"]]
        exception_errors = []
        other_issues = [["Error", "Linking Text on Website", "Link"]]

        # shunt link info into corresponding list
        for link_log in link_list:
            if link_log[0] == 200:
                code_200.append([link_log[1], link_log[2]])
            elif link_log[0] == 404:
                code_404.append([link_log[1], link_log[2]])
            elif link_log[0] == "Error":
                exception_errors.append([link_log[1], link_log[2], link_log[3]])
            else:
                other_issues.append([link_log[0], link_log[1], link_log[2]])

        # print results out in nicely formatted view
        if len(code_404) > 1:
            print("\n*************** 404 Issues ********************* ")
            print(tabulate(code_404, headers="firstrow", tablefmt="fancy_grid"))

        # print("**************** 200 *****************************")
        # print(tabulate(code_200, headers="firstrow", tablefmt="fancy_grid"))

        if len(exception_errors) == 0:
            continue
        else:
            print("**************** Error Issues *****************************")
            for log in exception_errors:
                print("Linking Text on Website: ", log[0])
                print("Link: ", log[1])
                print("Error: ", log[2])
                print()
        if len(other_issues) > 1:
            print("**************** Other Status Codes *****************************")
            print(tabulate(other_issues, headers="firstrow", tablefmt="fancy_grid"))
