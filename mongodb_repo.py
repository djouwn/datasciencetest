class MongoRepository:

    def __init__(
        self,
        mongo_uri: str,
        database_name: str
    ):
        self.client = MongoClient(mongo_uri)

        self.db = self.client[database_name]

        self.posts: Collection = self.db["posts"]
        self.images: Collection = self.db["images"]

        self._create_indexes()

    def _create_indexes(self):
        self.posts.create_index(
            [("post_id", ASCENDING)],
            unique=True
        )

        self.posts.create_index(
            [("topic", ASCENDING)]
        )

        self.posts.create_index(
            [("created_time", ASCENDING)]
        )

        self.images.create_index(
            [("post_id", ASCENDING)]
        )

    def save_post(
        self,
        post: Dict[str, Any]
    ):

        self.posts.update_one(
            {"post_id": post["post_id"]},
            {"$set": post},
            upsert=True
        )

    def save_image(
        self,
        image: Dict[str, Any]
    ):

        self.images.update_one(
            {
                "post_id": image["post_id"]
            },
            {
                "$set": image
            },
            upsert=True
        )