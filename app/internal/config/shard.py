shard_config = dict(
    shard_servers = {
        "male_shard": dict(address = "http://male_shard:8000"),
        "female_shard": dict(address = "http://female_shard:8000")
    },
    shard_rules = dict(
        students = lambda student: 'male_shard' if student.sex == 'M' else 'female_shard'
    )
)