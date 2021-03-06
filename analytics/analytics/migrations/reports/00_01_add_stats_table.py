SQL = """
create table stats
(
    id serial primary key,
    device_id varchar not null,
    user_id varchar not null,
    timestamp timestamp not null,
    timezone decimal not null,
    local_timestamp timestamp not null,
    path varchar not null,
    action varchar not null,
    os_family varchar not null,
    agent_type integer not null
);
"""


def up(db, conf):
    db.executescript(SQL)
