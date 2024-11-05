import csv
import os
from pathlib import Path
from typing import Any
import subprocess

DIR = Path(__file__).resolve().parent
PARTS_CSV_FILE = DIR / 'partitions.csv'
NVS_CSV_FILE = DIR / 'nvs.csv'
NVS_BIN_FILE = DIR / 'nvs.bin'
PARTITION = 'nvs'


def parse_mem_value(s: str) -> int:
    s = s.strip()

    # Check for kilobytes or megabytes suffix and resolve them.
    multipliers = {'K': 1024, 'M': 1024 * 1024}
    if s[-1] in multipliers:
        return int(s[:-1]) * multipliers[s[-1]]

    if s.startswith('0x'):
        return int(s, 16)

    return int(s)


def get_part_offset_size(parts_csv_file: Path, part: str) -> tuple[int, int]:
    with parts_csv_file.open() as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0].strip() != part:
                continue

            offset, size = map(parse_mem_value, row[3:5])
            return offset, size
        else:
            raise ValueError(f'NVS partition not found in {parts_csv_file!r}')


def gen_part_csv(nvs_csv_file: Path, params: dict[str, Any]) -> None:
    with nvs_csv_file.open('w') as f:
        # No spaces after commas to match the `nvs_partition_gen.py` format.
        writer = csv.writer(f,
                            delimiter=',',
                            quotechar='"',
                            lineterminator='\n')
        writer.writerow(['key', 'type', 'encoding', 'value'])

        for namespace, table in params.items():
            if not isinstance(table, dict):
                raise ValueError(f'Invalid namespace: `{namespace}`')

            writer.writerow([namespace, 'namespace', '', ''])

            for key, value in table.items():
                typ = {
                    str: 'string',
                    int: 'i64',
                }

                encoding = typ.get(type(value), None)
                if encoding is None:
                    raise ValueError(
                        f'Unsupported value type: `{type(value)!r}`')

                writer.writerow([key, 'data', encoding, value])


def build_part_bin(nvs_csv_file: Path, nvs_bin_file: Path, size: int) -> None:
    try:
        idf_path = os.environ['IDF_PATH']
    except KeyError:
        raise SystemExit('`IDF_PATH` environment variable not set')

    cmd = [
        f'{idf_path}/components/nvs_flash/nvs_partition_generator/nvs_partition_gen.py',
        'generate',
        str(nvs_csv_file),
        str(nvs_bin_file),
        hex(size),
    ]

    try:
        subprocess.run(cmd,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT,
                       check=True)
    except subprocess.CalledProcessError as e:
        raise SystemExit(f'Error generating NVS partition binary: {e}') from e


def main():
    _, size = get_part_offset_size(PARTS_CSV_FILE, PARTITION)
    params = {
        'factory': {
            'pop': 'popcorn',
            'name': 'Relay Module',
        },
    }
    gen_part_csv(NVS_CSV_FILE, params)
    build_part_bin(NVS_CSV_FILE, NVS_BIN_FILE, size)


if __name__ == '__main__':
    main()
