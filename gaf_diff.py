from ontobio.io.gafparser import GafParser
from ontobio.io.assocparser import AssocParserConfig
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--before')
parser.add_argument('-a', '--after')

def is_assoc_in_list(assoc, assoc_list, exact_match=True):
    result = False
    if exact_match:
        if assoc in assoc_list:
            result = True
    else:
        for a in assoc_list:
            # GP, term, qualifier, ev code
            if assoc["subject"]["id"] == a["subject"]["id"] \
            and assoc["object"]["id"] == a["object"]["id"] \
            and sorted(q.upper() for q in assoc['qualifiers']) == sorted(q.upper() for q in a['qualifiers']) \
            and assoc['evidence']['type'] == a['evidence']['type']:
                result = True
    return result

if __name__ == "__main__":
    args = parser.parse_args()

    config = AssocParserConfig(paint=True)
    parser = GafParser()
    parser.config = config

    # new_file = "/Users/ebertdu/panther/paint_issues/obsoletion/gene_association.paint_pombase.20180823.gaf"
    # old_file = "/Users/ebertdu/panther/paint_issues/obsoletion/gene_association.paint_pombase.20180801.gaf"
    new_file = args.after
    old_file = args.before
    new_assocs = parser.parse(new_file, skipheader=True)
    old_assocs = parser.parse(old_file, skipheader=True)

    added = []
    removed = []

    for a in new_assocs:
        if not is_assoc_in_list(a, old_assocs, exact_match=False):
            added.append(a)

    for a in old_assocs:
        if not is_assoc_in_list(a, new_assocs, exact_match=False):
            removed.append(a)

    print(len(new_assocs))
    print(len(old_assocs))
    print("{} annotation added".format(len(added)))
    print("{} annotation removed".format(len(removed)))