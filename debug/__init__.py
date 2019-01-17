from debug.globals import exports
from debug.debug import module as debug
from os import environ as env
from sys import stdout
from functools import reduce
import re
import time

exports = debugger = debug

# /**
#  * Colors.
#  */

exports.colors = [6, 2, 3, 4, 5, 1]

# /**
#  * Build up the default `inspectOpts` object from the environment variables.
#  *
#  *   $ DEBUG_COLORS=no DEBUG_DEPTH=10 DEBUG_SHOW_HIDDEN=enabled python app.py
#  */


def reducer(obj, key):
    # // camel-case
    prop = re.sub(r'_([a-z])', lambda _, k: k.upper(), key[6:].lower())

    # // coerce string value into JS value
    val = env[key]
    if (re.search(r'^(yes|on|true|enabled)$', val, re.IGNORECASE)):
        val = True
    elif (re.search(r'^(no|off|false|disabled)$', val, re.IGNORECASE)):
        val = False
    else:
        try:
            val = int(val)
        except:
            val = None

    obj[prop] = val
    return obj


exports.inspectOpts = reduce(reducer, [key for key in list(
    env.keys()) if re.search(r'^debug_', key, re.IGNORECASE)], {})

stream = stdout

# /**
#  * Is stdout a TTY? Colored output is enabled when `true`.
#  */


def useColors():
    if ('colors' in exports.inspectOpts):
        return bool(exports.inspectOpts['colors'])
    else:
        return stdout.isatty()


# /**
#  * Adds ANSI color escape codes if enabled.
#  *
#  * @api public
#  */

def formatArgs(self, *arguments):
    name = self.namespace
    useColors = self.useColors

    args = arguments[0]

    if (useColors):
        c = self.color
        prefix = '  \u001b[3' + str(c) + ';1m' + str(name) + ' ' + '\u001b[0m'

        # args[0].split('\n').join('\n' + prefix)
        args[0] = prefix + ('\n' + prefix).join(args[0].split('\n'))
        args.append('\u001b[3' + str(c) + 'm+' +
                    exports.humanize(self.diff) + '\u001b[0m')
    else:
        args[0] = time.strftime(
            '%a, %d %h %Y %H:%M:%S %Z ' + str(name) + ' ' + str(args[0]))

# /**
#  * Invokes `util.format()` with the specified arguments and writes to `stream`.
#  */


def log(*args):
    out = ''
    for arg in args[0]:
        out += str(arg) + ' '
    return stream.write(out + '\n')


# /**
#  * Save `namespaces`.
#  *
#  * @param {String} namespaces
#  * @api private
#  */

def save(namespaces):
    if (None == namespaces):
        # // If you set a process.env field to null or undefined, it gets cast to the
        # // value None. Just delete instead.
        # del env['DEBUG']
        pass
    else:
        env['DEBUG'] = namespaces


# /**
#  * Load `namespaces`.
#  *
#  * @return {String} returns the previously persisted debug modes
#  * @api private
#  */

def load():
    if ('DEBUG' in env):
        return env['DEBUG']
    else:
        return None

# /**
#  * Init logic for `debug` instances.
#  *
#  * Create a new `inspectOpts` object in case `useColors` is set
#  * differently for a particular `debug` instance.
#  */


def init(debug):
    debug.inspectOpts = {}

    keys = exports.inspectOpts.keys()
    for key in keys:
        debug.inspectOpts[key] = exports.inspectOpts[key]


exports.init = init
exports.log = log
exports.formatArgs = formatArgs
exports.save = save
exports.load = load
exports.useColors = useColors

exports.enable(load())
