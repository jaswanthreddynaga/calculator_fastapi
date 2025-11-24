import pytest
from pydantic import ValidationError
from app.calculation_factory import CalculationFactory, Add, Subtract, Multiply, Divide
from app.schemas import CalculationCreate

def test_add_operation():
    op = Add()
    assert op.execute(5, 3) == 8

def test_subtract_operation():
    op = Subtract()
    assert op.execute(5, 3) == 2

def test_multiply_operation():
    op = Multiply()
    assert op.execute(5, 3) == 15

def test_divide_operation():
    op = Divide()
    assert op.execute(6, 3) == 2

def test_divide_by_zero_operation():
    op = Divide()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        op.execute(5, 0)

def test_factory_create_operation():
    assert isinstance(CalculationFactory.create_operation("Add"), Add)
    assert isinstance(CalculationFactory.create_operation("Subtract"), Subtract)
    assert isinstance(CalculationFactory.create_operation("Multiply"), Multiply)
    assert isinstance(CalculationFactory.create_operation("Divide"), Divide)

def test_factory_invalid_operation():
    with pytest.raises(ValueError, match="Unknown operation type"):
        CalculationFactory.create_operation("Modulus")

def test_calculation_create_schema_valid():
    calc = CalculationCreate(a=10, b=5, type="Add")
    assert calc.a == 10
    assert calc.b == 5
    assert calc.type == "Add"

def test_calculation_create_schema_invalid_type():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=5, type="Invalid")

def test_calculation_create_schema_divide_by_zero():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=0, type="Divide")
