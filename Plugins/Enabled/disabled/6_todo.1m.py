#!/usr/bin/python

TODO_FILE_LOCATION = "/Users/michaelwagstaff/Documents/Todo/todo.md"


def main():

  todoItems = getTodoItems( TODO_FILE_LOCATION )
  printDetails( todoItems )


def getTodoItems( todo_file_location ):

  todoItems = []

  with open( todo_file_location, 'r' ) as file:
    for line in file:
      todoItems.append( line )

  return todoItems


def printDetails( todoItems ):

  itemIndex = 1

  for todoItem in todoItems:

    if '---' not in todoItem:
      print str( itemIndex ) + '. ' + todoItem.strip()
      itemIndex += 1

    else:
      print '---'


if __name__ == "__main__":
  main()
