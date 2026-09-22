import argparse
from collections import Counter
import csv
from itertools import combinations, product
import math
from pathlib import Path
import platform
import random
import statistics


BOOT_OLCU = ('n', 'ortalama', 'ampirik_varyans', 'orneklem_sd', 'kuramsal_boot_se',
             'yeniden_orneklem', 'boot_merkez', 'boot_varyans', 'boot_se',
             'boot_min', 'boot_max', 'alt025', 'ust975', 'boot_yanlilik', 'olasilik_toplami')
PERM_OLCU = ('n_a', 'n_b', 'ortalama_a', 'ortalama_b', 'gozlenen_fark', 'atama_sayisi',
             'uc_atama', 'p_tam', 'en_kucuk_fark', 'en_buyuk_fark', 'sifir_merkezi')


def csv_oku(yol, baslik, adet):
    with yol.open(encoding='utf-8-sig', newline='') as dosya:
        okuyucu = csv.reader(dosya)
        if next(okuyucu, []) != baslik:
            raise ValueError(f'Sutunlar uyusmuyor: {yol.name}')
        satirlar = list(okuyucu)
    if len(satirlar) != adet or any(len(satir) != len(baslik) for satir in satirlar):
        raise ValueError(f'Satir sayisi veya genisligi uyusmuyor: {yol.name}')
    return satirlar


def tamsayi(metin):
    deger = float(metin)
    if not math.isfinite(deger) or deger != int(deger):
        raise ValueError('Sonlu tam sayi gerekli.')
    return int(deger)


def gozlem_oku(yol, gruplu=False):
    baslik = ['id', 'grup', 'deger'] if gruplu else ['id', 'deger']
    adet = 6 if gruplu else 5
    satirlar = csv_oku(yol, baslik, adet)
    temiz = sorted((tamsayi(satir[0]), satir[1] if gruplu else '', float(satir[-1]))
                   for satir in satirlar)
    if [satir[0] for satir in temiz] != list(range(1, adet + 1)):
        raise ValueError('Kimlikler benzersiz ve 1..n olmali.')
    if any(not math.isfinite(satir[-1]) or abs(satir[-1]) > 1e12 for satir in temiz):
        raise ValueError('Bu ogretim paketi sonlu, mutlak degeri en cok 1e12 olan girdiler kabul eder.')
    if gruplu and Counter(satir[1] for satir in temiz) != Counter({'A': 3, 'B': 3}):
        raise ValueError('A ve B grubunda ucer gozlem gerekli.')
    return temiz


def planlar():
    bootstrap = list(product(range(1, 6), repeat=5))
    permutasyon = [tuple(secim) + tuple(kimlik for kimlik in range(1, 7) if kimlik not in secim)
                   for secim in combinations(range(1, 7), 3)]
    return bootstrap, permutasyon


def plan_oku(yol, beklenen):
    genislik = len(beklenen[0])
    satirlar = csv_oku(yol, ['sira'] + [f'ind{numara}' for numara in range(1, genislik + 1)], len(beklenen))
    temiz = sorted(tuple(tamsayi(alan) for alan in satir) for satir in satirlar)
    hedef = [(sira, *satir) for sira, satir in enumerate(beklenen, 1)]
    if temiz != hedef:
        raise ValueError(f'Tam sayim plani eksik veya degistirilmis: {yol.name}')
    return [satir[1:] for satir in temiz]


def girdiler(dizin):
    degerler = [satir[-1] for satir in gozlem_oku(dizin / 'veri.csv')]
    gruplar = gozlem_oku(dizin / 'permutasyon.csv', gruplu=True)
    bootstrap, permutasyon = planlar()
    return (degerler, gruplar,
            plan_oku(dizin / 'bootstrap-plan.csv', bootstrap),
            plan_oku(dizin / 'permutasyon-plan.csv', permutasyon))


def yuzdelik(degerler, olasilik):
    sirali = sorted(degerler)
    konum = (len(sirali) - 1) * olasilik
    alt = math.floor(konum)
    agirlik = konum - alt
    return sirali[alt] * (1 - agirlik) + sirali[min(alt + 1, len(sirali) - 1)] * agirlik


def hesapla(degerler, gruplar, bootstrap, permutasyon):
    ortalama = statistics.mean(degerler)
    ortalamalar = [statistics.mean(degerler[indis - 1] for indis in satir) for satir in bootstrap]
    merkez = statistics.mean(ortalamalar)
    ampirik_varyans = statistics.pvariance(degerler)
    boot_varyans = statistics.pvariance(ortalamalar)
    boot = (5, ortalama, ampirik_varyans, statistics.stdev(degerler),
            math.sqrt(ampirik_varyans / 5), len(ortalamalar), merkez, boot_varyans,
            math.sqrt(boot_varyans), min(ortalamalar), max(ortalamalar),
            yuzdelik(ortalamalar, .025), yuzdelik(ortalamalar, .975), merkez - ortalama,
            math.fsum(adet / len(ortalamalar) for adet in Counter(ortalamalar).values()))
    ortalama_a = statistics.mean(satir[-1] for satir in gruplar if satir[1] == 'A')
    ortalama_b = statistics.mean(satir[-1] for satir in gruplar if satir[1] == 'B')
    gozlenen = ortalama_a - ortalama_b
    tum = [satir[-1] for satir in gruplar]
    farklar = [statistics.mean(tum[indis - 1] for indis in satir[:3]) -
               statistics.mean(tum[indis - 1] for indis in satir[3:]) for satir in permutasyon]
    uc = sum(abs(fark) >= abs(gozlenen) - 1e-12 for fark in farklar)
    perm = (3, 3, ortalama_a, ortalama_b, gozlenen, len(farklar), uc, uc / len(farklar),
            min(farklar), max(farklar), statistics.mean(farklar))
    sonuc = [('bootstrap', olcu, deger) for olcu, deger in zip(BOOT_OLCU, boot)]
    sonuc += [('permutasyon', olcu, deger) for olcu, deger in zip(PERM_OLCU, perm)]
    return sonuc, ortalamalar, farklar


def kontrol_et(sonuc, yol):
    hedefler = csv_oku(yol, ['degisken', 'olcu', 'deger'], len(sonuc))
    for sonuc_satiri, hedef in zip(sonuc, hedefler):
        if list(sonuc_satiri[:2]) != hedef[:2]:
            raise ValueError('Referans etiketleri veya sirasi farkli.')
        deger = float(hedef[-1])
        if not math.isfinite(deger) or not math.isclose(sonuc_satiri[-1], deger, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError(f'Referans uyusmazligi: {hedef[1]}')
    print(f'DOGRULANDI: {len(sonuc)} kontrol degeri eslesiyor.')


def grafik_kaydet(dizin, ortalamalar, farklar, gozlenen):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, eksenler = plt.subplots(1, 2, figsize=(11, 4))
    frekans = Counter(ortalamalar)
    eksenler[0].bar(sorted(frekans), [frekans[deger] / len(ortalamalar) for deger in sorted(frekans)],
                   width=.16, color='#1F4E79')
    for sinir in (yuzdelik(ortalamalar, .025), yuzdelik(ortalamalar, .975)):
        eksenler[0].axvline(sinir, color='#B45F06', linestyle='--')
    eksenler[0].set(title='3125 tam bootstrap orneklemi', xlabel='Ortalama', ylabel='Olasilik')
    frekans = Counter(farklar)
    renkler = ['#B45F06' if abs(deger) >= abs(gozlenen) - 1e-12 else '#1F4E79' for deger in sorted(frekans)]
    eksenler[1].bar(sorted(frekans), [frekans[deger] / len(farklar) for deger in sorted(frekans)],
                   width=.45, color=renkler)
    eksenler[1].set(title='20 tam etiket atamasi', xlabel='A - B ortalama farki', ylabel='Olasilik')
    fig.tight_layout()
    hedef = dizin / 'ciktilar/python'
    hedef.mkdir(parents=True, exist_ok=True)
    fig.savefig(hedef / 'bootstrap-permutasyon.png', dpi=150)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description='Tam bootstrap ve tam permutasyon: iki ayri ogretim ornegi')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--grafik', action='store_true')
    parser.add_argument('--benzetim', action='store_true')
    secenek = parser.parse_args()
    dizin = Path(__file__).parent
    veri = girdiler(dizin)
    sonuc, ortalamalar, farklar = hesapla(*veri)
    for degisken, olcu, deger in sonuc:
        print(f'{degisken:12} {olcu:22} {deger:.12g}')
    if secenek.check:
        kontrol_et(sonuc, dizin / 'beklenen-sonuclar.csv')
    if secenek.grafik:
        grafik_kaydet(dizin, ortalamalar, farklar, dict((olcu, deger) for _, olcu, deger in sonuc)['gozlenen_fark'])
    if secenek.benzetim:
        rng = random.Random(2026)
        tekrarlar = [statistics.mean(rng.choices(veri[0], k=5)) for tekrar in range(10000)]
        print('Monte Carlo (kontrol CSV disi):', statistics.stdev(tekrarlar),
              yuzdelik(tekrarlar, .025), yuzdelik(tekrarlar, .975))
    print('Python', platform.python_version())


if __name__ == '__main__':
    main()