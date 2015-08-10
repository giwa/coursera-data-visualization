import os
import json

from github import Github

git_repos = dict(
scala = [
        'apache/spark',
        'takezoe/gitbucket',
        'ConsensusResearch/Scorex-Lagonaki',
        'ornicar/lila',
        'bigdatagenomics/adam'],
python = [
        'hexahedria/biaxial-rnn-music-composition',
        'p-e-w/krill',
        'rushter/data-science-blogs',
        'duerrp/pyexperiment',
        'jkbrzt/httpie'],
go = [
    'chrislusf/seaweedfs',
    'emirozer/exposq',
    'akhenakh/statgo',
    'docker/docker',
    'avelino/awesome-go'
    ]
)



"""
github api
GET /repos/:owner/:repo/languages
"""

data_file = "git_stat.json"

data = None
if not os.path.isfile(data_file):
    g = Github(os.environ['GITHUBID'], os.environ['GITHUBPASSWD'])
    d = {}
    for lang, repos in git_repos.items():
        d[lang] = []
        for repo in repos:
            user, repo_name = repo.split('/')
            repo_stat = g.get_user(user).get_repo(repo_name)
            languages = repo_stat.get_languages()
            languages_t = [e for e in languages.items()]
            languages_t.sort(key=lambda x: x[1], reverse=True)
            repo_d = {}
            repo_d['name'] = repo
            repo_d['repository_name'] = repo_name
            repo_d['user_name'] = user
            repo_d['languages'] = languages_t
            repo_d['main_language'] = lang
            d[lang].append(repo_d)
    data = d
    with open(data_file, 'w') as f:
        f.write(json.dumps(d, indent=4))
else:
    with open(data_file) as f:
        data = json.load(f)

lang_dict_f = 'lang_dict.json'
langs = []
for repos in data.values():
    for repo in repos:
        langs.extend([x[0] for x in repo['languages']])

lang_dict= dict((v, i) for i, v in enumerate(set(langs)))
with open(lang_dict_f, 'w') as f:
    f.write(json.dumps(lang_dict, indent=4))

print(lang_dict)


