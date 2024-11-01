from prefect import flow
from datetime import timedelta, datetime
from prefect.client.schemas.schedules import IntervalSchedule

# Source for the code to deploy (here, a GitHub repo)
SOURCE_REPO="https://github.com/gabrielTecchio/prefect_Test.git"

if __name__ == "__main__":
    flow.from_source(
        source=SOURCE_REPO,
        entrypoint="main.py:flowBCBtoGBQ", # Specific flow to run
    ).deploy(
        name="my-second-deployment",
        work_pool_name="mysecond--work-pool", # Work pool target,
        parameters={"codigo_serie": 1},
        schedules=[
            IntervalSchedule(
            interval=timedelta(minutes=10),
            anchor_date=datetime(2024, 1, 1, 0, 0),
            timezone="America/Chicago"
            )
        ]
    )
