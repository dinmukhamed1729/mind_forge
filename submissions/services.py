import os
import subprocess
import tempfile
import time
from abc import ABC, abstractmethod


class ICodeExecutor(ABC):
    @abstractmethod
    def run(self, code: str, input_data: str) -> tuple[str, str, float]:
        pass


class PythonCodeExecutor(ICodeExecutor):
    def run(self, code: str, input_data: str) -> tuple[str, str, float]:
        start_time = time.time()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(code.encode())
            temp_file_path = temp_file.name

        cmd = ["python", temp_file_path]
        try:
            process = subprocess.run(cmd, input=input_data, text=True, capture_output=True, timeout=2)
            execution_time = (time.time() - start_time) * 1000
            os.remove(temp_file_path)
            return process.stdout, process.stderr, execution_time
        except subprocess.TimeoutExpired:
            return "", "Time Limit Exceeded", 2000
        except Exception as e:
            return "", str(e), 0


class CodeExecutorFactory:
    EXECUTORS = {
        'python': PythonCodeExecutor(),
    }

    @staticmethod
    def get_executor(language: str) -> ICodeExecutor:
        return CodeExecutorFactory.EXECUTORS.get(language, None)


class SubmissionService:
    def __init__(self, executor_factory: CodeExecutorFactory):
        self.executor_factory = executor_factory

    def run_tests(self, submission):
        executor = self.executor_factory.get_executor(submission.language)
        if not executor:
            self._handle_submission_error(submission, "Unsupported language")
            return

        test_cases = submission.task.test_cases.all()
        total_tests = test_cases.count()
        passed_tests, execution_time = self._execute_tests(submission, executor, test_cases)
        self._save_results(submission, passed_tests, total_tests, execution_time)

    def _execute_tests(self, submission, executor, test_cases):
        passed_tests, execution_time = 0, 0
        for test_case in test_cases:
            output, error, exec_time = executor.run(submission.code, test_case.input_data)
            if error:
                self._handle_submission_error(submission, error)
                return passed_tests, execution_time
            if output.strip() == test_case.expected_output.strip():
                passed_tests += 1
                execution_time += exec_time
        return passed_tests, execution_time

    @staticmethod
    def _handle_submission_error(submission, error_message):
        submission.status = 'runtime_error'
        submission.error_message = error_message
        submission.save()

    @staticmethod
    def _save_results(submission, passed_tests, total_tests, execution_time):
        submission.status = 'correct' if passed_tests == total_tests else 'wrong'
        submission.test_cases_passed = passed_tests
        submission.total_test_cases = total_tests
        submission.execution_time = execution_time
        submission.save()
