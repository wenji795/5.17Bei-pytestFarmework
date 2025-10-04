import logging
import allure
import jsonpath
from utils.send_request import send_jdbc_request

@allure.step("3.HTTP响应断言")
def http_assert(case, res):
    if case["check"]:
        r = jsonpath.jsonpath(res.json(), case["check"])[0]
        logging.info(f"3.HTTP响应断言: 实际结果【{r}】 == 预期结果【{case["expected"]}】")
        # assert 实际结果 == 预期结果
        assert r == case["expected"]
        # case["check"] → 从字典里取出 JSONPath 表达式（例如 "$..msg"）case["expected"] → 从字典里取出预期结果（例如 "登录成功"）[0] → 因为 jsonpath() 返回列表，要取第一个元素
    else:
        # assert 预期结果 in 实际结果
        logging.info(f"3.HTTP响应断言: 预期结果【{case["expected"]}】 in 【实际结果{res.text}】")
        assert case["expected"] in res.text


# @allure.step("3.JDBC 数据库响应断言")
def jdbc_assert(case):
    if case["sql_check"] and case["sql_expected"]:
        with allure.step("3.JDBC 数据库响应断言"):
            logging.info(f"3.JDBC响应断言: 实际结果【{send_jdbc_request(case["sql_check"])}】 == 预期结果【{case["sql_expected"]}】")
            assert send_jdbc_request(case["sql_check"]) == case["sql_expected"]
