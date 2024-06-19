from faker import Faker

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table.udf import udf
from pyflink.table import StreamTableEnvironment
from pyflink.table import TableDescriptor, Schema, DataTypes, FormatDescriptor

fake = Faker()


def generate_mock_article():
    return {
        'article_id': fake.uuid4(),
        'title': fake.sentence(nb_words=6),
        'author': fake.name(),
        'publish_date': fake.date_time_this_year().isoformat(),
        'content': ' '.join(fake.paragraphs(nb=10))
    }


def main():
    articles = [generate_mock_article() for _ in range(20)]
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(env)

    source_table = t_env.from_elements(articles)

    source_table.print_schema()

    @udf(input_types=[DataTypes.STRING()], result_type=DataTypes.INT())
    def count_words(value: str) -> int:
        return len(value.split())

    t_env.create_temporary_system_function("COUNT_WORDS", count_words)

    result = t_env.sql_query(f"""
        SELECT *, COUNT_WORDS(content) AS word_count
        FROM {source_table}
    """)

    result.execute().print()

    t_env.create_temporary_table(
        'json_file_sink',
        TableDescriptor.for_connector('filesystem')
        .schema(Schema.new_builder()
                .column('article_id', DataTypes.STRING())
                .column('author', DataTypes.STRING())
                .column('content', DataTypes.STRING())
                .column('publish_date', DataTypes.STRING())
                .column('title', DataTypes.STRING())
                .column('word_count', DataTypes.BIGINT())
                .build())
        .format(FormatDescriptor.for_format('json').build())
        .option('path', 'output_path')
        .build())

    result.execute_insert('json_file_sink').wait()

    avg_tbl = t_env.sql_query(f"""
            SELECT sum(word_count) / count(*)
            FROM {result}
        """)

    avg_tbl.execute().print()


if __name__ == '__main__':
    main()
