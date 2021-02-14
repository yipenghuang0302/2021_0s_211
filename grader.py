#!/usr/bin/python3

import csv
import re
import shutil
import subprocess
import sys
import tarfile

from datetime import timedelta
from itertools import chain
from pathlib import Path
from typing import Dict, Generator, NamedTuple, Optional, Sequence


class CONFIG:
    CURRENT_PA = 'pa1'
    SUBPARTS = (
        'balanced',
        'bstReverseOrder',
        'goldbach',
        'matMul',
        'maximum',
    )
    SUBMISSIONS_DIR = 'submissions'
    TIME_LIMIT = timedelta(minutes=5)


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

    def __setitem__(self, student_id: str, grade: str) -> None:
        self._grades[student_id] = grade

    def write_to_file(self, output_gradebook: Path) -> None:
        fieldnames = (
            'Student',
            'ID',
            'SIS User ID',
            'SIS Login ID',
            'Section',
            self._assignment_name,
        )

        with output_gradebook.open('w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for student_id, grade in self._grades.items():
                row = self._metadata[student_id]
                if not row:
                    print(f'Student ID {student_id} not found.', file=sys.stderr)
                    continue

                row[self._assignment_name] = grade

                writer.writerow(row)


class Submission(NamedTuple):
    tar_path: Path
    extracted_path: Path
    student_id: str


def iter_submissions(submissions_dir: Path) -> Generator[Submission, None, None]:
    for sub_tarball in submissions_dir.iterdir():
        if not sub_tarball.exists() or not tarfile.is_tarfile(sub_tarball):
            continue

        student_id = sub_tarball.name.split('_')[1]
        extract_dir = submissions_dir / f'tmp-{student_id}'

        with tarfile.open(sub_tarball) as tarball:
            tarball.extractall(extract_dir)

        yield Submission(sub_tarball, extract_dir, student_id)

        shutil.rmtree(extract_dir)


def is_file_unchanged(source_of_truth: Path, file_: Path) -> bool:
    result = subprocess.run(
        ['diff', str(source_of_truth), str(file_)],
        stdout=subprocess.DEVNULL,
    )
    return result.returncode == 0


def overwrite_autograder_files_if_modified(
    source_of_truth_dir: Path,
    submission_dir: Path,
) -> None:
    subparts = CONFIG.SUBPARTS
    for autograder_path in chain(
        ('assignment_autograder.py',),
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
                shutil.copyfile(sot_file, submission_file)


def exec_grading_script(path: Path, log_file: Path) -> str:
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
        return 'timed out'
    finally:
        with log_file.open('w') as f:
            f.write(output)

    matches = re.findall(r'Score on assignment: (\d+) out of (\d+)\.', output)
    if not matches:
        raise Exception(f'Unexpected assignment autograder output. See {log_file}.')
    if len(matches) > 1:
        raise Exception(
            f'Score regex has multiple matches which is suspicious. See {log_file}.'
        )

    return matches[0][0]


def main(src_gradebook: Path, output_gradebook: Path) -> None:
    assignment_sot = Path(CONFIG.CURRENT_PA)
    submissions_dir = Path(CONFIG.SUBMISSIONS_DIR)

    metadata_reader = StudentMetadataReader(src_gradebook)
    grade_writer = StudentGradeWriter(metadata_reader, CONFIG.CURRENT_PA)

    for submission in iter_submissions(submissions_dir):
        print(repr(submission))

        overwrite_autograder_files_if_modified(
            assignment_sot,
            submission.extracted_path / CONFIG.CURRENT_PA,
        )

        grade = exec_grading_script(
            submission.extracted_path / CONFIG.CURRENT_PA / 'assignment_autograder.py',
            submission.tar_path.with_suffix('.log'),
        )
        grade_writer[submission.student_id] = grade

    grade_writer.write_to_file(output_gradebook)


if __name__ == '__main__':
    main(
        Path('2021-02-03T1440_Grades-01_198_211_05_COMPUTER_ARCHITECTUR.csv'),
        Path(f'{CONFIG.CURRENT_PA}_gradebook.csv'),
    )
