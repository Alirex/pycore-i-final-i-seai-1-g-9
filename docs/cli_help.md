# CLI

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `chat`
* `helpers`

## `chat`

**Usage**:

```console
$ chat [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `run`: Run the personal assistant chat.

### `chat run`

Run the personal assistant chat.

Provides interactive chat with the personal assistant.

Also, it can be used as a command line tool.

**Usage**:

```console
$ chat run [OPTIONS] [PREDEFINED_INPUT]
```

**Arguments**:

* `[PREDEFINED_INPUT]`: Predefined input to be used instead of prompting the user. 

Useful for testing and automation purposes. Related env var: &#x27;PERSYVAL_I_PREDEFINED_INPUT&#x27;

.

**Options**:

* `--show-commands`: Show input commands. 

Useful for debugging purposes.

.
* `--hide-intro`: Hide the introduction message.

.
* `--non-interactive`: Run in non-interactive mode. 

Do not prompt for user input. Exit after completion of action.

.
* `--plain-render`: Render plain text without any special formatting (e.g., colors, styles). 

Useful for simple terminals and CLI automation scripts.

.
* `--terminal-simplified`: Use simplified terminal input. 

Useful for testing and automation purposes. Also, useful for some debugging tools.

.
* `--raise-sys-exit-on-error`: Raise sys.exit(1) on error. 

Useful for testing and automation purposes.

.
* `--throw-full-error`: Throw full error. 

Useful for testing and automation purposes.

.
* `--storage-dir PATH`: Storage directory. 

 Use env var &#x27;PERSYVAL_I_NO_PERSISTENCE&#x27; if you want to disable storing data to the file system.

.
* `--use-advanced-completer`: Use advanced completer. 

 Useful if you need to use advanced commands.

.
* `--help`: Show this message and exit.

## `helpers`

**Usage**:

```console
$ helpers [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `show-paths`: Show the paths that used for storage.
* `clear-storage`: Clear all stored data.
* `fill-storage`: Fill the storage with some data.
* `debug`: Debug the application.

### `helpers show-paths`

Show the paths that used for storage.

**Usage**:

```console
$ helpers show-paths [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `helpers clear-storage`

Clear all stored data.

**Usage**:

```console
$ helpers clear-storage [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `helpers fill-storage`

Fill the storage with some data.

**Usage**:

```console
$ helpers fill-storage [OPTIONS]
```

**Options**:

* `--amount INTEGER`: Amount of entities for each type to be added.  [default: 10]
* `--storage-dir PATH`: Storage directory.
* `--init-only`: Only add data in section, if it doesn&#x27;t exist.
* `--help`: Show this message and exit.

### `helpers debug`

Debug the application.

**Usage**:

```console
$ helpers debug [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
