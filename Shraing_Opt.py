import re
from collections import defaultdict

function_lst = ['SUM', 'COUNT', 'AVG', 'MAX', 'MIN']

select_pattern = r"SELECT\s+(.*?)\s+FROM"
from_pattern = r"FROM\s+(.*?)(?:\s+WHERE|\s+GROUP\s+BY|$)"
where_pattern = r"WHERE\s+(.*?)(?:\s+GROUP\s+BY|$)"
group_by_pattern = r"GROUP\s+BY\s+(.*)"


def parseQuery(query):
    select_match = re.search(select_pattern, query, re.IGNORECASE)
    from_match = re.search(from_pattern, query, re.IGNORECASE)
    where_match = re.search(where_pattern, query, re.IGNORECASE)
    group_by_match = re.search(group_by_pattern, query, re.IGNORECASE)

    select_items = select_match.group(1) if select_match else ""
    from_items = from_match.group(1) if from_match else ""
    where_items = where_match.group(1) if where_match else ""
    group_by_items = group_by_match.group(1) if group_by_match else ""

    return select_items, from_items, where_items, group_by_items


def parseSelectItems(select_items):
    components = select_items.split(',')
    attribute = None
    measures, functions = [], []

    for component in components:
        component = component.strip()
        for func in function_lst:
            if func in component:
                measure_match = re.search(rf"{func}\((.*?)\)", component)
                if measure_match:
                    measure = measure_match.group(1)
                    measures.append(measure)
                    functions.append(func)
                break
        else:
            attribute = component

    return attribute, measures, functions


def combineAggregates(queries):
    grouped_aggregates_dict = defaultdict(lambda: {'measures': [], 'functions': []})

    for query in queries:
        select_items = parseQuery(query)[0]
        attribute, measures, functions = parseSelectItems(select_items)
        grouped_aggregates_dict[attribute]['measures'].extend(measures)
        grouped_aggregates_dict[attribute]['functions'].extend(functions)

    return grouped_aggregates_dict



# Q2 = 'SELECT a, SUM(m1) FROM D GROUP BY a'
# Q3 = 'SELECT a, COUNT(m2) FROM D GROUP BY a'
# print(combineAggregates([Q2, Q3]))