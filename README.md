# money-lib

![PyPI - Version](https://img.shields.io/pypi/v/money-lib.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/money-lib.svg)
![PyPI - License](https://img.shields.io/pypi/l/money-lib.svg)

Python 3 money lib with decimal precision and currency exchange support.

## Installation

Install the latest release with:
```
pip install money-lib
```

## Usage

A Currency object can be created with a *currency_code* (must be a string and valid ISO 4217 format: `^[A-Z]{3}$`).

```python
>>> from money import Currency
>>> currency = Currency('USD')
>>> currency
Currency('USD')
```

A Money object can be created with an *amount* (can be any valid value in `decimal.Decimal(value)`) and a *currency* (can be a string or a `Currency(code)` object).

```python
>>> from money import Money
>>> money = Money('7.37', 'USD')
>>> money
Money(Decimal('7.37'), 'USD')
```

Money objects are immutable by convention and hashable. Once created, you can use read-only properties *amount* (decimal.Decimal) and *currency* (Currency) to access its internal components.
The *amount* property returns the amount rounded to the correct number of decimal places for the currency.

```python
>>> money = Money('6.831', 'USD')
>>> money.amount
Decimal('6.83')
>>> money.currency
Currency('USD')
```

Money can apply most arithmetic and comparison operators between money objects, integers (int) and decimal numbers (decimal.Decimal).

```python
>>> money = Money('5', 'USD')
>>> money / 2
Money(Decimal('2.5'), 'USD')
>>> money + Money('10', 'USD')
Money(Decimal('15'), 'USD')
```

All comparison and arithmetic operators support automatic currency conversion as long as you have a [currency exchange backend](#currency-exchange) setup.
The currency of the leftmost object has priority.

```python
# Assuming the rate from USD to EUR is 2
>>> money = Money('7.50', 'USD')
>>> money + Money('5', 'EUR')
Money(Decimal('10.00'), 'USD')
```

Money supports formatting for different locales.
```python
>>> money = Money('13.65', 'USD')
>>> money.format()
'$13.65'
>>> money.format('pt_PT')
'13,65 US$'
```

## Currency exchange

Currency exchange works by setting a backend class that implements the abstract base class `money.exchange.BaseBackend`.
Its API is exposed through `money.xrates`, along with `xrates.backend` and `xrates.backend_name`.

A simple proof-of-concept backend `money.exchange.SimpleBackend` is included.

```python
from decimal import Decimal
from money import Money, xrates

xrates.backend = 'money.exchange.SimpleBackend'
xrates.base = 'USD'
xrates.setrate('AAA', Decimal('2'))
xrates.setrate('BBB', Decimal('8'))

a = Money(1, 'AAA')
b = Money(1, 'BBB')

assert a.to('BBB') == Money('4', 'BBB')
assert b.to('AAA') == Money('0.25', 'AAA')
assert a + b == Money('1.25', 'AAA')
```

## Credits

Currency exchange support based on https://github.com/carlospalol/money.

Currency data and formatting is powered by [Babel](http://babel.pocoo.org).