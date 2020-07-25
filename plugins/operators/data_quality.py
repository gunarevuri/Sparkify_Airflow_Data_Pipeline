from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 # List of tables 
                 tables=[],
                 task_id = "",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables
        self.task_id = task_id

    def execute(self, context):
        # Connect to redshift cluster through PostgresHook
        redshift_hook = PostgresHook(self.redshift_conn_id)
        for table in self.tables:
            records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {table}")
            # If returned 0 records, log details will get errors.
            if len(records) < 1 or len(records[0]) < 1:
                self.log.info(f"Data quality check on {table} failed and retry in 5 minutes")
                raise ValueError("Data quality check failed. {} returned no results".format(table))
            num_records = records[0][0]
            # if records < 2 log details will get errors.
            if num_records < 1:
                self.log.info(f"Data quality check on {table} failed and retry in 5 minutes")
                raise ValueError("Data quality check failed. {} contained 0 rows".format(table))
            self.log.info(f"Data quality on table {table} check passed with {num_records} records")
