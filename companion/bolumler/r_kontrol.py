import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from kontrol import PAKETLER


def calistir(komut, dizin):
    try:
        komut = [os.path.join(".", os.path.relpath(komut[0], dizin)), *komut[1:]]
        sonuc = subprocess.run(komut, cwd=dizin, capture_output=True, text=True,
                               encoding='utf-8', errors='replace', timeout=180)
        return {'cikis_kodu': sonuc.returncode, 'stdout': sonuc.stdout, 'stderr': sonuc.stderr}
    except (OSError, subprocess.TimeoutExpired) as hata:
        return {'cikis_kodu': None, 'hata': str(hata)}


def paket_kontrol(kok, kod, rscript):
    ornek = kok / kod / 'ornek-01'
    kayit = {'paket': kod, 'durum': 'calistirilmadi'}
    if rscript is None:
        kayit['neden'] = 'Rscript bulunamadi; kaynak incelemesi calistirma testi sayilmaz.'
        return kayit
    try:
        with (ornek / 'beklenen-sonuclar.csv').open(encoding='utf-8-sig', newline='') as stream:
            okuyucu = csv.DictReader(stream)
            alanlar = okuyucu.fieldnames
            hedefler = list(okuyucu)
        if alanlar != ['degisken', 'olcu', 'deger'] or not hedefler:
            raise ValueError('Referans CSV bos veya basligi farkli.')
        kayit['beklenen_kontrol_sayisi'] = len(hedefler)
        kayit['girdi_sha256'] = {
            path.relative_to(ornek).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(ornek.rglob('*')) if path.is_file() and path.suffix in ('.R', '.csv')
        }
        with tempfile.TemporaryDirectory(prefix='r-kontrol-', dir='.') as temporary:
            kopya = Path(os.path.relpath(temporary)) / 'ornek-01'
            shutil.copytree(ornek, kopya, ignore=shutil.ignore_patterns('__pycache__'))
            komut = [rscript, '--vanilla', 'cozum.R', '--check']
            kayit['komut'] = 'Rscript --vanilla cozum.R --check'
            kayit['calisma'] = calistir(komut, kopya)
            eslesme = re.search(r'DOGRULANDI:\s*(\d+)\s+kontrol', kayit['calisma'].get('stdout', ''))
            pozitif = (kayit['calisma']['cikis_kodu'] == 0 and eslesme is not None
                       and int(eslesme.group(1)) == len(hedefler))
            hedefler[0]['deger'] = str(float(hedefler[0]['deger']) + 1)
            with (kopya / 'beklenen-sonuclar.csv').open('w', encoding='utf-8', newline='') as stream:
                yazici = csv.DictWriter(stream, fieldnames=alanlar)
                yazici.writeheader()
                yazici.writerows(hedefler)
            kayit['degistirilmis_referans'] = calistir(komut, kopya)
            negatif = kayit['degistirilmis_referans']['cikis_kodu'] not in (None, 0)
            kayit['durum'] = 'gecti' if pozitif and negatif else 'basarisiz'
    except (OSError, ValueError) as hata:
        kayit.update(durum='basarisiz', hata=str(hata))
    return kayit


def main():
    parser = argparse.ArgumentParser(description='17 paketin gercek R yorumlayicisi ile izole kontrolu.')
    parser.add_argument('--rscript', default='Rscript', help='PATH komutu veya calisma dizinine gore goreli Rscript yolu')
    parser.add_argument('--rapor', required=True, help='Yeni, goreli JSON dosyasi')
    secenek = parser.parse_args()
    hedef = Path(secenek.rapor)
    if (hedef.is_absolute() or '..' in hedef.parts or hedef.exists()
            or any(path.is_symlink() for path in (hedef, *hedef.parents))):
        parser.error('Yeni, goreli ve sembolik baglanti icermeyen rapor yolu gerekli.')
    if Path(secenek.rscript).is_absolute():
        parser.error('Rscript icin PATH komutu veya goreli yol kullanin.')
    bulunan = shutil.which(secenek.rscript)
    rscript = os.path.relpath(bulunan) if bulunan else None
    kok = Path(os.path.relpath(Path(__file__).parent))
    rapor = {'tarih_utc': datetime.now(timezone.utc).isoformat(), 'Rscript_bulundu': bulunan is not None,
             'kapsam': 'Gercek R ile --check ve degistirilmis referansi reddetme; SPSS calistirilmaz.',
             'paketler': []}
    if rscript:
        rapor['R_oturumu'] = calistir([rscript, '--vanilla', '-e', 'sessionInfo()'], Path('.'))
    for kod in PAKETLER:
        kayit = paket_kontrol(kok, kod, rscript)
        rapor['paketler'].append(kayit)
        print(kod + ': ' + kayit['durum'], flush=True)
    rapor['gecen'] = sum(kayit['durum'] == 'gecti' for kayit in rapor['paketler'])
    with hedef.open('x', encoding='utf-8') as stream:
        json.dump(rapor, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    if rscript is None:
        return 2
    return 0 if rapor['gecen'] == len(PAKETLER) and rapor['R_oturumu']['cikis_kodu'] == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())