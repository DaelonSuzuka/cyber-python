from cyber import CyberVM

cyber = CyberVM()

# print(cyber.get_print())
cyber.set_print(print)

output = cyber.exec('print "hello"')
print(output)

output = cyber.eval('false')
print(output)