import psycopg2
import psycopg2.extras
import os

def run_query(query):
    try:
        conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PW'],
        port=5432
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query)
        results = cur.fetchall()
        dict_results = [dict(row) for row in results]
        cur.close()
        conn.close()
        return dict_results
    except Exception, err:
        sys.stderr.write('ERROR: %sn' % str(err))
        return 1

def account():
    query = """
    select id, name, industry from accounts limit 1
    """
    data = run_query(query)[0]
    message = "Account ID: {0}\n Name: {1}\n Industry: {2}".format(data['id'], data['name'], data['industry'])
    return message
