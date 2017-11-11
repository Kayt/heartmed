from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=80)),
    Column('name', String(length=100)),
    Column('surname', String(length=100)),
    Column('gender', String(length=50)),
    Column('location', String(length=200)),
    Column('email', String(length=120)),
    Column('password_hash', String(length=80)),
    Column('weight', Float),
    Column('height', Float),
    Column('bio', Text),
    Column('pic', String(length=200)),
    Column('role', String(length=20)),
    Column('flagged', Boolean),
    Column('mydoctor', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['location'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['location'].drop()
