Test Runner
===========
After creating AIML unit tests with the test_creator.py utility, use test_runner to execute the tests and flag up
any errors or invalid responses

Usage:
    python3 test_runner.py --test_dir test-dir --qna_file qna-file --verbose
or
    python3 test_runner.py --test_file test_file --qna_file qna-file --verbose

    --test_dir  - Directory to search for aiml files to execute, includes sub directories in search
    --test_file - Name of a single aiml unit test file to execute, useful during test creation process
    --qna_file  - This file is created during test execution and provides a record of all questions and their answers
    --verbose   - Prints out more detailed debugging information as the test runner executes each test. Useful of you
                  have a large number of tests and want to monitor progress

Filel Format:
