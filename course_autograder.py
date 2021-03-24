#!/usr/bin/python3

# Authors:
# Marie Petitjean mpetitjean22
# Abhinav Sirohi Abhinavnj
# Neeraj Mula Acryptarch
# Yipeng Huang yipenghuang0302

import csv
import re
import os
import shutil
import subprocess
import sys
import tarfile

from datetime import timedelta
from itertools import chain
from pathlib import Path
from typing import Dict, Generator, NamedTuple, Optional, Sequence


class CONFIG:
    CURRENT_PA = 'pa3'
    SUBPARTS = (
        'toHex',
        'binSub',
        'binToFloat',
        'doubleToBin',
        'floatMul',
    )
    SUBMISSIONS_DIR = 'submissions'
    TIME_LIMIT = timedelta(seconds=30)


class Result(NamedTuple):
    final_grade: Optional[int] = None
    subpart_grades: Optional[Dict[str, int]] = None
    error_msg: Optional[str] = None


class StudentMetadataReader:
    def __init__(self, src_gradebook: Path) -> None:
        self._metadata_by_id: Dict[str, Dict[str, str]] = {}

        with src_gradebook.open(newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                student_id = row['ID']
                self._metadata_by_id[student_id] = {
                    k: row[k]
                    for k in (
                        'Student',
                        'ID',
                        'SIS User ID',
                        'SIS Login ID',
                        'Section',
                    )
                }

    def __getitem__(self, student_id: str) -> Optional[Dict[str, str]]:
        metadata = self._metadata_by_id.get(student_id)
        if not metadata:
            return None

        return metadata.copy()


class StudentGradeWriter:
    def __init__(
        self,
        metadata_reader: StudentMetadataReader,
        assignment_name: str,
    ) -> None:
        self._metadata = metadata_reader
        self._assignment_name = assignment_name
        self._timed_out = False
        self._grades: Dict[str, str] = {}

    def __setitem__(self, student_id: str, results: Result) -> None:
        self._grades[student_id] = results

    def write_to_file(self, output_gradebook: Path) -> None:
        fieldnames = (
            'Student',
            'ID',
            'SIS User ID',
            'SIS Login ID',
            'Section',
            self._assignment_name,
        ) + tuple(CONFIG.SUBPARTS)

        with output_gradebook.open('w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for student_id, results in self._grades.items():
                row = self._metadata[student_id]
                if not row:
                    print(f'Student ID {student_id} not found.', file=sys.stderr)
                    continue

                if not results.final_grade:
                    row[self._assignment_name] = results.error_msg
                else:
                    row[self._assignment_name] = results.final_grade
                    for subpart in CONFIG.SUBPARTS:
                        row[subpart] = results.subpart_grades.get(subpart,0)
                writer.writerow(row)


class Submission(NamedTuple):
    tar_path: Path
    extracted_path: Path
    student_id: str


def iter_submissions(submissions_dir: Path) -> Generator[Submission, None, None]:
    for sub_tarball in submissions_dir.iterdir():
        if not sub_tarball.exists() or not tarfile.is_tarfile(sub_tarball):
            continue

        if "LATE" in sub_tarball.name:
            student_id = sub_tarball.name.split('_')[2]
        else:
            student_id = sub_tarball.name.split('_')[1]

        extract_dir = submissions_dir / f'tmp-{student_id}'

        try:
            with tarfile.open(sub_tarball) as tarball:
                    tarball.extractall(extract_dir)

            yield Submission(sub_tarball, extract_dir, student_id)
        except Exception:
            print(f'Failed to extract {sub_tarball}.')

        shutil.rmtree(extract_dir)


def is_file_unchanged(source_of_truth: Path, file_: Path) -> bool:
    result = subprocess.run(
        ['diff', str(source_of_truth), str(file_)],
        # stdout=subprocess.DEVNULL,
    )
    return result.returncode == 0


def overwrite_autograder_files_if_modified(
    source_of_truth_dir: Path,
    submission_dir: Path,
) -> None:
    subparts = CONFIG.SUBPARTS
    for autograder_path in chain(
        ('assignment_autograder.py',),
        (f'{subpart}/Makefile' for subpart in subparts),
        (f'{subpart}/autograder.py' for subpart in subparts),
        (f'{subpart}/tests' for subpart in subparts),
        (f'{subpart}/answers' for subpart in subparts),
    ):
        source_of_truth = source_of_truth_dir / autograder_path

        if not source_of_truth.exists():
            continue

        sot_files = (
            source_of_truth.iterdir()
            if source_of_truth.is_dir()
            else (source_of_truth,)
        )

        for sot_file in sot_files:
            rel_path = sot_file.relative_to(source_of_truth_dir)
            submission_file = submission_dir / rel_path

            if not is_file_unchanged(sot_file, submission_file):
                print(f'Detected modified file: {sot_file}')
                os.makedirs(os.path.dirname(submission_file), exist_ok=True)
                shutil.copyfile(sot_file, submission_file)


def invoke_make_clean(
    submission_dir: Path,
    log_file: Path,
) -> None:
    subparts = CONFIG.SUBPARTS
    for subpart_path in chain(
        (f'{subpart}/' for subpart in subparts),
    ):
        try:
            result = subprocess.run(
                ['make', '--directory', subpart_path, 'clean'],
                cwd=submission_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding='utf-8',
                timeout=CONFIG.TIME_LIMIT.total_seconds(),
            )
            output = result.stdout
        except subprocess.TimeoutExpired as ex:
            output = ex.stdout
            return 'timed out'
        finally:
            with log_file.open('a') as f:
                f.write(output)


def exec_grading_script(path: Path, log_file: Path) -> Result:
    output = ""
    try:
        result = subprocess.run(
            ['python3', str(path.name)],
            cwd=path.parent,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8',
            timeout=CONFIG.TIME_LIMIT.total_seconds(),
        )
        output = result.stdout
    except subprocess.TimeoutExpired as ex:
        output = ex.stdout
        return Result(
            error_msg='timed out'
        )
    except subprocess.CalledProcessError as ex:
        output = ex.stdout
        return Result(
            error_msg='assignment_autograder.py returned non-zero exit status 1.'
        )
    finally:
        with log_file.open('a') as f:
            print(output)
            f.write(output if output else "")
            return gather_results(output, log_file)


def find_matches_or_log(matcch_str: str, output: str, log_file: Path) -> str:
    matches = re.findall(matcch_str, output)
    if not matches:
        raise Exception(f'Unexpected assignment autograder output. See {log_file}.')
    if len(matches) > 1:
        raise Exception(
            f'Score regex has multiple matches which is suspicious. See {log_file}.'
        )
    return matches[0][0]


def gather_results(output: str, log_file: Path) -> Result:
    try:
        final_grade = find_matches_or_log(
            r'Score on assignment: (\d+) out of (\d+)\.',
            output,
            log_file,
        )
    except Exception:
        return Result(
            error_msg=f'Could not gather score on assignment; see: {log_file}'
        )

    subpart_grades = {}
    for subpart in CONFIG.SUBPARTS:
        try:
            subpart_grade = find_matches_or_log(
                f'Score on {subpart}: (\\d+) out of (\\d+)\\.',
                output,
                log_file
            )
            subpart_grades[subpart] = subpart_grade
        except Exception:
            pass

    return Result(
        final_grade,
        subpart_grades,
    )


def main(src_gradebook: Path, output_gradebook: Path) -> None:
    assignment_sot = Path(CONFIG.CURRENT_PA)
    submissions_dir = Path(CONFIG.SUBMISSIONS_DIR)

    metadata_reader = StudentMetadataReader(src_gradebook)
    grade_writer = StudentGradeWriter(metadata_reader, CONFIG.CURRENT_PA)

    for iter, submission in enumerate(iter_submissions(submissions_dir)):
        print(f'\n\nSubmission {iter}:')
        print(repr(submission))

        overwrite_autograder_files_if_modified(
            assignment_sot,
            submission.extracted_path / CONFIG.CURRENT_PA,
        )

        log_file_path = submission.tar_path.with_suffix('.log')
        # clear contents of log file just in case
        open(log_file_path, "w").close()

        invoke_make_clean(
            submission.extracted_path / CONFIG.CURRENT_PA,
            log_file_path,
        )

        results = exec_grading_script(
            submission.extracted_path / CONFIG.CURRENT_PA / 'assignment_autograder.py',
            log_file_path,
        )
        grade_writer[submission.student_id] = results

    grade_writer.write_to_file(output_gradebook)


if __name__ == '__main__':
    main(
        Path('2021-03-03T0028_Grades-01_198_211_05_COMPUTER_ARCHITECTUR.csv'),
        Path(f'{CONFIG.CURRENT_PA}_gradebook.csv'),
    )
