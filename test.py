import lib.utilities
import pandas as pd
from git import Repo


def yearmon_index_from_t0(t0):
    return pd.date_range(start=t0, end='2019-06-01', freq='MS')


# 18219288
# /tmp/reaper_runs/18219288/google-perftools/
path = '/tmp/reaper_runs/18219288/google-perftools/'
repo = Repo(path)
git = repo.git

t0 = lib.utilities.earliest_commit_date(path)
print(t0)

t0_yearmon = lib.utilities.unix_ts_to_yearmon(int(t0))
t_ind = yearmon_index_from_t0(t0_yearmon)

# reverse index
for t in t_ind[::-1]:
    # lib.utilities.rollback(path, t)
    # git log -1 --before="{0} 23:59:59" --pretty="format:%H"'
    before = '{0}-{1}-01 00:00:00'.format(t.year, t.month)
    sha = git.log('-1', before=before, format='%H')
    if sha != '':
        git.reset('--hard', sha)
        sha = git.log('-1', format='%h')
        loc = lib.utilities.get_loc(path)
        print('t = {0}, h = {1}, sloc = {2}, cloc = {3}'.format(
            t, sha, loc['SUM']['sloc'], loc['SUM']['cloc']
            )
        )


git.pull()
