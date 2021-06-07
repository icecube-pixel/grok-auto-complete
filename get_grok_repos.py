import logging
from github import Github
from typing import Dict, Tuple, List
import os
import argparse

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_top_repositories(args: Dict)->Tuple[List[str],int]:
    """
    Gets the top repositories based on 
        language python
        Desc Order based on stars of repo
    """
    logger.info("Inside to get top repositories function")
    
    github_repo_data = []
    try:
        g_obj = Github(args['token'])
        _query_str = '"grok" in:file extension:j2 NOT language:Jinja NOT language:Shell NOT language:YAML NOT language:INI NOT language:Perl NOT language:Haskell'
        results = g_obj.search_code(_query_str)
        for repo in results:
            logger.info(repo);exit()
            github_repo_data.append(str(repo.clone_url).replace('.git', ''))

        logger.info("Appended %s links to list" % len(github_repo_data))
        # epoch_nano_sec = str(round(time.time() * 100000))
        # path_to_dump = os.path.join("data", epoch_nano_sec)
    
        # with open(path_to_dump, 'wb') as handle: # Dumping the data to pickle 
        #     pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return github_repo_data, 200         
    except Exception as e:
        logger.error("Exception occurred while calling search repo {error}".format(error=e))
        return github_repo_data, 400
    

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