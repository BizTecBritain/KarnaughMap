import tests.fixed_test_2
import tests.fixed_test_3
import tests.fixed_test_4
import tests.fixed_test_5
import tests.fixed_test_6
import tests.double_wrap_test
import tests.user_test


def run_all():
    print(double_wrap_test.run())
    print(fixed_test_2.run())
    print(fixed_test_3.run())
    print(fixed_test_4.run())
    print(fixed_test_5.run())
    print(fixed_test_6.run())
    print(user_test.run())


def run():
    print(double_wrap_test.run())
    print(fixed_test_2.run())
    print(fixed_test_3.run())
    print(fixed_test_4.run())
    print(fixed_test_5.run())
    print(fixed_test_6.run())
