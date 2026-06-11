import os
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType

from batch_recommendation.repository.rating_repo import fetch_als_input


def get_spark():
    return SparkSession.builder \
        .master(os.getenv('SPARK_MASTER', 'local[2]')) \
        .appName("PopcornPick") \
        .config("spark.driver.memory", os.getenv('SPARK_DRIVER_MEMORY', '2g')) \
        .config("spark.sql.shuffle.partitions", os.getenv('SPARK_SHUFFLE_PARTITIONS', '4')) \
        .getOrCreate()


def train_als():
    spark = get_spark()

    rows = fetch_als_input()

    if not rows:
        print("학습 데이터 없음, ALS 스킵")
        return None, None

    schema = StructType([
        StructField("user_id",  IntegerType(), False),
        StructField("movie_id", IntegerType(), False),
        StructField("rating",   FloatType(),   False),
    ])

    df = spark.createDataFrame(
        [(int(r[0]), int(r[1]), float(r[2])) for r in rows],
        schema=schema
    )

    als = ALS(
        userCol="user_id",
        itemCol="movie_id",
        ratingCol="rating",
        rank=10,
        maxIter=10,
        regParam=0.1,
        coldStartStrategy="drop",
        implicitPrefs=False,
    )

    model = als.fit(df)
    print(f"ALS 학습 완료 (학습 데이터: {df.count()}건)")

    return spark, model