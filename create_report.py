import os, time, unittest
import HtmlTestRunner
report_path = os.getcwd() #get current work dir
now = time.strftime('%y-%m-%d %H:%M',time.localtime(time.time()))
title=u'entry_task'
report_repash = os.path.join(report_path, title + now + '.html')

def get_cases():
    case_path = "./"
    discover = unittest.defaultTestLoader.discover(case_path, pattern='test_for*.py')
    return  discover
if __name__ == '__main__':
    file = open('./ ', "wb")
    runner = HtmlTestRunner.HTMLTestRunner(output='./', combine_reports=True, report_name="report", report_title="report", descriptions="details")
    runner.run(get_cases())
    file.close()

