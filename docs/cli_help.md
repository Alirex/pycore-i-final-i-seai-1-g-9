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

Also, can be used as a command line tool.

**Usage**:

```console
$ chat run [OPTIONS]
```

**Options**:

* `--show-commands / --no-show-commands`: [default: no-show-commands]
* `--hide-intro / --no-hide-intro`: [default: no-hide-intro]
* `--non-interactive / --no-non-interactive`: [default: no-non-interactive]
* `--plain-render / --no-plain-render`: [default: no-plain-render]
* `--predefined-input TEXT`
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
