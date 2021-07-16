import sys

from lib import utilities

MAP = {
    'C': ['C', 'C/C++ Header'],
    'C++': ['C++', 'C/C++ Header'],
    'Objective C': ['Objective C', 'C/C++ Header']
}


def run(project_id, repo_path, cursor, **options):
    threshold = options.get('threshold', 0)

    query = 'SELECT language FROM projects WHERE id = %d' % project_id
    cursor.execute(query)

    record = cursor.fetchone()
    language = record[0]
    languages = MAP[language] if language in MAP else [language]

    sloc = utilities.get_loc(repo_path)
    rresult = 0
    for language in languages:
        if language in sloc:
            rresult += sloc[language]['sloc']

    bresult = True if rresult >= threshold else False

    print('{0} - Project size: {1}'.format(project_id, rresult))
    return bresult, rresult

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
