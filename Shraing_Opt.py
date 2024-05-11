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
    # Group queries by FROM and WHERE clauses for potential combination
    query_groups = defaultdict(list)
    for query in queries:
        select_items, from_clause, where_clause, group_by_items = parseQuery(query)
        attribute, measures, functions = parseSelectItems(select_items)
        key = (from_clause, where_clause)
        query_groups[key].append((group_by_items, measures, functions, attribute))

    combined_queries = []
    for (from_clause, where_clause), group in query_groups.items():
        combined_by_group = defaultdict(list)
        for group_by_items, measures, functions, attribute in group:
            combined_by_group[group_by_items].append((measures, functions, attribute))

        for group_by_items, details in combined_by_group.items():
            select_parts = []
            for measures, functions, attribute in details:
                for measure, function in zip(measures, functions):
                    select_parts.append(f"{function}({measure}) AS {function}_{measure}")
            select_clause = ', '.join(select_parts)
            where_clause = f"WHERE {where_clause}" if where_clause else ""
            group_by_clause = f"GROUP BY {group_by_items}" if group_by_items else ""
            query = f"SELECT {group_by_items}, {select_clause} FROM {from_clause} {where_clause} {group_by_clause};"
            combined_queries.append(query)

    return combined_queries

# Example usage
queries = [
    'SELECT a, SUM(m1) FROM D WHERE a > 10 GROUP BY a',
    'SELECT a, COUNT(m2) FROM D WHERE a > 10 GROUP BY a',
    'SELECT b, AVG(m3) FROM D WHERE b < 5 GROUP BY b'
]

combined_queries = combineAggregates(queries)
for query in combined_queries:
    print(query)
