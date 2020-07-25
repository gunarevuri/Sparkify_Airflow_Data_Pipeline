
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    insert_into_sql_stmt = """
        INSERT INTO {} 
        {}
    """

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id = "",
                 table = "",
                 select_query = "",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)

        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.select_query = select_query

    def execute(self, context):

        # connect to redshift cluster

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # As insert_into_sql_stmt is class variable must access through class name if not error will displayed

        redshift.run(LoadFactOperator.insert_into_sql_stmt.format( self.table, self.select_query ))
