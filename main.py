import click
from storage import Storage
# from pathlib import Path


database = Storage()
database.create_database()
database.create_table()

CONTEXT_SETTING = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTING)
@click.option("--add", "-a",type=(str, str, str), help="Add an item to todolist in format (task number, name, priority, deadline")
@click.option("--list", "-l", is_flag=True, help="List the database as it currently is.")
@click.option("--delete", "-d")
@click.option("--update", "-u", type=int, help="Update an entry in the list according to it's Task number (TID)")
@click.pass_context
def cli(ctx, add, list, delete, update):

    #The add options logic
    if add:
        try:
            name, prio, deadline = (add)
        except TypeError as error:
            click.secho("See help page --help", fg="magenta")

        # Function to add data to todolist database etc.
        # There's no point having 2 todo lists so i will not implement "tablename" stuff here.
        #imported from storage.py
        database.add_task(add)
    #List options logic to display the todolist using the view_todo from the storage.py
    if list:
        columns = f"{'Task':<5}{'Name':<21}{'Priority':<21}{'Deadline':<21}"
        click.secho(columns, fg="black", bg=208)
        if list is True:
            table = database.view_todo()
            for entry in table:
                line = ""
                for _ in entry:
                    if entry.index(_) == 0:
                        line += f"{str(_):<5}"
                    else:
                        line += f"{str(_):<20} "
                click.secho(line, fg="bright_white")
    #The delete option for the program using the delete
    if delete:
        database.delete_todo(delete)
    if update:
        name = click.prompt("What is the new name? Leave blank if none.\n" ,default="")
        prio = click.prompt("What is the new priority? Leave blank if none.\n", default="")
        deadline = click.prompt("What is the new deadline? Leave blank if none.\n", default="")
        task_update = (update, name, prio, deadline)
        database.update_existing(task_update)
    if not(add or update or delete or list):
        click.echo(ctx.get_help())

if __name__ == "__main__":
    cli()

