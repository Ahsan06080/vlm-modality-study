"""Python 3 port of the official WikiTableQuestions evaluator (evaluator.py, ppasupat/WikiTableQuestions v1.0.2,
CC BY-SA 4.0, Pasupat & Liang 2015). Logic unchanged; only py2 -> py3 syntax (unicode/basestring/long, ur'' strings)."""
import re
import unicodedata
from math import isinf, isnan


def normalize(x):
    if isinstance(x, bytes):
        x = x.decode("utf8", errors="ignore")
    x = "".join(c for c in unicodedata.normalize("NFKD", x) if unicodedata.category(c) != "Mn")
    x = re.sub(r"[‘’´`]", "'", x)
    x = re.sub(r"[“”]", '"', x)
    x = re.sub(r"[‐‑‒–—−]", "-", x)
    while True:
        old_x = x
        x = re.sub(r"((?<!^)\[[^\]]*\]|\[\d+\]|[•♦†‡*#+])*$", "", x.strip())
        x = re.sub(r"(?<!^)( \([^)]*\))*$", "", x.strip())
        x = re.sub(r'^"([^"]*)"$', r"\1", x.strip())
        if x == old_x:
            break
    if x and x[-1] == ".":
        x = x[:-1]
    x = re.sub(r"\s+", " ", x, flags=re.U).lower().strip()
    return x


class Value:
    _normalized = None

    @property
    def normalized(self):
        return self._normalized


class StringValue(Value):
    def __init__(self, content):
        assert isinstance(content, str)
        self._normalized = normalize(content)
        self._hash = hash(self._normalized)

    def __eq__(self, other):
        return isinstance(other, StringValue) and self.normalized == other.normalized

    def __hash__(self):
        return self._hash

    def __repr__(self):
        return "S" + str([self.normalized])

    def match(self, other):
        return self.normalized == other.normalized


class NumberValue(Value):
    def __init__(self, amount, original_string=None):
        assert isinstance(amount, (int, float))
        if abs(amount - round(amount)) < 1e-6:
            self._amount = int(amount)
        else:
            self._amount = float(amount)
        self._normalized = str(self._amount) if not original_string else normalize(original_string)
        self._hash = hash(self._amount)

    @property
    def amount(self):
        return self._amount

    def __eq__(self, other):
        return isinstance(other, NumberValue) and self.amount == other.amount

    def __hash__(self):
        return self._hash

    def __repr__(self):
        return ("N(%f)" % self.amount) + str([self.normalized])

    def match(self, other):
        if self.normalized == other.normalized:
            return True
        if isinstance(other, NumberValue):
            return abs(self.amount - other.amount) < 1e-6
        return False

    @staticmethod
    def parse(text):
        try:
            return int(text)
        except Exception:
            try:
                amount = float(text)
                assert not isnan(amount) and not isinf(amount)
                return amount
            except Exception:
                return None


class DateValue(Value):
    def __init__(self, year, month, day, original_string=None):
        assert not (year == month == day == -1)
        self._year, self._month, self._day = year, month, day
        if not original_string:
            self._normalized = "{}-{}-{}".format(year if year != -1 else "xx", month if month != -1 else "xx",
                                                  day if day != "-1" else "xx")
        else:
            self._normalized = normalize(original_string)
        self._hash = hash((self._year, self._month, self._day))

    @property
    def ymd(self):
        return (self._year, self._month, self._day)

    def __eq__(self, other):
        return isinstance(other, DateValue) and self.ymd == other.ymd

    def __hash__(self):
        return self._hash

    def __repr__(self):
        return ("D(%d,%d,%d)" % self.ymd) + str([self._normalized])

    def match(self, other):
        if self.normalized == other.normalized:
            return True
        if isinstance(other, DateValue):
            return self.ymd == other.ymd
        return False

    @staticmethod
    def parse(text):
        try:
            ymd = text.lower().split("-")
            assert len(ymd) == 3
            year = -1 if ymd[0] in ("xx", "xxxx") else int(ymd[0])
            month = -1 if ymd[1] == "xx" else int(ymd[1])
            day = -1 if ymd[2] == "xx" else int(ymd[2])
            assert not (year == month == day == -1)
            assert month == -1 or 1 <= month <= 12
            assert day == -1 or 1 <= day <= 31
            return (year, month, day)
        except Exception:
            return None


def to_value(original_string, corenlp_value=None):
    if isinstance(original_string, Value):
        return original_string
    if not corenlp_value:
        corenlp_value = original_string
    amount = NumberValue.parse(corenlp_value)
    if amount is not None:
        return NumberValue(amount, original_string)
    ymd = DateValue.parse(corenlp_value)
    if ymd is not None:
        if ymd[1] == ymd[2] == -1:
            return NumberValue(ymd[0], original_string)
        return DateValue(ymd[0], ymd[1], ymd[2], original_string)
    return StringValue(original_string)


def to_value_list(original_strings, corenlp_values=None):
    if corenlp_values is not None:
        assert len(original_strings) == len(corenlp_values)
        return list(set(to_value(x, y) for x, y in zip(original_strings, corenlp_values)))
    return list(set(to_value(x) for x in original_strings))


def check_denotation(target_values, predicted_values):
    if len(target_values) != len(predicted_values):
        return False
    for target in target_values:
        if not any(target.match(pred) for pred in predicted_values):
            return False
    return True
