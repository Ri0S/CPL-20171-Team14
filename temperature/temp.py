import subprocess

a = subprocess.Popen(['./temperature', '15'], stdout=subprocess.PIPE).stdout.read().strip()

a = a.split()

print a
print float(a[0]) + float(a[1])
