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
$ chat run [OPTIONS]
```

**Options**:

* `--show-commands / --no-show-commands`: Show input commands. 

Useful for debugging purposes.

.  [default: no-show-commands]
* `--hide-intro / --no-hide-intro`: Hide the introduction message.

.  [default: no-hide-intro]
* `--non-interactive / --no-non-interactive`: Run in non-interactive mode. 

Do not prompt for user input. Exit after completion of action.

.  [default: no-non-interactive]
* `--plain-render / --no-plain-render`: Render plain text without any special formatting (e.g., colors, styles). 

Useful for simple terminals and CLI automations scripts.

.  [default: no-plain-render]
* `--terminal-simplified / --no-terminal-simplified`: Use simplified terminal input. 

Useful for testing and automation purposes. Also, useful for some debugging tools.

.  [default: no-terminal-simplified]
* `--predefined-input TEXT`: Predefined input to be used instead of prompting the user. 

Useful for testing and automation purposes. Related env: &#x27;PERSYVAL_I_PREDEFINED_INPUT&#x27;

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
