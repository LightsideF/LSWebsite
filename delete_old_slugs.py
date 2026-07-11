import os

old_slugs = [
    'mr-and-mrs-b-personal-guarantees',
    'mr-jb-hmrc',
    'mr-bb-divorce-and-debt',
    'cau-ltd-closing-a-company',
    'cc-ltd-business-turnaround',
    'mr-g-personal-liability',
    'ms-j-too-much-debt',
    'ms-jj-too-much-debt',
    'ms-j-your-property-at-risk',
    'mr-a-bankruptcy',
    'mr-a-personal-liability',
    'mr-and-mrs-c-personal-too-much-debt',
    'mr-n-too-much-debt',
    'nim-ltd-personal-liability',
    'nim-ltd-closing-a-company',
    'ms-pa-business-personal-guarantees',
    'mr-and-mrs-tac-property-at-risk',
    'ms-r-divorce-debt',
    'mr-cr-hmrc',
    'mrs-ss-property-at-risk',
    'gg-property-portfolio',
    'mr-d-and-mr-j-personal-liability',
    'mr-and-mrs-v-bankruptcy',
    'mr-and-mrs-v-too-much-debt',
    'mr-v-other-situations',
    'ms-m-creditors-bailiffs',
    'ken-personal-liability',
    'sam-closing-a-company',
    'diana-closing-a-company',
    'jeff-death-debt',
    'david-debt-and-death',
    '200SB-debt-and-death',
]

deleted = 0
missing = 0
for slug in old_slugs:
    f = slug + '.html'
    if os.path.exists(f):
        os.remove(f)
        print('DELETED: ' + f)
        deleted += 1
    else:
        print('ALREADY GONE: ' + f)
        missing += 1

print('')
print('Done. Deleted: ' + str(deleted) + ', Already gone: ' + str(missing))
