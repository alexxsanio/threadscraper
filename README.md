# threadscraper

threadscraper is a Python module where you can scrape user profiles from [threads.com](https://www.threads.com) based on their username. 

The file structure goes:

```text
threadscraper/       
│       
├── config/       
│   ├── settings.yaml       
├── data/       
├── media/       
├── output/       
│   ├── threads_results.csv       
│   ├── threads_results.json       
├── src/       
│   ├── main.py       
│   └── scraper/       
│       ├── utils/       
│       │        
│       ├── __init__.py       
│       ├── exporter.py       
│       ├── threads_scraper.py       
│       └── parser.py       
```

# How to use
       
To use this module and scrape threads, start by

- go to `/config/settings.yaml`, specify the list of threads usernames you want to scrape
- open your terminal, navigate to `threadscraper/src` 
- apply the command `python main.py` and wait for the module to scrape threads for each user

Sample results are stored in `threadscraper/output` as `threads_results.csv`.