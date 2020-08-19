import search_engine_parser
from search_engine_parser import (
    GoogleSearch, 
    BingSearch,
    DuckDuckGoSearch)

import newsapi
from newsapi import NewsApiClient

import requests
import json
from typing import Iterable, Callable

# Search object for gathering links to further analysis
# It uses class arc
class Search:

    def __init__(self):
        self.newsapi_obj = NewsApiClient(apikey__missing)

    # This makes the actual process
    def __call__(query:str, n_links:int, search_method:str = 'google', language:str = None) -> Iterable:
        '''
        Args:
            query (:obj: 'str')
               * The search query we are passing to the specified search engine
               * It can be different from the question. Maybe the user wants so ask a totally 
                different question than the search querybut as standard it is the question
            n_links (:obj: 'int')
               * The maximum amount of links that is returned
               * These links should be crawlable, because they've gone through a filter
               * I'm maybe considering getting the data right after the search query. 
                This way we can skip the filter part and just directly get the page data
            search_method (:obj: 'str')
               * It's the type of search engine we want to use. Maybe Google, NewsAPI or another one
               * This can be effective if Google are IP banning you/us. But also if we want 
                to search news articles
               * We are validating the search_method through the search_methods function
        '''

        # Validate search_method
        search_method = self.check_search_method(search_method)

        # Load search engine function
        search_engine = self.create_search_fn(search_method)

        # 1.Search for query
        if method == 'newsapi'
            results = search_engine(query=query, lang=lang)
        else:
            results = search_engine(query=query)

        # Remove blacklisted websites
        results = self.filter_urls(results)

        # Take max n_links
        return results[:n_links]

    def filter_urls(self, urls:Iterable) -> Callable:
        '''
        urls (:obj: 'Iterable')
        '''

        # List of urls we want to get rid of
        invalid_urls = ['.xls', '.txt', 'youtube.com', 'youtu.be']

        # We're turning the urls into a string so it's easier to look it up
        str_urls = ' '.join(urls)

        # We haven't created the filter yet, so we're just returning the
        for i in non_valid:
            # Adds a filter so we don't 
            # always have to iterate over urls
            if i in str_urls:
                for j in urls:
                    if i in j:
                        urls.remove(j)

        return urls

    def create_search_fn(self, method:str) -> Callable:
        '''
        Args:
            method (:obj: 'str')
               * The name of the way we want to search
               * This could be 'google', 'newsapi'
        '''

        if method == 'google':
            def search_fn(query):
                args = (query, 1)
                results = GoogleSearch().search(*args)
                return results
            return search_fn

        elif method == 'newsapi':
            def search_fn(query, lang):
                results = news_api_fn(
                    api_obj=self.newsapi_obj,
                    query=query,
                    lang=lang)
                return results
            return search_fn

        elif method == 'bing':
            def search_fn(query):
                args = (query, 1)
                results = BingSearch().search(*args)
                return results
            return search_fn

        elif method == 'duckduckgo':
            def search_fn(query):
                args = (query, 1)
                results = DuckDuckGoSearch().search(*args)
                return results
            return search_fn

    def check_search_method(self, method:str) -> str:
        '''
        Args:
            method (:obj: 'str')
               * The name of the search method we want to use
               * That string is then checked is correct in this function
        '''

        method = method.lower()

        # A list of all available search_engines
        # The first link will always be the standard
        #! In a future version use quinturnions to live update this if an error happens with the google search engine, or the news api 
        available_engines = (
            'google',
            'bing',
            'duckduckgo',
            'newsapi')

        if method in available_engines:
            return method # We're lowering it
        return available_engines[0]

def news_api_fn(query:str, lang:str = 'en', api_obj:NewsApiClient = None) -> Iterable:
    '''
    Args:
        api_obj (:obj: 'NewsApiClient', :default: 'None')
           * A preinitialized client api object
           * We're loading it before this func, to save a little bit of time, 
            and it would be pointless to do it over and over again
        query (:obj: 'str')
           * The search query specified by the user
           * This function is the main reason for splitting question and query
            because this will achieve better results with the just the headline
        lang (:obj: 'str', :default: 'en [english]')
           * That's the langauge we want to search in
           * It will be automatically generated by the google translate api
            It returns the original language which is pretty cool
    '''

    if api_obj == None:
        api_obj = NewsApiClient(apikey__missing)

    # Send a request to the API
    response = api_obj.get_everything(
        q=query,
        language=lang,
        sort_by='relevancy')

    # Convert from json to dict
    response = json.loads(response)

    # Only get links if we successfully sent the request
    if response['status'] != 'error':
        # Save urls
        #! In a future version, probably do some logic of the description, so we get the most accurate news articles
        urls = []
        for article in response['articles']:
            url = article['url']
            urls.append(url)
        return urls
    return None