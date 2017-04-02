import shelve
import os
import re
import queue
import time

from pyprint.ConsolePrinter import ConsolePrinter
from coalib.output.printers.LogPrinter import LogPrinter

from coalib.settings.Section import append_to_sections
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.processes.Processing import instantiate_bears

sections = {}
append_to_sections(sections, 'test', 'val', 'origin', section_name='test')
config_path = os.path.abspath(os.path.join('tests', 'processes',
                                           os.path.dirname(__file__),
                                           'section_executor_test_files', '.coafile'))
testcode_c_path = os.path.join(os.path.dirname(config_path),
                               'testcode.c')

result_queue = queue.Queue()
log_queue = queue.Queue()
console_printer = ConsolePrinter()
log_printer = LogPrinter(ConsolePrinter())

start_gathering_time = time.time()
(sections,
 local_bears,
 global_bears,
 targets) = gather_configuration(lambda *args: True,
                                 log_printer,
                                 arg_list=['--config',
                                           re.escape(config_path)])
end_gathering_time = time.time()

start_write_time = time.time()

with shelve.open('coala-shelf', 'c') as shelf:
    shelf['section'] = sections
    shelf['local_bears'] = local_bears
    shelf['global_bears'] = global_bears
end_write_time = time.time()

start_load_time = time.time()

with shelve.open('coala-shelf', 'r') as shelf:
    for key in shelf.keys():
        pass

end_load_time = time.time()

gathering_duration = end_gathering_time - start_gathering_time
write_duration = end_write_time - start_write_time
load_duration = end_load_time - start_load_time
print('Time taken to gather sections and bears from scratch',
      gathering_duration)
print('Time taken to write', write_duration)
print('Time taken to load', load_duration)
print('Performance improvement = ',
      gathering_duration / (write_duration + load_duration),
      'times')
