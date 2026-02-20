Import("env", "projenv")

# This script moves third-party libraries from standard Includes (-I) 
# to System Includes (-isystem), telling GCC to ignore their internal warnings.

def convert_to_isystem(e):
    cpppaths = e.get("CPPPATH", [])
    filtered_paths = []
    for p in cpppaths:
        p_str = str(e.Dir(p).abspath)
        # If the include path is a third-party library or Arduino framework
        if "framework" in p_str or ".pio" in p_str:
            # Add it as a system include (-isystem)
            e.Append(CCFLAGS=[("-isystem", p_str)])
        else:
            # Keep it as a normal include (-I) for your own code
            filtered_paths.append(p)
            
    e.Replace(CPPPATH=filtered_paths)

convert_to_isystem(env)
convert_to_isystem(projenv)