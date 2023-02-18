import logging
import clickhouse_connect

from validation_service.utils.logconf import DEFAULT_LOGGER

logger = logging.getLogger(DEFAULT_LOGGER)

create_kafka_sql = """
CREATE TABLE kafka_queue (
 time DateTime,
 correlation_id String,
 check_id String,
 type String
) ENGINE = Kafka('kafka:29092', 'topic_event', 'group1', 'JSONEachRow');
"""

create_table_daily = """
CREATE TABLE daily (
    day Date,
    correlation_id String,
    type String,
    total UInt64
  ) ENGINE = SummingMergeTree()
  ORDER BY (day, correlation_id, type);
"""

create_materialized_view = """
CREATE MATERIALIZED VIEW consumer TO daily
    AS SELECT toDate(toDateTime(time)) AS day, correlation_id, type, count() as total
    FROM kafka_queue GROUP BY day, correlation_id, type;
"""


def create_table():
    client = clickhouse_connect.get_client(host='clickhouse', port='8123', user='default', password='')
    client.command('DROP TABLE IF EXISTS kafka_queue')
    client.command('DROP TABLE IF EXISTS daily')
    client.command('DROP VIEW IF EXISTS consumer')

    client.command(create_kafka_sql)
    client.command(create_table_daily)
    client.command(create_materialized_view)
    logger.info('Tables in Clickhouse created')


def get_data():
    client = clickhouse_connect.get_client(host='clickhouse', port='8123', user='default', password='')
    result = client.query('SELECT correlation_id, sum(total) FROM daily GROUP BY correlation_id;')
    print()
    print(result)
