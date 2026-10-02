class SocialMediaCollector:

    def __init__(
        self,
        connector: FacebookConnector,
        repository: MongoRepository,
        topic_filter: TopicFilter
    ):
        self.connector = connector
        self.repository = repository
        self.topic_filter = topic_filter

    def process_post(
        self,
        raw_post: Dict[str, Any],
        topic: str
    ) -> bool:

        post_id = raw_post.get("id")

        if not post_id:
            return False

        message = raw_post.get("message", "")

        # On considère également les commentaires
        # lors du filtrage.
        comments = self.connector.get_comments(post_id)

        comment_text = " ".join(
            comment.get("message", "")
            for comment in comments
        )

        searchable_text = (
            f"{message} {comment_text}"
        )

        if not self.topic_filter.matches(
            searchable_text
        ):
            return False

        post_document = {
            "post_id": post_id,
            "topic": topic,
            "message": message,
            "created_time": raw_post.get(
                "created_time"
            ),
            "permalink": raw_post.get(
                "permalink_url"
            ),
            "author": raw_post.get("from"),
            "comments": comments,
        }

        self.repository.save_post(
            post_document
        )

        image_url = raw_post.get(
            "full_picture"
        )

        if image_url:
            image_document = {
                "post_id": post_id,
                "topic": topic,
                "url": image_url,
                "source": "facebook"
            }

            self.repository.save_image(
                image_document
            )

        return True

    def collect(
        self,
        page_id: str,
        topic: str
    ):

        posts = self.connector.collect_posts(
            page_id
        )

        collected = 0

        for post in posts:

            try:
                if self.process_post(
                    post,
                    topic
                ):
                    collected += 1

            except FacebookAPIError as exc:
                logging.error(
                    "Unable to process post %s: %s",
                    post.get("id"),
                    exc
                )

        logging.info(
            "%d posts collected for topic '%s'",
            collected,
            topic
        )

        return collected