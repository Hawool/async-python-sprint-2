def test_job_to_dict(job_1):
    expected_data = {
        'dependencies': [],
        'start_at': 123456789.0,
        'task_str': 'task_1',
        'tries': 1
    }
    assert job_1.dict() == expected_data


def test_check_run(job_1):
    assert job_1.check_run() == False
