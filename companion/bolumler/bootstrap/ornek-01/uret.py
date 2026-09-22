import argparse
import csv
from pathlib import Path

from cozum import planlar


def main():
    parser = argparse.ArgumentParser(description='Tam sayim planlarini yeni bir klasore uretir; gozlem verisini degistirmez.')
    parser.add_argument('--hedef', default='yeniden-planlar')
    secenek = parser.parse_args()
    hedef = Path(secenek.hedef)
    if (hedef.is_absolute() or '..' in hedef.parts or hedef == Path('.') or
            hedef.exists() or any(yol.is_symlink() for yol in (hedef, *hedef.parents))):
        parser.error('Goreli, yeni ve sembolik baglanti icermeyen bir hedef gerekli.')
    hedef.mkdir(parents=True, exist_ok=False)
    for ad, satirlar in zip(('bootstrap-plan.csv', 'permutasyon-plan.csv'), planlar()):
        with (hedef / ad).open('w', encoding='utf-8', newline='') as dosya:
            yazici = csv.writer(dosya, lineterminator='\n')
            yazici.writerow(['sira'] + [f'ind{indis}' for indis in range(1, len(satirlar[0]) + 1)])
            yazici.writerows((sira, *satir) for sira, satir in enumerate(satirlar, 1))
    print('Uretildi:', hedef)


if __name__ == '__main__':
    main()