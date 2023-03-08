from .vm import *


try:
    from IPython.core.magic import Magics, magics_class, line_cell_magic

    @magics_class
    class CyberMagics(Magics):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._cyber = CyberVM()
            
            @self._cyber.function('core.print')
            def _print(string: str):
                print(string)

        @line_cell_magic
        def cyber(self, line, cell=None):
            if cell is None:
                self._cyber.eval(line)
            else:
                self._cyber.eval(cell)

    def load_ipython_extension(ipython):
        ipython.register_magics(CyberMagics)

except ImportError:
    pass
