import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
<<<<<<< HEAD
from requests.exceptions import Timeout, ConnectionError, ReadTimeout
=======
from requests.exceptions import Timeout, ConnectionError
>>>>>>> 349884f (add user input to link checker, and .gitignore file)
from tabulate import tabulate
from urllib.parse import urlparse, urljoin


<<<<<<< HEAD
=======
##################################################
>>>>>>> 349884f (add user input to link checker, and .gitignore file)
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


<<<<<<< HEAD
=======
##################################################
>>>>>>> 349884f (add user input to link checker, and .gitignore file)
def get_footer_navbar_tags(url):
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Specify the CSS selector for the footer <a> tags
<<<<<<< HEAD
        footer_selector = "footer a"
        navbar_selector = ".navbar a"
=======
        footer_selector = "footer a, .footer a"
        navbar_selector = ".navbar a, .nav a"
>>>>>>> 349884f (add user input to link checker, and .gitignore file)

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


<<<<<<< HEAD
### START OF MAIN CODE ###

domain = "https://www.rc.virginia.edu"
=======
################ START OF MAIN CODE ######################

# domain = "https://www.rc.virginia.edu"
domain = input("What domain would you like to check?: ")

# strip the trailing / in the domain name
if domain[-1] == "/":
    domain = domain[:-1]
>>>>>>> 349884f (add user input to link checker, and .gitignore file)

footer_and_navbar_links = get_footer_navbar_tags(domain)

interior_page_list = interior_pages_list(domain)

<<<<<<< HEAD
for page in interior_page_list:
    # Check for connectivity
    try:
=======
for page in interior_page_list:  ####
    try:  # Check for connectivity
>>>>>>> 349884f (add user input to link checker, and .gitignore file)
        response = requests.get(page, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except (Timeout, ConnectionError, requests.exceptions.HTTPError) as error:
        print(f"Error: {error}")
        print("Could not connect to the website.")
    else:
        if response.status_code == 200:
<<<<<<< HEAD
            print(f"\n\nThe website {page} is up and running")

        # Find all the links on the website page
=======
            print(f"\n\nChecking Website: {page} ")

        ## Find all the anchor tags on the page
>>>>>>> 349884f (add user input to link checker, and .gitignore file)
        soup = BeautifulSoup(response.content, "html.parser")

        anchors = set(soup.find_all("a"))

        link_list = []  # list for info I want to print at the end

<<<<<<< HEAD
        for anchor in anchors:
            try:
                href_link = anchor.get("href")
=======
        ## Extract hyperlinks and check for functionality
        for anchor in anchors:
            try:
                href_link = anchor.get("href")
                # Exclude some links
>>>>>>> 349884f (add user input to link checker, and .gitignore file)
                if (
                    href_link is None  # exclude tags that have no link
                    or href_link == ""  # exclude empty links
                    or href_link[:6] == "mailto"  # exclude email links
                    or href_link[0] == "#"  # exclude within page links
                ):
                    continue
<<<<<<< HEAD
                if href_link[0] == "/":
                    href_link = "https://www.rc.virginia.edu" + href_link
=======
                # Format remaining links
                if href_link[0] == "/":
                    href_link = domain + href_link
>>>>>>> 349884f (add user input to link checker, and .gitignore file)

                if href_link[-1] == "/":
                    href_link = href_link[0:-1]

<<<<<<< HEAD
=======
                # Check link functionality
                #### Check all links on main page
>>>>>>> 349884f (add user input to link checker, and .gitignore file)
                if interior_page_list.index(page) == 0:
                    link_page = requests.get(href_link, timeout=10)
                    link_list.append([link_page.status_code, anchor.text, href_link])
                else:
<<<<<<< HEAD
                    if href_link not in footer_and_navbar_links:
=======
                    if (
                        href_link not in footer_and_navbar_links
                    ):  #### Check subset of links on remaining pages
>>>>>>> 349884f (add user input to link checker, and .gitignore file)
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

<<<<<<< HEAD
        # lists to hold info
=======
        #### Formatting
        # lists for seperating items by status
>>>>>>> 349884f (add user input to link checker, and .gitignore file)
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
