from telemeta.analysis.vamp.core import *
a = VampCoreAnalyzer()
print a.get_plugins_list()
print a.render(['qm-vamp-plugins', 'qm-tempotracker', 'beats'],'/home/momo/dev/telemeta/telemeta/tests/samples/wav/Cellar-ShowMe-02.wav')

