"""Regenerates findings F001 to F006 from data/primary. Run from research/findings/."""
import csv, collections, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, '..', '..', 'data', 'primary')
R = list(csv.DictReader(open(os.path.join(P, 'halted_trials_dedup.csv'))))
T = {r['nct']: r for r in csv.DictReader(open(os.path.join(P, 'trial_records.csv')))}
for r in R:
    r['study_type'] = T.get(r['nct'], {}).get('study_type', '?')

def cell(r):
    return (r['modality'][:4], 'IND' if r['sponsor_class'] == 'INDUSTRY' else 'NONIND')

def share(rows, key='biz'):
    n = len(rows); k = sum(r[key] == 'True' for r in rows)
    return f'{k}/{n} = {100*k/n:.1f}%' if n else '0/0'

def yb(y):
    try: y = float(y)
    except ValueError: return 'NA'
    return '<=2018' if y <= 2018 else '2019-21' if y <= 2021 else '2022+'

print('F001  business-cited share, INTERVENTIONAL trials only')
I = [r for r in R if r['study_type'] == 'INTERVENTIONAL']
for c in sorted(set(cell(r) for r in I)):
    print('   ', c, share([r for r in I if cell(r) == c]))

IT = [r for r in R if cell(r) == ('Ther', 'IND')]
print('F002  industry-therapeutic cell by subfamily (n, business share)')
for s, _ in collections.Counter(r['subfamily'] for r in IT).most_common():
    print('   ', s, share([r for r in IT if r['subfamily'] == s]))

print('F003  business share by trial start year')
groups = {
    'industry CAR-T': [r for r in IT if 'CAR-T' in r['subfamily']],
    'industry non-CAR-T therapeutics': [r for r in IT if 'CAR-T' not in r['subfamily']],
    'industry diagnostics': [r for r in R if cell(r) == ('Diag', 'IND')],
    'non-industry therapeutics': [r for r in R if cell(r) == ('Ther', 'NONIND')],
}
for name, rows in groups.items():
    print('   ', name, {b: share([r for r in rows if yb(r['start_year']) == b]) for b in ['<=2018', '2019-21', '2022+']})

biz = [r for r in IT if r['biz'] == 'True']
print('F004  industry-therapeutic business halts:', len(biz))
print('    names a financial cause:', share(biz, 'names_financial_cause'))
print('    explicitly denies a safety cause:', share(biz, 'denies_safety_cause'))
print('    distinct sponsors:', len(set(r['sponsor'] for r in biz)))
print('    top sponsor:', collections.Counter(r['sponsor'] for r in biz).most_common(1))

print('F005  AI/ML subfamily inside the diagnostic cells; modalities per subfamily')
for c in [('Diag', 'IND'), ('Diag', 'NONIND')]:
    rows = [r for r in R if cell(r) == c]
    print('   ', c, 'AI/ML rows:', sum('AI/ML' in r['subfamily'] for r in rows), 'of', len(rows))
m = collections.defaultdict(set)
for r in R: m[r['subfamily']].add(r['modality'])
print('    subfamilies with more than one modality:', {k: v for k, v in m.items() if len(v) > 1} or 'none')

cn = re.compile(r'Co\.,? ?Ltd|Shanghai|Guangzhou|Nanjing|Beijing|Shenzhen|Hangzhou|Suzhou|Wuhan|Chengdu|Hefei|Tianjin|Zhejiang|Jiangsu|China|Chinese|Sichuan|Shandong|Hunan|Henan|Fujian|Xiamen|Chongqing', re.I)
print('F006  China-name-pattern sponsors, industry therapeutics:', share([r for r in IT if cn.search(r['sponsor'])]), ' others:', share([r for r in IT if not cn.search(r['sponsor'])]))
