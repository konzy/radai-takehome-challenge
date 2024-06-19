import os

from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream.connectors.kinesis import FlinkKinesisConsumer
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.table import StreamTableEnvironment
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table.udf import udf
from pyflink.table import StreamTableEnvironment
from pyflink.table import TableDescriptor, Schema, DataTypes, FormatDescriptor


def word_count():

    env = StreamExecutionEnvironment.get_execution_environment()

    consumer_config = {
        'aws.region': 'us-east-1',
        'aws.credentials.provider.basic.accesskeyid': 'test',
        'aws.credentials.provider.basic.secretkey': 'test',
        'flink.stream.initpos': 'LATEST',
    }

    kinesis = env.add_source(FlinkKinesisConsumer('MyStream', SimpleStringSchema(), consumer_config))

    t_env = StreamTableEnvironment.create(env)

    kinesis_table = t_env.from_data_stream(kinesis)

    t_env.create_temporary_view('kinesis_source', kinesis_table)

    # t_env.create_temporary_table(
    #     'kinesis_source',
    #     TableDescriptor.for_connector('kinesis')
    #     .schema(source_schema)
    #     .format(FormatDescriptor.for_format('json').build())
    #     .option('stream', 'MyStream')
    #     .option('aws.endpoint', 'http://localhost:4566')
    #     .option('aws.region', 'us-east-1')
    #     .option('aws.credentials.provider.basic.accesskeyid', 'test')
    #     .option('aws.credentials.provider.basic.secretkey', 'test')
    #     .option('scan.startup.mode', 'latest-offset')
    #     .option('format', 'json')
    #     .build())
    #
    # t_env.create_temporary_table(
    #     's3_sink',
    #     TableDescriptor.for_connector('filesystem')
    #     .schema(Schema.new_builder()
    #             .column('article_id', DataTypes.STRING())
    #             .column('author', DataTypes.STRING())
    #             .column('content', DataTypes.STRING())
    #             .column('publish_date', DataTypes.STRING())
    #             .column('title', DataTypes.STRING())
    #             .column('word_count', DataTypes.BIGINT())
    #             .build())
    #     .format(FormatDescriptor.for_format('json').build())
    #     .option('path', 's3://my-bucket/output')
    #     .option('aws.endpoint', 'http://localstack:4566')
    #     .option('aws.region', 'us-east-1')
    #     .option('aws.credentials.provider.basic.accesskeyid', 'test')
    #     .option('aws.credentials.provider.basic.secretkey', 'test')
    #     .build())
    #
    source_table = t_env.from_path("kinesis_source")

    source_table.execute().print()

    print('success')


if __name__ == '__main__':
    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    os.environ['AWS_ENDPOINT_URL'] = 'http://localhost:4566'

    word_count()
