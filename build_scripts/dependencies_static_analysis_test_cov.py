""" build script to building the similarity tool"""
import platform
from subprocess_calls import call_subprocess
from install_dependencies import install_pip


def install_aspell():
    """
    Installs Aspell and configure for english
    """
    if str(platform.system()).upper() == "LINUX":
        call_subprocess("sudo apt-get update -qq")
        call_subprocess("sudo apt-get install --assume-yes aspell aspell-en")
        print("Stage Install aspell -- COMPLETED --")
    else:
        print("Please install and configure Aspell for english")


def install_jscpd():
    """
    Installs jscpd and configure for english
    """
    if str(platform.system()).upper() == "LINUX":
        call_subprocess("sudo npm install")
        call_subprocess("sudo npm install -g jscpd@3.2.1")
        print("Stage Install jscpd -- COMPLETED --")
    else:
        print("Please install and configure jscpd")


def check_lint():
    """
    function check the repo for any python linting errors
    """
    call_subprocess("python3 -m pylint similarity_processor/ test/ build_scripts/ ")
    print("Stage linting -- COMPLETED --")


def check_code_duplication():
    """
    checks the repo for any duplicate or code code with 20 token and 10% allowed duplicate
    """
    call_subprocess('jscpd --min-tokens 20 --reporters "json" --mode "strict" --format "python" -o . .')
    call_subprocess("python3 build_scripts/jscpd_parser.py --j 10 ")
    print("Stage duplicate detection -- COMPLETED --")


def check_cyclomatic_complexity():
    """
    checks the repo for function with cyclomatic complexity , fails if value is greater than 6
    """
    call_subprocess('python3 -m lizard similarity_processor -X> CC.xml')
    call_subprocess("python3 build_scripts/cyclo_gate.py --c 6")
    print("Stage cyclomatic complexity detection -- COMPLETED --")


def check_dead_code():
    """
    checks the repo for dead code with minimum confidence 70
    """
    call_subprocess('python3 -m vulture --min-confidence 70 '
                    'similarity_processor test build_scripts whitelist.py')
    print("Stage dead code detection -- COMPLETED --")


def check_spelling():
    """
    check the repo for spelling errors
    """
    call_subprocess('python3 -m pyspelling')
    print("Stage spell checking -- COMPLETED --")


def test_coverage():
    """
    executes the tests and gates the coverage for greater than 95
    """
    call_subprocess('python3 -m pytest test --cov-config=.coveragerc --cov=similarity_processor')
    call_subprocess('coverage report --fail-under=95')
    call_subprocess('codecov')
    print("Stage test & coverage -- COMPLETED --")


def mutation_testing():
    """
    executes the mutation tests and gates for 20 percentage
    """
    call_subprocess('python3 -m mutmut run > mutmut.log || true')
    call_subprocess('mutmut junitxml --suspicious-policy=ignore --untested-policy=ignore > mutmut.xml')
    call_subprocess('python3 build_scripts/mutmut_parse.py --m 20')
    print("Stage mutation testing -- COMPLETED --")


if __name__ == '__main__':
    install_pip()
    install_aspell()
    install_jscpd()
    check_lint()
    check_code_duplication()
    check_cyclomatic_complexity()
    check_dead_code()
    check_spelling()
    test_coverage()
    # mutation_testing()
