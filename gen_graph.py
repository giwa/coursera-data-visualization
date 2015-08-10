import json

with open('./git_stat.json') as f:
    repo_stat= json.load(f)
with open('./lang_dict.json') as f:
    lang_d= json.load(f)

graph = dict(nodes=[], links=[])

lang_r=18
lang_idx = {}
for i,lang in enumerate(lang_d.keys()):
    lang_idx[lang.lower()] = i
    d = dict(name=lang, value=lang_r, group=i)
    graph['nodes'].append(d)

for lang, repos in repo_stat.items():
    for repo in repos:
        d = {}
        d['name'] = repo['name']
        d['value'] = 6
        d['group'] = lang_idx[repo['main_language']]
        graph['nodes'].append(d)
        repo_idx = len(graph['nodes']) - 1
        link_d = {}
        link_d['target'] = repo_idx
        link_d['source'] = lang_idx[repo['main_language']]
        link_d['value'] = 5
        graph['links'].append(link_d)
        for other_lang in [e[0] for e in repo['languages'] if e[0].lower() not in repo['main_language']]:
            link_d = dict(target=repo_idx, source=lang_idx[other_lang.lower()], value=2)
            graph['links'].append(link_d)
print(graph)

with open('./webapp/app/graph.json', 'w') as f:
    f.write(json.dumps(graph, indent=4))
