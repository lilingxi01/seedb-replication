import re

function_lst = ['SUM', 'COUNT', 'AVG']

select_pattern = r"SELECT\s+(.*?)\s+FROM"
from_pattern = r"FROM\s+(.*?)(?:\s+WHERE|\s+GROUP\s+BY|$)"
where_pattern = r"WHERE\s+(.*?)(?:\s+GROUP\s+BY|$)"
group_by_pattern = r"GROUP\s+BY\s+(.*)"


def parseFunction(select_items):
    components = select_items.split(',')
    attribute, measure, function = None, None, None

    for component in components:
        component = component.strip()
        for func in function_lst:
            if func in component:
                function = func
                function_pattern = rf"{func}\((.*?)\)"
                measure_match = re.search(function_pattern, component)
                if measure_match:
                    measure = measure_match.group(1)
                break
        else:
            attribute = component

    return attribute, function, measure


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


# def combineMultipleAggregates(dimension_lst, function_lst, measure_lst):

# Q2 = 'SELECT a, SUM(m) FROM D GROUP BY a'
# select_items, from_items, where_items, group_by_items = parseQuery(Q2)
# print(select_items)
# print(parseFunction(select_items))
# # print(parseQuery(Q2))