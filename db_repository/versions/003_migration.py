from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
doctor_feed_back = Table('doctor_feed_back', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('content', Text),
    Column('patient', String(length=100)),
    Column('doctor_id', Integer),
)

patient_feed_back = Table('patient_feed_back', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('content', Text),
    Column('patient_id', Integer),
)

query = Table('query', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('content', Text),
    Column('patient_id', Integer),
)

response = Table('response', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('content', Text),
    Column('doctor_id', Integer),
)

doctor = Table('doctor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=80)),
    Column('name', String(length=100)),
    Column('surname', String(length=100)),
    Column('gender', String(length=50)),
    Column('email', String(length=120)),
    Column('password_hash', String(length=80)),
    Column('achievements', Text),
    Column('rank', String(length=100)),
    Column('career', Text),
    Column('bio', Text),
    Column('pic', String(length=200)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['doctor_feed_back'].create()
    post_meta.tables['patient_feed_back'].create()
    post_meta.tables['query'].create()
    post_meta.tables['response'].create()
    post_meta.tables['doctor'].columns['achievements'].create()
    post_meta.tables['doctor'].columns['career'].create()
    post_meta.tables['doctor'].columns['rank'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['doctor_feed_back'].drop()
    post_meta.tables['patient_feed_back'].drop()
    post_meta.tables['query'].drop()
    post_meta.tables['response'].drop()
    post_meta.tables['doctor'].columns['achievements'].drop()
    post_meta.tables['doctor'].columns['career'].drop()
    post_meta.tables['doctor'].columns['rank'].drop()
