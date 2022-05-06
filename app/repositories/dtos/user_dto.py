import sqlalchemy

UserDTO = sqlalchemy.Table(
    "users",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.Text),
    sqlalchemy.Column("last_name", sqlalchemy.Text),
    sqlalchemy.Column("birth_date", sqlalchemy.DateTime),
    sqlalchemy.Column("created", sqlalchemy.DateTime),
    sqlalchemy.Column("updated", sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column("deleted", sqlalchemy.DateTime, nullable=True),
)
