import contextlib as _contextlib
import dataclasses as _dataclasses
import os as _os
import subprocess as _subprocess
import tempfile as _tmp

import Bio.SeqIO as _SeqIO
import Bio.SeqRecord as _SR


@_dataclasses.dataclass
class Cline:
    cmd: str = _dataclasses.field(default="igblastn")
    query: str = _dataclasses.field(kw_only=True)
    out: str = _dataclasses.field(kw_only=True)
    auxiliary_data: str = _dataclasses.field(kw_only=True)
    germline_db_V: str = _dataclasses.field(kw_only=True)
    germline_db_D: str = _dataclasses.field(kw_only=True)
    germline_db_J: str = _dataclasses.field(kw_only=True)
    def __iter__(self):
        l = [
            self.cmd,
            '-query', self.query, 
            '-out', self.out,
            '-auxiliary_data', self.auxiliary_data,
            '-germline_db_V', self.germline_db_V,
            '-germline_db_D', self.germline_db_D,
            '-germline_db_J', self.germline_db_J,
            '-domain_system', 'imgt',
            '-num_alignments_V', '1',
            '-num_alignments_J', '1',
            '-num_alignments_D', '1',
            '-outfmt', '7 std qseq sseq btop',
        ] 
        return (x for x in l)
    def dump(self, obj):
        if type(obj) is not _SR.SeqRecord:
            obj = _SR.SeqRecord(obj)
        return _SeqIO.write(self.query, "fasta", obj)
    def exec(self, **kwargs):
        _subprocess.run(list(self), **kwargs)
    @classmethod
    def _file(cls, *, kwargs, key, directory, filename):
    	if key in kwargs.keys():
    		return
        kwargs[k] _os.path.join(directory, filename)
    @classmethod
    @_contextlib.contextmanager
    def manager(cls, cmd, **kwargs):
    	keys = ('query', 'out')
    	tmp_needed = False
    	for k in keys:
    		if k not in kwargs.keys():
    			tmp_needed = True
        if tmp_needed:
            inner_manager = _tmp.TemporaryDirectory()
        else:
            inner_manager = _contextlib.nullcontext()
        with inner_manager as directory:
            cls._file(key="query", kwargs=kwargs, directory=directory, filename="query.fasta")
            cls._file(key="out", kwargs=kwargs, directory=directory, filename="out.txt")
            yield cls(cmd, **kwargs)








