'''
 * This is the common logic for both the Node.js and web browser
 * implementations of `debug()`.
 *
 * Expose `debug()` as the module.
 '''

from time import time
from packages.ms import ms
import re

from glob import exports

module = {}

'''
  * Select a color.
  * @param {String} namespace
  * @return {Number}
  * @api private
  '''


def selectColor(namespace):
    hash = 0

    for char in namespace:
        hash = ((hash << 5) - hash) + ord(char)
        # Convert to 32bit (unsigned) integer
        (hash & ((1 << 31) - 1)) - (hash & (1 << 31))

    return exports.colors[abs(hash) % len(exports.colors)]


'''
 * Create a debugger with the given `namespace`.
 *
 * @param {String} namespace
 * @return {Function}
 * @api public
 '''


def createDebug(namespace):
    '''
     * Previous log timestamp.
     '''

    global prevTime
    prevTime = False

    def debug(*arguments):
        # disabled?
        if (not debug.enabled):
            return {}

        global prevTime
        self = debug

        # set `diff` timestamp
        curr = int(time())
        ms = curr - (prevTime or curr)
        self.diff = ms
        self.prev = prevTime
        self.curr = curr
        prevTime = curr

        # turn the `arguments` into a proper Array
        args = []
        for arg in arguments:
            args.append(arg)

        args[0] = exports.coerce(args[0])

        if (str != type(args[0])):
            # anything else let's inspect with %O
            args.insert(0, '%O')

        # apply any `formatters` transformations

        global index
        index = 0

        def replacer(match):
            global index
            # if we encounter an escaped % then don't increase the array index
            if (match == '%%'):
                return match
            index += 1
            if match.start() in exports.formatters:
                formatter = exports.formatters[match.start()]
                if (callable(formatter)):
                    val = args[index]
                    match = formatter(self, val)

                    # now we need to remove `args[index]` since it's inlined in the `format`
                    args.remove(val)
                    index -= 1
            return match

        re.sub(r'%([a-zA-Z%])', replacer, args[0])
        '''args[0] = args[0].replace(/%([a-zA-Z%])/g, function(match, format) {
      # if we encounter an escaped % then don't increase the array index
      if (match === '%%') return match;
      index += 1;
      var formatter = exports.formatters[format];
      if ('function' === typeof formatter) {
        var val = args[index];
        match = formatter.call(self, val);

        # now we need to remove `args[index]` since it's inlined in the `format`
        args.splice(index, 1);
        index -= 1;
      }
      return match;
    })'''

        # apply env-specific formatting (colors, etc.)
        exports.formatArgs(self, args)

        try:
            logFn = exports.log
            pass
        except:
            logFn = print
            pass
        logFn(args)

    debug.namespace = namespace
    debug.enabled = exports.enabled(namespace)
    debug.useColors = exports.useColors()
    debug.color = selectColor(namespace)

    # env-specific initialization logic for debug instances
    if (callable(exports.init)):
        exports.init(debug)

    return debug


'''
 * Enables a debug mode by namespaces. This can include modes
 * separated by a colon and wildcards.
 *
 * @param {String} namespaces
 * @api public
 '''


def enable(namespaces):
    exports.save(namespaces)

    exports.names = []
    exports.skips = []
    split = []
    if (str == type(namespaces)):
        split = re.split(r'[\s, ]+', namespaces)

    for part in split:
        if (part == ''):
            continue  # ignore empty strings
        namespaces = re.sub(r'\*', '.*?', part)
        if (namespaces[0] == '-'):
            exports.skips.append(re.compile('^' + namespaces[1:] + '$'))
        else:
            exports.names.append(re.compile('^' + namespaces + '$'))


'''
 * Disable debug output.
 *
 * @api public
 '''


def disable():
    exports.enable('')


'''
 * Returns True if the given mode name is enabled, False otherwise.
 *
 * @param {String} name
 * @return {Boolean}
 * @api public
 '''


def enabled(name):
    for skip in exports.skips:
        if (skip.search(name)):
            return False

    for n in exports.names:
        if (n.search(name)):
            return True

    return False


'''
 * Coerce `val`.
 *
 * @param {Mixed} val
 * @return {Mixed}
 * @api private
 '''


def coerce(val):
    if (type(val) == Exception):
        return val.stack or val.message
    return val


exports = module = createDebug.debug = createDebug.default = createDebug
exports.coerce = coerce
exports.disable = disable
exports.enable = enable
exports.enabled = enabled
exports.humanize = ms

'''
 * The currently active debug mode names, and names to skip.
 '''

exports.names = []
exports.skips = []

'''
 * Map of special "%n" handling functions, for the debug "format" argument.
 *
 * Valid key names are a single, lower or upper-case letter, i.e. "n" and "N".
 '''

exports.formatters = {}
