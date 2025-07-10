import pytest
from main import read_csv, filter_data, aggregate_data

# Тестовые данные
sample_data = [
    {'name': 'Alice', 'age': '30', 'salary': '5000'},
    {'name': 'Bob', 'age': '40', 'salary': '6000'},
    {'name': 'Charlie', 'age': '35', 'salary': '7000'}
]

def test_filter_data_equal():
    result = filter_data(sample_data, "name=Alice")
    assert len(result) == 1
    assert result[0]['name'] == 'Alice'

def test_filter_data_greater():
    result = filter_data(sample_data, "age>34")
    assert len(result) == 2
    assert all(int(person['age']) > 34 for person in result)

def test_filter_data_less():
    result = filter_data(sample_data, "salary<6000")
    assert len(result) == 1
    assert result[0]['name'] == 'Alice'

def test_aggregate_avg():
    result = aggregate_data(sample_data, "salary=avg")
    assert result['function'] == 'avg'
    assert result['result'] == pytest.approx(6000.0)

def test_aggregate_min():
    result = aggregate_data(sample_data, "age=min")
    assert result['result'] == 30

def test_aggregate_max():
    result = aggregate_data(sample_data, "age=max")
    assert result['result'] == 40

def test_aggregate_invalid_column():
    result = aggregate_data(sample_data, "wrong=avg")
    assert result is None
