import logging
from github import Github
from typing import Dict, Tuple, List
import os
import argparse
import traceback

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO)

logger = logging.getLogger(__name__)

# https://docs.github.com/en/github/searching-for-information-on-github/searching-on-github/searching-for-repositories#search-by-when-a-repository-was-created-or-last-updated

def get_query_string_to_exclude()->str:
    """
    Generates query string instead of hard-coding and appends to the query string
    :return:
    """
    logger.info("Inside function to generate query to hit API")
    languages_to_exclude = ['Jinja', 'Shell', 'YAML', 'INI', 'Perl', 'Haskell']
    exclude_languages = " ".join(["NOT language:{}".format(language)  for language in languages_to_exclude])
    return " " + exclude_languages + " "


def get_top_repositories(args: Dict)->None:
    """
    Gets the top matches of code based on pattern where grok is used and is of not YAML etc
    """
    logger.info("Inside to get top repositories function")

    try:
        g_obj = Github(args['token'])
        _query_str = '"grok" in:file extension:j2 NOT language:Jinja NOT language:Shell NOT language:YAML NOT language:INI NOT language:Perl NOT language:Haskell'
        results = g_obj.search_code(_query_str)
        for repo in results:
            file_name = str(repo).split("ContentFile(path=")[1].replace('"',"")[:-1].replace("/", "_")
            path_to_dump = os.path.join(os.getcwd(), "data", file_name)
            logger.info("Dumping file {}".format(file_name))
            with open(path_to_dump, "wb") as f:
                f.write(repo.decoded_content)
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())


def get_inputs()->Dict:
    """Gets the username and password from the console """
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", dest="token", help="Enter the oAuth token", required=True)
    args = vars(parser.parse_args())
    return args


def main():
    logger.info("Inside Main")
    args = get_inputs()
    get_top_repositories(args=args)


if __name__ == '__main__':
    main()