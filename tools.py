import os
import json
from apify_client import ApifyClient


def _get_client() -> ApifyClient:
    return ApifyClient(os.getenv("APIFY_API_TOKEN"))


def search_company_news(company_name: str, query_suffix: str = "latest news product launch technology 2025") -> str:
    client = _get_client()

    run_input = {
        "queries": f"{company_name} {query_suffix}",
        "maxPagesPerQuery": 1,
        "resultsPerPage": 10,
        "mobileResults": False,
    }

    run = client.actor("apify/google-search-scraper").call(run_input=run_input)

    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        for r in item.get("organicResults", [])[:8]:
            results.append({
                "title": r.get("title", ""),
                "description": r.get("description", ""),
                "url": r.get("url", ""),
            })

    return json.dumps(results)


def scrape_company_tech_blog(company_name: str, blog_url: str = None) -> str:
    client = _get_client()

    if not blog_url:
        search_run_input = {
            "queries": f"{company_name} engineering blog technical articles",
            "maxPagesPerQuery": 1,
            "resultsPerPage": 5,
        }
        search_run = client.actor("apify/google-search-scraper").call(run_input=search_run_input)

        urls = []
        for item in client.dataset(search_run["defaultDatasetId"]).iterate_items():
            for r in item.get("organicResults", [])[:3]:
                url = r.get("url", "")
                if url:
                    urls.append(url)

        if not urls:
            return json.dumps({"error": "Could not find a tech blog for this company"})

        blog_url = urls[0]

    run_input = {
        "startUrls": [{"url": blog_url}],
        "maxCrawlPages": 4,
        "crawlerType": "cheerio",
    }

    run = client.actor("apify/website-content-crawler").call(run_input=run_input)

    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        text = item.get("text", "")
        if text:
            results.append({
                "url": item.get("url", ""),
                "title": item.get("metadata", {}).get("title", ""),
                "content": text[:1500],
            })

    return json.dumps(results[:4])


def search_job_postings(company_name: str) -> str:
    client = _get_client()

    run_input = {
        "queries": f"{company_name} software engineer job requirements skills 2025",
        "maxPagesPerQuery": 1,
        "resultsPerPage": 8,
    }

    run = client.actor("apify/google-search-scraper").call(run_input=run_input)

    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        for r in item.get("organicResults", [])[:6]:
            results.append({
                "title": r.get("title", ""),
                "description": r.get("description", ""),
                "url": r.get("url", ""),
            })

    return json.dumps(results)
