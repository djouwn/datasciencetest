import os

from facebook_connector import (
    FacebookConnector,
    MongoRepository,
    SocialMediaCollector,
    TopicFilter
)
def main():

    access_token = os.environ["META_ACCESS_TOKEN"]

    api_version = os.getenv(
        "META_API_VERSION",
        "vXX.X"
    )

    mongo_uri = os.getenv(
        "MONGODB_URI",
        "mongodb://localhost:27017"
    )

    database = os.getenv(
        "MONGODB_DATABASE",
        "social_monitoring"
    )

    # User chooses the topic
    topic = input(
        "Enter the topic you want to monitor: "
    ).strip()

    if not topic:
        print("Error: topic cannot be empty.")
        return

    print(f"\nTopic selected: {topic}")

    # Automatically create the filter
    topic_filter = TopicFilter(topic)

    print(
        f"Keywords detected: "
        f"{topic_filter.keywords}"
    )

    page_id = input(
        "Enter the Facebook Page ID: "
    ).strip()

    connector = FacebookConnector(
        access_token=access_token,
        api_version=api_version
    )

    repository = MongoRepository(
        mongo_uri=mongo_uri,
        database_name=database
    )

    collector = SocialMediaCollector(
        connector=connector,
        repository=repository,
        topic_filter=topic_filter
    )

    collector.collect(
        page_id=page_id,
        topic=topic
    )


if __name__ == "__main__":
    main()