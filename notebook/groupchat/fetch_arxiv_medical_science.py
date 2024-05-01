# filename: fetch_arxiv_medical_science.py

import arxiv
import datetime

# Define the search query parameters
search_query = 'cat:q-bio* AND (ti:medical OR abs:medical)'
sort_by = 'submittedDate'
sort_order = 'descending'
max_results = 5

# Fetch the papers
def fetch_papers(search_query, sort_by, sort_order, max_results):
    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        sort_by=sort_by,
        sort_order=sort_order
    )
    for result in search.results():
        yield {
            'title': result.title,
            'authors': [author.name for author in result.authors],
            'abstract': result.summary,
            'published': result.published,
            'updated': result.updated,
            'arxiv_id': result.get_short_id(),
            'categories': [category['term'] for category in result.categories],
            'pdf_url': result.pdf_url
        }

# Print the fetched papers
if __name__ == '__main__':
    papers = fetch_papers(search_query, sort_by, sort_order, max_results)
    for paper in papers:
        print(f"Title: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Abstract: {paper['abstract']}")
        print(f"Published: {paper['published']}")
        print(f"Updated: {paper['updated']}")
        print(f"arXiv ID: {paper['arxiv_id']}")
        print(f"Categories: {', '.join(paper['categories'])}")
        print(f"PDF URL: {paper['pdf_url']}")
        print("\n" + "-"*80 + "\n")