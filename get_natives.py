import requests
import zipfile
import io
import shutil

OS = [
    "linux",
    "osx",
    "windows"
]

ARCH = [
   "x86_64",
   "aarch_64"
]

VER = "63"

for os in OS:
    for arch in ARCH:
        if os == "windows" and arch == "aarch_64":
            continue
        print(os, arch)
        url = f"https://repo1.maven.org/maven2/io/netty/incubator/netty-incubator-codec-native-quic/0.0.{VER}.Final/netty-incubator-codec-native-quic-0.0.{VER}.Final-{os}-{arch}.jar"
        r = requests.get(url)
        zfr = io.BytesIO(r.content)
        zf = zipfile.ZipFile(zfr)
        for entry in zf.infolist():
            if entry.is_dir():
                continue
            if entry.filename.startswith("META-INF/native/"):
                nf = zf.open(entry)
                if entry.filename.endswith(".jnilib"):
                    newfn = entry.filename.split("/")[-1].replace(".jnilib", ".dylib")
                    with open("native/" + newfn, "wb") as wf:
                        print(newfn)
                        shutil.copyfileobj(nf, wf)
                        nf.seek(0)
                with open("native/" + entry.filename.split("/")[-1], "wb") as wf:
                    print(entry.filename.split("/")[-1])
                    shutil.copyfileobj(nf, wf)

