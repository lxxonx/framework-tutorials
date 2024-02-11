from functools import reduce
import hashlib
import json
import re
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel


day_15_router = APIRouter(prefix="/15")


class CheckInput(BaseModel):
    input: str


@day_15_router.post("/nice")
async def check_nice_input(body: CheckInput = Body(...)):
    nauty_strings = ["ab", "cd", "pq", "xy"]
    vowels = ["a", "e", "i", "o", "u", "y"]
    result = "naughty"

    for substring in nauty_strings:
        if substring in body.input:
            return JSONResponse(status_code=400, content={"result": result})
    vowel_count = 0
    for char in body.input:
        if char in vowels:
            vowel_count += 1
    if vowel_count < 3:
        return JSONResponse(status_code=400, content={"result": result})

    for i in range(len(body.input) - 1):
        if body.input[i] == body.input[i + 1] and body.input[i].isalpha():
            result = "nice"
            return JSONResponse(status_code=200, content={"result": result})

    return JSONResponse(status_code=400, content={"result": result})


RESPONSE_MAP = {
    "rule_1": {"status_code": 400, "reason": "8 chars", "result": "naughty"},
    "rule_2": {
        "status_code": 400,
        "reason": "more types of chars",
        "result": "naughty",
    },
    "rule_3": {"status_code": 400, "reason": "55555", "result": "naughty"},
    "rule_4": {"status_code": 400, "reason": "math is hard", "result": "naughty"},
    "rule_5": {
        "status_code": 406,
        "reason": "not joyful enough",
        "result": "naughty",
    },
    "rule_6": {
        "status_code": 451,
        "reason": "illegal: no sandwich",
        "result": "naughty",
    },
    "rule_7": {"status_code": 416, "reason": "outranged", "result": "naughty"},
    "rule_8": {"status_code": 426, "reason": "😳", "result": "naughty"},
    "rule_9": {
        "status_code": 418,
        "reason": "not a coffee brewer",
        "result": "naughty",
    },
    "success": {
        "status_code": 200,
        "reason": "that's a nice password",
        "result": "nice",
    },
}


def rule_no3(string):
    integers = [int(match) for match in re.findall(r"\d", string)]
    return len(integers) >= 5


def rule_no4(string):
    integers = [int(match) for match in re.findall(r"\d+", string)]
    sum_of_integers = sum(integers)
    return sum_of_integers == 2023


def rule_no5(string):
    joy = ["j", "o", "y"]
    compare_string = ""
    for char in string:
        if char in joy:
            compare_string += char

    return compare_string == "joy"


def rule_no6(string):
    for i in range(len(string) - 2):
        if (
            string[i] == string[i + 2]
            and string[i] != string[i + 1]
            and string[i].isalpha()
        ):
            return True

    return False


def rule_no7(string):
    # [U+2980, U+2BFF]
    unicode_range = [0x2980, 0x2BFF]
    for char in string:
        uc = char.encode("unicode_escape")
        if len(uc) < 4:
            continue
        code = int(uc[2:], 16)
        if unicode_range[0] <= code <= unicode_range[1]:
            return True

    return False


def rule_no8(string):
    emoji = re.findall(r"[\U0001F300-\U0001F5FF]", string)
    return len(emoji) > 0


def rule_no9(string):
    sha256_hash = hashlib.sha256(string.encode()).hexdigest()

    return sha256_hash[-1] == "a"


@day_15_router.post("/game")
async def check_password(body: CheckInput = Body(...)):
    print(body.input)

    if len(body.input) < 8:
        rule = RESPONSE_MAP["rule_1"]
        return JSONResponse(
            status_code=rule["status_code"],
            content={
                "reason": rule["reason"],
                "result": rule["result"],
            },
        )

    if not bool(re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)", body.input)):
        rule = RESPONSE_MAP["rule_2"]
        return JSONResponse(
            status_code=rule["status_code"],
            content={
                "reason": rule["reason"],
                "result": rule["result"],
            },
        )

    if not rule_no3(body.input):
        rule = RESPONSE_MAP["rule_3"]
        return JSONResponse(
            status_code=rule["status_code"],
            content={
                "reason": rule["reason"],
                "result": rule["result"],
            },
        )

    if not rule_no4(body.input):
        rule = RESPONSE_MAP["rule_4"]
        return JSONResponse(
            status_code=rule["status_code"],
            content={
                "reason": rule["reason"],
                "result": rule["result"],
            },
        )

    if not rule_no5(body.input):
        rule = RESPONSE_MAP["rule_5"]
        return JSONResponse(
            status_code=rule["status_code"],
            content={
                "reason": rule["reason"],
                "result": rule["result"],
            },
        )

    if not rule_no6(body.input):
        rule = RESPONSE_MAP["rule_6"]
        return JSONResponse(
            status_code=rule["status_code"],
            content={
                "reason": rule["reason"],
                "result": rule["result"],
            },
        )

    if not rule_no7(body.input):
        rule = RESPONSE_MAP["rule_7"]
        return JSONResponse(
            status_code=rule["status_code"],
            content={
                "reason": rule["reason"],
                "result": rule["result"],
            },
        )

    if not rule_no8(body.input):
        rule = RESPONSE_MAP["rule_8"]
        return JSONResponse(
            status_code=rule["status_code"],
            content={
                "reason": rule["reason"],
                "result": rule["result"],
            },
        )

    if not rule_no9(body.input):
        rule = RESPONSE_MAP["rule_9"]
        return JSONResponse(
            status_code=rule["status_code"],
            content={
                "reason": rule["reason"],
                "result": rule["result"],
            },
        )

    rule = RESPONSE_MAP["success"]
    return JSONResponse(
        status_code=rule["status_code"],
        content={
            "reason": rule["reason"],
            "result": rule["result"],
        },
    )
