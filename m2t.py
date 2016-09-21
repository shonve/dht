import shutil
import tempfile
import os.path as op
import sys
import libtorrent as lt
from time import sleep

def magnet_to_torrent(magnet, output_name = None):
    if output_name and \
            not op.isdir(output_name) and \
            not op.isdir(op.dirname(op.abspath(output_name))):
        print "Invalid output folder:" + op.dirname(op.abspath(output_name))
        sys.exit(0)

    tempdir = tempfile.mkdtemp()
    ses = lt.session()
    params = {
        'save_path': tempdir,
        'duplicate_is_error': True,
        'storage_mode': lt.storage_mode_t(2),
        'paused': False,
        'auto_managed': True,
        'duplicate_is_error': True
    }
    handle = lt.add_magnet_uri(ses, magnet, params)
    print "Downloading Metadata (this may take a while)"
    while (not handle.has_metadata()):
        try:
            sleep(1)
        except KeyboardInterrupt:
            print "Aborting..."
            ses.pause()
            print "Cleanup dir " + tempdir
            shutil.rmtree(tempdir)
            sys.exit(0)
    ses.pause()
    print "Done"
    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)
    output = op.abspath(torinfo.name() + ".torrent")
    if output_name:
        if op.isdir(output_name):
            output = op.abspath(op.join(output_name, torinfo.name() + ".torrent"))
        elif op.isdir(op.dirname(op.abspath(output_name))):
            output = op.abspath(output_name)
    print "Saving torrent file here : " + output + "..."
    torcontent = lt.bencode(torfile.generate())
    f = open(output, 'wb')
    f.write(lt.bencode(torfile.generate()))
    f.close()
    print "Saved! Cleaning up dir: " + tempdir
    ses.remove_torrent(handle)
    shutil.rmtree(tempdir)
    return output

def main():
    magnet = "mdafga"
    output_name = None
    magnet_to_torrent(magnet, output_name)

if __name__ == "__main__":
    main()
