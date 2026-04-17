import compileall
import sys

success = compileall.compile_dir(".", force=True, quiet=1)

if not success:
    print("Syntax errors detected")
    sys.exit(1)

print("Syntax OK")
