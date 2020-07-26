from sql_queries import create_tables_list, drop_tables_list
import psycopg2




def drop_tables(cur, conn):
	for query in drop_tables_list:
		print(query+str("drop tables"))
		cur.execute(query)
		conn.commit()
		print("finish ------drop")

def create_tables(cur, conn):
	for query in create_tables_list:
		print("query"+str(query))
		cur.execute(query)
		conn.commit()
		print("finish-------query")


def main():
	values = ('airflowcluster.cen7uusy9typ.us-west-2.redshift.amazonaws.com', 'airflowdb', 'airflow_user','Passw0rd', 5439)
	conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*values))
	cur = conn.cursor()

	drop_tables(cur, conn)
	create_tables(cur, conn)
	print("creation successfull")


if __name__ == '__main__':
	main()