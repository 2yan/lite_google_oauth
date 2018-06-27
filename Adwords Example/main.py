import datagetter
import re

def fix_name(name):
    name = name.replace('ga:', '')

    def convert(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    return convert(name)

# Campaign X
# AD Group X
# Search Keyword X
# Search Keyword Match Type X


''' Possible '''
# Impressions X
# Clicks X
# Cost X

''' Remaining '''
# Avg.CPC
# First page CPC
# Max CPC
# Quality Score
# Conversions
# Search Keyword Status


start_date = '2018-01-01'
end_date = '2018-02-01'
view_id = '42723232'
metric = ['ga:impressions','ga:adClicks','ga:adCost', 'ga:CPC'] 
dimension = ['ga:adGroup','ga:campaign','ga:adMatchedQuery','ga:adMatchType']
segment_id = "sessions::condition::ga:medium==cpc"
segment_id = False
data = datagetter.full_get(start_date, end_date, view_id, metric, dimension, segment_id)




#final.columns = final.columns.map(fix_name)
#final.index.name = fix_name(final.index.name)

