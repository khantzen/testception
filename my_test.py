class TestCase:
    def __init__(self, name):
        self.name = name

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def run(self, result):
        self.setUp()
        result.testStarted()
        try:
            exec("self." + self.name + "()")
        except :
            result.testFailed()

        self.tearDown()
        return result

class WasRun(TestCase):
    def __init__(self, name):
        self.name = name

    def setUp(self):
        self.log = "setUp"

    def testMethod(self):
        self.log = self.log + " testMethod"

    def tearDown(self):
        self.log = self.log + " tearDown"

    def testBrokenMethod(self):
        assert 1 == 2

class TestResult:
    def __init__(self):
        self.runCount = 0
        self.failCount = 0

    def testStarted(self):
        self.runCount += 1

    def testFailed(self):
        self.failCount += 1

    def summary(self):
        return f"{self.runCount} run, {self.failCount} failed"

class TestSuite:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            result = test.run(result)
        return result

class TestCaseTest(TestCase):
    def setUp(self):
        self.test = WasRun("testMethod")
        self.result = TestResult()

    def testTemplateMethod(self):
        self.test.run(self.result)
        assert "setUp testMethod tearDown" == self.test.log

    def testResult(self):
        test = WasRun("testMethod")
        self.result = test.run(self.result)
        assert "1 run, 0 failed" == self.result.summary()

    def testFailedResult(self):
        test = WasRun("testBrokenMethod")
        self.result = test.run(self.result)
        assert "1 run, 1 failed" == self.result.summary()

    def testResultTemplate(self):
        self.result = TestResult()

        self.result.testStarted()
        self.result.testFailed()

        assert "1 run, 1 failed" == self.result.summary()

    def testSuite(self):
        suite = TestSuite()

        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))

        self.result = suite.run(self.result)

        assert "2 run, 1 failed" == self.result.summary()

suite = TestSuite()

for test in ["testTemplateMethod", "testResult", "testFailedResult",
             "testResultTemplate", "testSuite"]:
    suite.add(TestCaseTest(test))

result = TestResult()

result = suite.run(result)

print(result.summary())
