import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = {}
    links = corpus[page]

    # Return distribution with evenly distributed probability if page has no links
    if len(links) == 0:
        for p in corpus:
            model[p] = 1.0 / len(corpus)
        return model
    
    for p in corpus:
        model[p] = (1.0 - damping_factor) / len(corpus)
    
    for p in links:
        model[p] += damping_factor / len(links)

    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample = random.choice(list(corpus.keys()))
    pagerank = None
    counts = {p: 0 for p in corpus}

    for i in range(1, n):
        # Keep track of number of times each page was visited
        counts[sample] += 1
        pagerank = transition_model(corpus, sample, damping_factor)
        
        sample = random.choices(list(pagerank.keys()), weights=list(pagerank.values()), k=1)[0]

    # Normalize values by dividing each page-visits by total number of loops
    pagerank = {p: counts[p] / n for p in corpus}
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    for p in corpus:
        pagerank[p] = 1 / len(corpus)

    diff = True
    # Loop until changes in pagerank is minimal
    while diff:
        new = {}
        diff = False

        for p in corpus:
            sum = 0
            for link in corpus:
                if len(corpus[link]) == 0:
                    sum += pagerank[link] / len(corpus)
                    
                # Check if the page being checked is in the list of links 
                elif p in corpus[link]:
                    sum += pagerank[link] / len(corpus[link])

            sum *= damping_factor
            
            new[p] = ((1-damping_factor) / len(corpus)) + sum

        # Check for each value if difference between current and new is >0.001
        for p in pagerank:
            new_diff = abs(new[p] - pagerank[p])
            if new_diff > 0.001:
                diff = True

        pagerank = new
        
    return pagerank


if __name__ == "__main__":
    main()
