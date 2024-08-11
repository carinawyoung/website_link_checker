# Root domain website link checker

### Purpose:

Checks hyperlinks for broken links, error responses, or anything that doesn't return a status code of 200 on a user-selected root-domain website.

### Limitations:

(1) The code is designed to be given root (aka base) domains like https://herrinc.com/ and not domains with a path, like https://herrinc.com/about.

If given a non-root domain, the code may incorrectly format hyperlinks to check. For example, when given the non-root domain https://www.skagitcohousing.org/our-blog, the header on that page has the hyperlink _/our-location.html_, and the code pairs it with the non-root domain to get the full hyperlink https://www.skagitcohousing.org/our-blog/our-location.html, when the correct pairing is https://www.skagitcohousing.org/our-location.html.

(2) The code can take a while to run, especially if there are a lot of links on a page.

There is a message printed when the code starts on a new page, and when it finishes a page, but there can be a long wait between those when a user might wonder if the code is still running correctly.

(3) One of the functions, _get_footer_navbar_tags(url)_, makes a list of the hyperlinks in the header and footer. Header and footers are often identical on each webpage in the domain, so they don't need to be checked on each page, just once at the beginning.

The code identifies the header and footer sections of a webpage by using the html classes, like this:

```
footer_selector = "footer a, .footer a, .footer_area a"
navbar_selector = ".navbar a, .nav a"
```

but this can be problematic, since web developers can name header and footer classes anything they like, so headers and footers with different class names than those already included won't be identified by the code, and will be checked on every page.

### Ideas for future changes:

(1) Adjust the code to deal with non-root domains.

(2) Add a progress indicator to show the code is running on each page -- useful for when there is a long stretch of hyperlinks to check and the user doesn't see anything for a while.

(3) Simpler but somewhat similar to this ^ , I could add a line that prints after each website checked that gives the number of hyperlinks checked on tha page.

(4) Really build the thing out and make a web page with an input box for the user to enter the website they want to check.

### History:

I had an upcoming job interview and needed to present a project as part of the interview. I decided to build something new, and purused the company website for a project idea.

As a clicked through the website, I noticed a couple of broken links and decided it would be fun to build a link checker. It felt a little cheeky to then be displaying the link checker and the broken company website links in the interview, but I enjoyed the project quite a bit and added to my knowledge base. :)
