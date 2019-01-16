def debugger(namespace):
    from os import environ as env
    from time import time

    limColors = [6, 2, 3, 4, 5, 1]
    colors = [20, 21, 26, 27, 32, 33, 38, 39, 40, 41, 42, 43, 44, 45, 56, 57, 62, 63,
              68, 69, 74, 75, 76, 77, 78, 79, 80, 81, 92, 93, 98, 99, 112, 113, 128,
              129, 134, 135, 148, 149, 160, 161, 162, 163, 164, 165, 166, 167, 168,
              169, 170, 171, 172, 173, 178, 179, 184, 185, 196, 197, 198, 199, 200,
              201, 202, 203, 204, 205, 206, 207, 208, 209, 214, 215, 220, 221]

    class Debugger:
        def __init__(self, namespace, colors):
            self.namespace = str(namespace)
            self.color = self.selectColor(namespace, colors)
            self.enabled = True
            self.curr = int(time())
            if ('DEBUG' in env):
                # print(env['DEBUG'])
                pass
            pass

        def selectColor(self, namespace, colors):
            hash = 0
            for i in range(len(namespace)):
                hash = ((hash << 5) - hash) + ord(namespace[i])
                # Convert to 32bit (unsigned) integer
                hash = (hash & ((1 << 31) - 1)) - (hash & (1 << 31))
            return colors[abs(hash) % len(colors)]

        def debug(self, *args):
            # if (not self.enabled):
            #     return

            # curr = int(time())
            # ms = 0
            # try:
            #     ms = curr - self.prev
            # except:
            #     pass
            # self.diff = ms
            # self.prev = self.curr
            # self.curr = curr

            # args2 = []
            # for arg in args:
            #     args2.append(arg)

            # args2[0] = createDebug.coerce(args2[0])  # inspect

            # if (type(args[0]) != 'string'):
            #     # Anything else let's inspect with % O
            #     args2.insert(0, '%O')

            # // Apply any `formatters` transformations
                        # let index = 0;
                        # args[0] = args[0].replace(/%([a-zA-Z%])/g, (match, format) => {
                        # 	// If we encounter an escaped % then don't increase the array index
                        # 	if (match === '%%') {
                        # 		return match;
                        # 	}
                        # 	index++;
                        # 	const formatter = createDebug.formatters[format];
                        # 	if (typeof formatter === 'function') {
                        # 		const val = args[index];
                        # 		match = formatter.call(self, val);

                        # 		// Now we need to remove `args[index]` since it's inlined in the `format`
                        # 		args.splice(index, 1);
                        # 		index--;
                        # 	}
                        # 	return match;
                        # });

            # createDebug.formatArgs.call(self, args);

                        # const logFn = self.log || createDebug.log;
                        # logFn.apply(self, args);

            colorCode = '\u001B[3'
            if (self.color < 8):
                colorCode += str(self.color)
            else:
                colorCode += '8;5;' + str(self.color)
            sequence = \
                colorCode + ';1m' + self.namespace + \
                '\033[0m ' + args[0] + '' + colorCode + \
                'm +' + '163ms' + '\033[0m'
            print(sequence)

    a = Debugger(namespace, limColors)
    return a.debug
