import datetime


def test_restore_jobs(scheduler_1):
    scheduler_1.restore_jobs()
    assert scheduler_1.job_list[0].task_str == 'task_1'
    assert scheduler_1.job_list[0].tries == 1
    assert scheduler_1.job_list[0].start_at == datetime.datetime(2022, 12, 17, 1, 28, 40, 841133)
    assert scheduler_1.job_list[0].dependencies == []
