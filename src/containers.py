from dependency_injector import providers, containers
from repositories.geo_repo import GeoRepo
from repositories.proxy_repo import ProxyRepo
from repositories.sql_repo import SqlRepo
from repositories.api_repo import ApiRepo
from jobs.pldown.pldown_scraper import PldownScraper
from jobs.pldown.pldown_runner import PldownRunner
from jobs.pldown.pldown_checker import PldownChecker
from jobs.proxyscrape.proxyscrape_scraper import ProxyScrapeScraper
from jobs.proxyscrape.proxyscape_runner import ProxyScrapeRunner
from jobs.proxyscrape.proxyscrape_checker import ProxyScrapeChecker
from jobs.cleanup.cleanup_checker import CleanupChecker
from jobs.cleanup.cleanup_runner import CleanupRunner
from scheduler import Scheduler
from scheduler_second import SchedulerSecond


class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')


class Repos(containers.DeclarativeContainer):
    geo_repo = providers.Singleton(GeoRepo, config=Configs.config)
    proxy_repo = providers.Singleton(ProxyRepo, config=Configs.config)
    sql_repo = providers.Singleton(SqlRepo, config=Configs.config)
    api_repo = providers.Singleton(ApiRepo, config=Configs.config)


class Scrapers(containers.DeclarativeContainer):
    pldown_scraper = providers.Singleton(PldownScraper, config=Configs.config)
    proxyscrape_scraper = providers.Singleton(ProxyScrapeScraper, config=Configs.config)


class Checkers(containers.DeclarativeContainer):
    pldown_checker = providers.Singleton(PldownChecker, config=Configs.config, geo_repo=Repos.geo_repo, proxy_repo=Repos.proxy_repo, sql_repo=Repos.sql_repo, api_repo=Repos.api_repo, pldown_scraper=Scrapers.pldown_scraper)
    proxyscrape_checker = providers.Singleton(ProxyScrapeChecker, config=Configs.config, geo_repo=Repos.geo_repo, proxy_repo=Repos.proxy_repo, sql_repo=Repos.sql_repo, api_repo=Repos.api_repo, proxyscrape_scraper=Scrapers.proxyscrape_scraper)
    cleanup_checker = providers.Singleton(CleanupChecker, config=Configs.config, sql_repo=Repos.sql_repo, proxy_repo=Repos.proxy_repo, api_repo=Repos.api_repo)


class Runners(containers.DeclarativeContainer):
    pldown_runner = providers.Singleton(PldownRunner, pldown_checker=Checkers.pldown_checker)
    proxyscrape_runner = providers.Singleton(ProxyScrapeRunner, proxyscrape_checker=Checkers.proxyscrape_checker)
    cleanup_runner = providers.Singleton(CleanupRunner, cleanup_checker=Checkers.cleanup_checker)


class Scheduler(containers.DeclarativeContainer):
    scheduler = providers.Singleton(Scheduler, pldown_runner=Runners.pldown_runner, proxyscrape_runner=Runners.proxyscrape_runner, cleanup_runner=Runners.cleanup_runner)
    scheduler_second = providers.Singleton(SchedulerSecond, pldown_runner=Runners.pldown_runner, proxyscrape_runner=Runners.proxyscrape_runner, cleanup_runner=Runners.cleanup_runner)
