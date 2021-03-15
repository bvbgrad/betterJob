# Welcome to the betterJob app!


Create Class model for the data object before doing the alembic upgrade

The database evolution is facilitated via alembic
ae => activate venv
# create revision file
alembic revision -m "meaningful comment"
# edit revision file upgrade and downgrade functions
op.create_table, op.add_column, op.drop_table etc....
# run migration to implement upgrade from current state to latest head
alembic upgrade head
# back to nothing
alembic downgrade base

# useful commands
alembic history

