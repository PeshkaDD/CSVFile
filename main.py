import argparse
import csv
from tabulate import tabulate
from typing import List, Dict, Union, Optional, Callable


def read_csv(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def filter_data(
    data: List[Dict[str, str]],
    condition: str
) -> List[Dict[str, str]]:
    if not condition:
        return data

    column, operator, value = parse_condition(condition)
    filtered_data = []

    for row in data:
        if evaluate_condition(row[column], operator, value):
            filtered_data.append(row)

    return filtered_data


def parse_condition(condition: str) -> tuple[str, str, str]:
    operators = ['>=', '<=', '>', '<', '=']
    for op in operators:
        if op in condition:
            column, value = condition.split(op, 1)
            return column.strip(), op, value.strip()
    raise ValueError(f"Invalid condition: {condition}")


def evaluate_condition(
    cell_value: str,
    operator: str,
    condition_value: str
) -> bool:
    try:
        # Try numeric comparison
        cell_num = float(cell_value)
        cond_num = float(condition_value)
        if operator == '>':
            return cell_num > cond_num
        elif operator == '<':
            return cell_num < cond_num
        elif operator == '>=':
            return cell_num >= cond_num
        elif operator == '<=':
            return cell_num <= cond_num
        elif operator == '=':
            return cell_num == cond_num
    except ValueError:
        # Fall back to string comparison
        if operator == '=':
            return cell_value == condition_value
    return False


def aggregate_data(
    data: List[Dict[str, str]],
    aggregate: str
) -> Optional[Dict[str, Union[float, str]]]:
    if not aggregate or not data:
        return None

    column, operation = aggregate.split('=', 1)
    column = column.strip()
    operation = operation.strip().lower()

    try:
        values = [float(row[column]) for row in data]
    except ValueError:
        return None

    if operation == 'avg':
        result = sum(values) / len(values)
    elif operation == 'min':
        result = min(values)
    elif operation == 'max':
        result = max(values)
    else:
        return None

    return {'column': column, operation: result}


def main():
    parser = argparse.ArgumentParser(description='Process CSV file.')
    parser.add_argument('file', help='Path to the CSV file')
    parser.add_argument(
        '--where',
        help='Filter condition (e.g., "price>500")',
        default=None
    )
    parser.add_argument(
        '--aggregate',
        help='Aggregate condition (e.g., "price=avg")',
        default=None
    )
    args = parser.parse_args()

    data = read_csv(args.file)

    if args.where:
        data = filter_data(data, args.where)

    if args.aggregate:
        result = aggregate_data(data, args.aggregate)
        if result:
            print(tabulate([result], headers='keys', tablefmt='grid'))
        else:
            print("Invalid aggregation or non-numeric column")
    else:
        print(tabulate(data, headers='keys', tablefmt='psql'))


if __name__ == '__main__':
    main()